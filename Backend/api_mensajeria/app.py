import threading

from flask import Flask,jsonify
from sqlalchemy import text, create_engine

from models import smsdr
from services import sms_service
from config import Config, db

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

def crear_database_y_tablas():
    db_uri = Config.SQLALCHEMY_DATABASE_URI
    engine = create_engine(db_uri.rsplit('/', 1)[0])

    try:
        with engine.connect() as connection:
            connection.execute(text("CREATE DATABASE IF NOT EXISTS message"))
            print("Base de datos creada o ya existente.")

        with app.app_context():
            db.create_all()
            print("Creación exitosa de las tablas")

    except Exception as e:
        print(f"Error al crear la base de datos o las tablas: {e}")


def start_sms_service():
    sms_service.main()


if __name__ == '__main__':
    crear_database_y_tablas()
    hilo_sms_service = threading.Thread(target=start_sms_service)
    hilo_sms_service.start()
    app.run(debug=True, host="0.0.0.0")