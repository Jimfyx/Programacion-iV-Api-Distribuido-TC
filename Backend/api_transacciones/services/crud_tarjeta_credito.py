import random
from datetime import datetime, timedelta

from flask import jsonify, abort
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

def mod_tarjeta_credito(PAN,cvv_tc, fech_exp_tc, id_estado, monto_max):
    tarjeta_credito_mod = Tarjeta_credito.Tarjeta_credito.query.filter_by(numero_tc=PAN).first()
    if tarjeta_credito_mod is None:
        abort(400, "No se encontraron coincidencias con el numero de tarjeta proporcionado")

    if cvv_tc is not None:
        tarjeta_credito_mod.cvv_tc = cvv_tc

    if fech_exp_tc is not None:
        try:
            tarjeta_credito_mod.fech_exp_tc = datetime.strptime(fech_exp_tc, '%Y-%m-%d').date()
        except ValueError:
            abort(400, "Formato de fecha invalido. 'YYYY-MM-DD'.")

    if id_estado is not None:
        tarjeta_credito_mod.id_estado = id_estado

    if monto_max is not None:
        tarjeta_credito_mod.monto_max = monto_max

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        abort(500, f"Error al actualizar la tarjeta de credito: {str(e)}")

    return jsonify({"message": "Tarjeta actualizada"}), 200

def borrar_tarjeta(tarjeta):

    try:
        db.session.delete(tarjeta)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        abort(500, f"Error al borrar la tarjeta de crédito: {str(e)}")

    return jsonify({"message": "Tarjeta borrada exitosamente"}), 200