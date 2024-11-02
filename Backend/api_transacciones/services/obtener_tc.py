from flask import abort
from models import Tarjeta_credito

def obtener_tc(PAN):
    tarjeta = Tarjeta_credito.Tarjeta_credito.query.filter_by(numero_tc=int(PAN)).first()

    if not tarjeta:
        abort(404, 'Tarjeta de crédito no encontrada')

    return tarjeta.to_dict(), 200
