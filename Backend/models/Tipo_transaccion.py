from config import db

class Tipo_transaccion(db.Model):
    __tablename__ = 'tipo_transaccion'

    id_tipo_trans = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom_tipo_trans = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {
            'id_tipo_trans': self.id_tipo_trans,
            'nom_tipo_trans': self.nom_tipo_trans
        }