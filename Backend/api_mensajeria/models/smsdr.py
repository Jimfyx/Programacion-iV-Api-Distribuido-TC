from config import db

class Mdr(db.Model):
    __tablename__ = 'mdr'

    id_mdr = db.Column(db.Integer, primary_key=True, autoincrement=True)
    numero_tc = db.Column(db.BigInteger, nullable=False)
    tipo_trans = db.Column(db.String(50), nullable=False)
    monto = db.Column(db.Numeric(10,2), nullable=False)
    lugar = db.Column(db.String(50), nullable=False)
    hora = db.Column(db.Time, nullable=False)
    mensaje_enviado = db.Column(db.String(255), nullable=False)
    enviado_por = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {
            'id_mdr': self.id_mdr,
            'numero_tc': self.numero_tc,
            'tipo_trans': self.tipo_trans,
            'monto': self.monto,
            'lugar': self.lugar,
            'hora': self.hora,
            'mensaje_enviado': self.mensaje_enviado,
            'enviado_por': self.enviado_por
        }