from models import Tarjeta_credito

def obtener_listado_tc():
    tarjetas = Tarjeta_credito.Tarjeta_credito.query.all()
    return [tarjeta.to_dict() for tarjeta in tarjetas]