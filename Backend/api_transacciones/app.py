import os
from datetime import datetime

from flask import Flask, request, abort, jsonify
from sqlalchemy import text, create_engine

from services.crud_transaccion import guardar_transaccion
from services.crud_tarjeta_credito import crear_tarjeta_credito, mod_tarjeta_credito, borrar_tarjeta
from services.obtener_tc import obtener_tc
from services.obtener_listado_tc import obtener_listado_tc
from services.balance import obtener_balance
from services import crud_persona
from services import validar_tarjeta_credito
from services.sms_sender import sms_sender
from config import Config, db

from models import Transaccion
from db_init import initializer
app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

def crear_database(db_uri):
    engine = create_engine(db_uri.rsplit('/', 1)[0])
    try:
        connection = engine.connect()
        connection.execute(text("CREATE DATABASE IF NOT EXISTS banco"))
        print("Base de datos creada o ya existente.")
        connection.close()
    except Exception as e:
        print(f'Error al crear la base de datos: {e}')

with app.app_context():

    crear_database(Config.SQLALCHEMY_DATABASE_URI)

    try:
        db.session.execute(text('SELECT 1'))
        print('Conexión exitosa con la base de datos')

        db.create_all(bind_key='banco')
        print('Creación exitosa de las tablas')

        initializer()
        id_app = os.environ.get('HOSTNAME')

    except Exception as e:
        print(f'Error en la creación de la base de datos: {e}')

@app.route('/tarjeta-credito/', methods=['GET'])
def obtener_tarjeta_credito():
    if request.args.get('PAN'):
        return obtener_tc(PAN=request.args.get('PAN')).to_dict()
    else:
        return obtener_listado_tc(), 200  # pendiente agregar, page, perpage, paginate

@app.route('/tarjeta-credito/', methods=['POST'])
def crear_persona_tarjeta_credito():
    body = request.get_json()
    datos = ['nombre', 'apellido', 'edad', 'dpi', 'telefono', 'direccion', 'trabajo', 'salario']
    for dato in datos:
        if dato not in body or body[dato] is None:
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

@app.route('/tarjeta-credito/', methods=['DELETE'])
def eliminar_tarjeta_credito():
    pan = request.args.get('PAN')
    if not pan:
        return jsonify({"message": "El numero de tarjeta es requerido"}), 400
    tarjeta = obtener_tc(PAN=pan)

    if not tarjeta:
        return jsonify({"message": "Tarjeta no encontrada"}), 404
    try:
        balance = obtener_balance(tarjeta)
        monto = tarjeta.monto_max
        if monto == balance:
            borrar_tarjeta(tarjeta)
            return jsonify({"message": f"La tarjeta {pan}, fue borrada exitosamente"}), 200
        return jsonify({"message": f"El saldo disponible de la tarjeta debe ser {monto}", "saldo disponible": f"{balance}"}), 200
    except Exception as e:
        return jsonify({"message": "Error interno del servidor"}), 500


@app.route('/tarjeta-credito/balance/', methods=['GET'])
def balance_tarjeta_credito():
    pan = request.args.get('PAN')
    if not pan:
        return jsonify({"message": "El numero de tarjeta es requerido"}), 400

    tarjeta = obtener_tc(PAN=pan)

    if not tarjeta:
        return jsonify({"message": "Tarjeta no encontrada"}), 404
    try:
        balance = obtener_balance(tarjeta)
        return jsonify({"balance": balance}), 200
    except Exception as e:
        print(f"Error al calcular el balance: {e}")
        return jsonify({"message": "Error interno del servidor"}), 500


