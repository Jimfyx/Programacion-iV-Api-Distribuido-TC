from models.Estado import Estado
from config import db

estados_default = [
    {'nom_estado': 'Creada'},
    {'nom_estado': 'Activo'},
    {'nom_estado': 'Inactivo'},
    {'nom_estado': 'Activa'},
    {'nom_estado': 'Inactiva'},
    {'nom_estado': 'Habilitado'},
    {'nom_estado': 'Inhabilitado'},
    {'nom_estado': 'Habilitada'},
    {'nom_estado': 'Inhabilitada'},
    {'nom_estado': 'Bloqueada'},
    {'nom_estado': 'Vencida'},
]

def crear_estados():
    for estado in estados_default:
        is_estado = Estado.query.filter_by(nom_estado=estado['nom_estado']).first()
        if is_estado is None:
            new_estado = Estado(nom_estado=estado['nom_estado'])
            db.session.add(new_estado)
    db.session.commit()