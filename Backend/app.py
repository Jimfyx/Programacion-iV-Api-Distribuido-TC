from flask import Flask
from sqlalchemy import text

from config import Config, db

from models import Estado,Tipo_transaccion,Persona,Tarjeta_credito,Transaccion
from db_init import initializer
app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    try:
        db.session.execute(text('SELECT 1'))
        print('Conexión exitosa con la base de datos')

        db.create_all()
        print('Creación exitosa de las tablas')

        initializer()

    except Exception as e:
        print(f'Error en la creación de la base de datos: {e}')

if __name__ == '__main__':
    app.run(debug=True)