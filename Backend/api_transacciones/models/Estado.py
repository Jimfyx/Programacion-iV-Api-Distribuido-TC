from config import db

class Estado(db.Model):
    __bind_key__ = 'banco'
    __tablename__ = 'estado'

    id_estado = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom_estado = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {
            'id_estado': self.id_estado,
            'nom_estado': self.nom_estado,
        }