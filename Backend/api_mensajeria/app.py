from flask import Flask,jsonify
import pika
from sqlalchemy import text, create_engine

from models import smsdr
from services import sms_service
from config import Config, db

app = Flask(__name__)

app.config.from_object(Config)

def crear_database(db_uri):
    engine = create_engine(db_uri.rsplit('/', 1)[0])
    try:
        connection = engine.connect()
        connection.execute(text("CREATE DATABASE IF NOT EXISTS message"))
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

    except Exception as e:
        print(f'Error en la creación de la base de datos: {e}')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")