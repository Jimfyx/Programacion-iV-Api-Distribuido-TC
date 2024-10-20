from config import db

class Persona(db.Model):
    __tablename__ = 'persona'

    id_persona = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    dpi = db.Column(db.Integer, nullable=False, unique=True)
    telefono = db.Column(db.Integer, nullable=False)
    direccion = db.Column(db.String(50), nullable=False, default='ciudad')
    trabajo = db.Column(db.String(50), nullable=False)
    salario = db.Column(db.Integer, nullable=False)
    id_estado = db.Column(db.Integer, db.ForeignKey('estado.id_estado'), nullable=False, default=1)
    created_by = db.Column(db.String(50), nullable=False)

    estado = db.relationship('Estado', backref='estadosp', lazy=True)

    def to_dict(self):
        return {
            'id_persona': self.id_persona,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'edad': self.edad,
            'dpi': self.dpi,
            'telefono': self.telefono,
            'direccion': self.direccion,
            'trabajo': self.trabajo,
            'salario': self.salario,
            'id_estado': self.id_estado,
            'created_by': self.created_by
        }