from config import db

class Mdr(db.Model):
    __tablename__ = 'mdr'

    id_mdr = db.Column(db.Integer, primary_key=True, autoincrement=True)
    numero_tc = db.Column(db.BigInteger, nullable=False, unique=True)
    tipo_trans = db.Column(db.String(50), nullable=False)
    monto = db.Column(db.Numeric, nullable=False)
    lugar_consumo = db.Column(db.String(50), nullable=False, unique=True)
    hora_consumo = db.Column(db.Time, nullable=False)
    mensaje_enviado = db.Column(db.String(50), nullable=False, default='xxxxx')
    enviado_por = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {
            'id_mdr': self.id_smsdr,
            'numero_tc': self.numero_tc,
            'tipo_trans': self.tipo_trans,
            'monto': self.monto,
            'lugar_consumo': self.lugar_consumo,
            'hora_consumo': self.hora_consumo,
            'mensaje_enviado': self.mensaje_enviado,
            'enviado_por': self.enviado_por
        }