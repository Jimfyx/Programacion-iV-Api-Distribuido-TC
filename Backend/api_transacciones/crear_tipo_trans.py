from models.Tipo_transaccion import Tipo_transaccion
from config import db

tipo_transaccion_default =[
    {'nom_tipo_trans': 'Cargo'},
    {'nom_tipo_trans': 'Abono'},
    {'nom_tipo_trans': 'Reversion'},
]

def crear_tipo_trans():
    for tipo in tipo_transaccion_default:
        is_tipo_trans = Tipo_transaccion.query.filter_by(nom_tipo_trans=tipo['nom_tipo_trans']).first()
        if is_tipo_trans is None:
            new_tipo_trans = Tipo_transaccion(nom_tipo_trans=tipo['nom_tipo_trans'])
            db.session.add(new_tipo_trans)
    db.session.commit()