import time

from flask_sqlalchemy import SQLAlchemy
import pika

db = SQLAlchemy()

def get_pika_connection():
    conexion_config = pika.ConnectionParameters(host='rabbitmq-app', port=5672)
    try:
        conexion = pika.BlockingConnection(conexion_config)
        print("Conexión establecida con RabbitMQ")
        channel = conexion.channel()
        return channel
    except pika.exceptions.AMQPConnectionError:
        print("No se pudo establecer conexión con RabbitMQ.")
    return None

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:root@mysql-app:3306/message'
    SQLALCHEMY_TRACK_MODIFICATIONS = False