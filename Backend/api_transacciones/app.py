import os
from datetime import datetime
from os import abort

from flask import Flask, request
from sqlalchemy import text, create_engine

from services.crud_tarjeta_credito import crear_tarjeta_credito, mod_tarjeta_credito
from services.obtener_tc import obtener_tc
from services.obtener_listado_tc import obtener_listado_tc
from services import crud_persona
from services import validar_tarjeta_credito
from services.sms_sender import sms_sender
from config import Config, db

from models import Estado,Tipo_transaccion,Persona,Transaccion
from models import Tarjeta_credito
from db_init import initializer
app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

def crear_database(db_uri):
    engine = create_engine(db_uri.rsplit('/', 1)[0])
    try:
        connection = engine.connect()
        connection.execute("CREATE DATABASE IF NOT EXISTS banco")
        print("Base de datos creada o ya existente.")
    except Exception as e:
        print(f'Error al crear la base de datos: {e}')
    finally:
        connection.close()

with app.app_context():

    crear_database(Config.SQLALCHEMY_DATABASE_URI)

    try:
        db.session.execute(text('SELECT 1'))
        print('Conexión exitosa con la base de datos')

        db.create_all()
        print('Creación exitosa de las tablas')

        initializer()
        id_app = os.environ.get('HOSTNAME')

    except Exception as e:
        print(f'Error en la creación de la base de datos: {e}')

@app.route('/tarjeta-credito/', methods=['GET'])
def obtener_tarjeta_credito():
    if request.args.get('PAN'):
        return obtener_tc(PAN=request.args.get('PAN'))
    else:
        return obtener_listado_tc(), 200  # pendiente agregar, page, perpage, paginate

@app.route('/tarjeta-credito/', methods=['POST'])
def crear_persona_tarjeta_credito():
    body = request.get_json()
    datos = [body['nombre'], body['apellido'], body['edad'], body['dpi'], body['telefono'], body['direccion'], body['trabajo'], body['salario']]
    for dato in datos:
        if dato not in datos:
            abort(400, f"El dato de {dato} es obligatorio")

    id_new_persona, salario_new_persona = crud_persona.crear_persona(body['nombre'], body['apellido'], body['edad'], body['dpi'], body['telefono'], body['direccion'], body['trabajo'], body['salario'], id_app)
    return crear_tarjeta_credito(id_new_persona, salario_new_persona, id_app)

@app.route('/tarjeta-credito/', methods=['PUT'])
def modificar_tarjeta_credito():
    body = request.get_json()
    if not body.get('PAN'):
        abort(400, 'El numero de tarjeta es requerido')

    cvv_tc = body.get('cvv_tc')
    fech_exp_tc = body.get('fech_exp_tc')
    id_estado = body.get('id_estado')
    monto_max = body.get('monto_max')

    return mod_tarjeta_credito(body['PAN'], cvv_tc, fech_exp_tc, id_estado, monto_max)

@app.route('/tarjeta-credito/balance')

@app.route('/tarjeta-credito/procesamiento/', methods=['POST'])
def cargo_tarjeta_credito():
    body = request.get_json()

    #validacion de contenido
    if not body:
        abort(400, 'Solicitud invalida')

    datos = [body['monto'], body['lugar_consumo'], body['hora_consumo']]
    for dato in datos:
        if dato not in datos:
            abort(400, f"El dato de {dato} es obligatorio")

    #cambia a formato fecha el str que recibe
    fech_exp_tc_obj = datetime.strptime(body['fech_exp_tc'], '%Y-%m-%d').date()

    #se validan los datos de la tarjeta
    tarjeta_credito = validar_tarjeta_credito.validar_tc(body['PAN'],body['cvv_tc'],fech_exp_tc_obj)

    #si no se procesa correctamente la tarjeta se aborta la operacion
    if not tarjeta_credito:
        abort(400, 'Error al procesar la solicitud')


    #prueba enviar los datos a la cola de mensajes
    try:
        sms_sender(tarjeta_credito.numero_tc,'Cargo',body['monto'],body['lugar_consumo'],body['hora_consumo'],id_app)
    except Exception as e:
        print(f'Error al procesar la solicitud: {e}')
    return '', 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')