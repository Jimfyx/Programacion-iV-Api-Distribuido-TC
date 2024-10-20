from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:toor@192.168.0.21:3306/banco'
    SQLALCHEMY_TRACK_MODIFICATIONS = False