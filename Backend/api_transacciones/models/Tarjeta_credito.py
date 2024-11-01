from config import db

class Tarjeta_credito(db.Model):
    __tablename__ = 'tarjeta_credito'

    id_tc = db.Column(db.Integer, primary_key=True, autoincrement=True)
    numero_tc = db.Column(db.BigInteger, nullable=False, unique=True)
    cvv_tc = db.Column(db.SmallInteger, nullable=False)
    fech_exp_tc = db.Column(db.Date, nullable=False)
    id_estado = db.Column(db.Integer, db.ForeignKey('estado.id_estado'), nullable=False, default=1)
    id_persona = db.Column(db.Integer, db.ForeignKey('persona.id_persona'), nullable=False)
    monto_max = db.Column(db.Numeric, nullable=False)
    fech_creacion_tc = db.Column(db.Date, nullable=False)
    created_by = db.Column(db.String(50), nullable=False, default='admin')

    estado = db.relationship('Estado', backref='estadostc', lazy=True)
    persona = db.relationship('Persona', backref='personas', lazy=True)

    def to_dict(self):
        return {
            'id_tc': self.id_tc,
            'numero_tc': self.numero_tc,
            'cvv_tc': self.cvv_tc,
            'fech_exp_tc': self.fech_exp_tc,
            'id_estado': self.id_estado,
            'id_persona': self.id_persona,
            'monto_max': self.monto_max,
            'fech_creacion_tc': self.fech_creacion_tc,
            'created_by': self.created_by
        }