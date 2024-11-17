from datetime import date

from config import db

class Transaccion(db.Model):
    __bind_key__ = 'banco'
    __tablename__ = 'transaccion'

    id_trans = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_tipo_trans = db.Column(db.Integer, db.ForeignKey('tipo_transaccion.id_tipo_trans'), nullable=False)
    id_tc = db.Column(db.Integer, db.ForeignKey('tarjeta_credito.id_tc'), nullable=False)
    fech_trans = db.Column(db.Date, nullable=False, default=date.today)
    lugar = db.Column(db.String(50), nullable=False)
    hora = db.Column(db.Time, nullable=False)
    monto_trans = db.Column(db.Numeric(10,2), nullable=False)
    created_by = db.Column(db.String(50), nullable=False)

    tipo_transaccion = db.relationship('Tipo_transaccion', backref='transacciones', lazy=True)
    tarjeta_credito = db.relationship('Tarjeta_credito', backref='tarjetacredito', lazy=True)


    def to_dict(self):
        return {
            'id_trans': self.id_trans,
            'id_tipo_trans': self.id_tipo_trans,
            'id_tc': self.id_tc,
            'fech_trans': self.fech_trans,
            'monto_trans': self.monto_trans,
            'created_by': self.created_by
        }