@app.route('/tarjeta-credito/procesamiento/', methods=['POST'])
def cargo_tarjeta_credito():
    body = request.get_json()

    #validacion de contenido
    if not body:
        return jsonify({"message": "Solicitud invalida"}), 400

    datos = ['PAN', 'cvv_tc', 'fech_exp_tc', 'monto', 'lugar', 'hora']
    for dato in datos:
        if not body.get(dato):
            return jsonify({"message": f"El dato de {dato} es obligatorio"}), 400


    try:
        monto = body['monto']
    except Exception as e:
        print(f"Error al cargar el monto de la tarjeta: {e}")
        return jsonify({"message": "Error al cargar el monto"}), 400

    #cambia a formato fecha el str que recibe
    fech_exp_tc_obj = datetime.strptime(body['fech_exp_tc'], '%Y-%m-%d').date()

    #se validan los datos de la tarjeta
    tarjeta_credito = validar_tarjeta_credito.validar_tc(body['PAN'],body['cvv_tc'],fech_exp_tc_obj)

    #si no se procesa correctamente la tarjeta se aborta la operacion
    if not tarjeta_credito:
        return jsonify({"message": "Error al procesar la solicitud"}), 400

    try:
        balance = obtener_balance(tarjeta_credito)
    except Exception as e:
        print(f"Error al calcular el balance: {e}")
        return jsonify({"message": "Error interno del servidor"}), 500

    if monto > balance:
        return jsonify({
            "error": "Saldo insuficiente",
            "saldo disponible": balance,
            "monto del cargo": monto
        }), 400


    #prueba enviar los datos a la cola de mensajes y guardar el registro en la tabla de transacciones
    try:
        guardar_transaccion(tarjeta_credito,1,body['monto'],body['lugar'],body['hora'],id_app)
        sms_sender(tarjeta_credito,'Cargo',body['monto'],body['lugar'],body['hora'],id_app)
        return jsonify({
                "mensaje": "Registro guardado correctamente"
        }), 201
    except Exception as e:
        print(f'Error al procesar la solicitud: {e}')
        return jsonify({"error": "Error al procesar la solicitud"}), 500

@app.route('/tarjeta-credito/abono/', methods=['POST'])
def abono_tarjeta_credito():
    body = request.get_json()
    # validacion de contenido
    if not body:
        return jsonify({"message": "Solicitud invalida"}), 400

    datos = ['PAN', 'monto', 'lugar', 'hora']
    for dato in datos:
        if not body.get(dato):
            return jsonify({"message": f"El dato de {dato} es obligatorio"}), 400

    pan = body.get('PAN')
    tarjeta = obtener_tc(PAN=pan)

    # si no se procesa correctamente la tarjeta se aborta la operacion
    if not tarjeta:
        return jsonify({"message": "Error al verificar el numero de tarjeta de credito"}), 400

    # prueba enviar los datos a la cola de mensajes y guardar el registro en la tabla de transacciones
    try:
        guardar_transaccion(tarjeta, 2, body['monto'], body['lugar'], body['hora'], id_app)
        sms_sender(tarjeta, 'Cargo', body['monto'], body['lugar'], body['hora'], id_app)
        return jsonify({
            "mensaje": "Registro guardado correctamente"
        }), 201
    except Exception as e:
        print(f'Error al procesar la solicitud: {e}')
        return jsonify({"error": "Error al procesar la solicitud"}), 500

@app.route('/tarjeta-credito/reversion/', methods=['POST'])
def reversion_tarjeta_credito():
    body = request.get_json()

    #validacion de contenido
    if not body:
        return jsonify({"message": "Solicitud invalida"}), 400

    datos = ['PAN', 'cvv_tc', 'fech_exp_tc', 'monto', 'lugar', 'hora']
    for dato in datos:
        if not body.get(dato):
            return jsonify({"message": f"El dato de {dato} es obligatorio"}), 400


    try:
        monto = body['monto']
    except Exception as e:
        print(f"Error al cargar el monto de la tarjeta: {e}")
        return jsonify({"message": "Error al cargar el monto"}), 400

    #cambia a formato fecha el str que recibe
    fech_exp_tc_obj = datetime.strptime(body['fech_exp_tc'], '%Y-%m-%d').date()

    #se validan los datos de la tarjeta
    tarjeta_credito = validar_tarjeta_credito.validar_tc(body['PAN'],body['cvv_tc'],fech_exp_tc_obj)

    #si no se procesa correctamente la tarjeta se aborta la operacion
    if not tarjeta_credito:
        return jsonify({"message": "Error al procesar la solicitud"}), 400


    #prueba enviar los datos a la cola de mensajes y guardar el registro en la tabla de transacciones
    try:
        guardar_transaccion(tarjeta_credito,3,body['monto'],body['lugar'],body['hora'],id_app)
        sms_sender(tarjeta_credito,'Cargo',body['monto'],body['lugar'],body['hora'],id_app)
        return jsonify({
                "mensaje": "Registro guardado correctamente"
        }), 201
    except Exception as e:
        print(f'Error al procesar la solicitud: {e}')
        return jsonify({"error": "Error al procesar la solicitud"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')