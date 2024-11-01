from flask import Flask,jsonify
import pika
from sqlalchemy import text

from models import smsdr
from services import sms_service
from config import Config, db

app = Flask(__name__)

app.config.from_object(Config)

with app.app_context():
    try:
        db.session.execute(text('SELECT 1'))
        print('Conexión exitosa con la base de datos')

        db.create_all()
        print('Creación exitosa de las tablas')

    except Exception as e:
        print(f'Error en la creación de la base de datos: {e}')

if __name__ == '__main__':
    app.run(debug=True)