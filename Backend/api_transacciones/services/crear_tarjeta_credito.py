import random
from datetime import datetime, timedelta
from os import abort

from flask import jsonify
from models import Tarjeta_credito
from config import db, digito_ini_tc, multiplo_monto

from services import crud_persona


def crear_tarjeta_credito(id_persona, salario, creador):
    if id_persona == None or salario == None:
        abort(500, "Ha ocurrido un error interno en la creacion de la tarjeta de credito")

    while True:
        num_random_01 = random.randint(1000,9999)
        num_random_02 = random.randint(1000,9999)
        num_random_03 = random.randint(1000,9999)

        num_tc_final = int(str(digito_ini_tc) + str(num_random_01) + str(num_random_02) +str(num_random_03))

        test_num_tc_final = Tarjeta_credito.Tarjeta_credito.query.filter_by(numero_tc=num_tc_final).first()
        if test_num_tc_final is None:
            break

    new_cvv_tc = random.randint(100,999)
    new_fech_creacion_tc = datetime.now()
    new_fech_exp_tc = new_fech_creacion_tc + timedelta(days=720)
    limite_tc = (multiplo_monto*salario)


    new_tc = Tarjeta_credito.Tarjeta_credito(numero_tc=num_tc_final, cvv_tc=new_cvv_tc, fech_exp_tc=new_fech_exp_tc,
                                             id_persona=id_persona, monto_max=limite_tc, fech_creacion_tc=new_fech_creacion_tc, created_by=creador)

    try:
        db.session.add(new_tc)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        crud_persona.borrar_persona(id_persona)
        abort(500, f'Error al guardar la tarjeta de credito, se borro la persona creada: {str(e)}')
    return jsonify({"message": "Tarjeta Creada",
                    "numero de tarjeta de credito": new_tc.numero_tc}), 200