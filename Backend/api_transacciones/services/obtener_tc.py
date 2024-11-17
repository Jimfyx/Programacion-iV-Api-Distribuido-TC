from flask import abort
from models import Tarjeta_credito

def obtener_tc(PAN):
    tarjeta = Tarjeta_credito.Tarjeta_credito.query.filter_by(numero_tc=PAN).first()

    if not tarjeta:
        return None
    return tarjeta
