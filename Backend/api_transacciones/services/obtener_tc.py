from models import Tarjeta_credito

def obtener_tc(PAN):
    tarjeta = Tarjeta_credito.Tarjeta_credito.query.filter_by(numero_tc=PAN).first()
    return tarjeta.to_dict()