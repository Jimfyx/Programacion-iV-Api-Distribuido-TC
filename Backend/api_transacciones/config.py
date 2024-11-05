from flask_sqlalchemy import SQLAlchemy
import pika

db = SQLAlchemy()
#primeros 4 digitos de la tarjeta
digito_ini_tc = 6800
#monto maximo de la tarjeta 3 veces sueldo
multiplo_monto = 3

def get_pika_connection():
    conexion_config = pika.ConnectionParameters('192.168.0.16', 5672)
    try:
        conexion = pika.BlockingConnection(conexion_config)
        channel = conexion.channel()
        return channel, conexion
    except pika.exceptions.AMQPConnectionError:
        print("No se pudo establecer conexión con RabbitMQ")
        return None

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:root@192.168.0.17:3306/banco'
    SQLALCHEMY_TRACK_MODIFICATIONS = False