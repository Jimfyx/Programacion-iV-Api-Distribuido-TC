from sqlalchemy import func
from models import Transaccion
from config import db

def obtener_balance(tc):
    gastado = 0
    abonado = 0
    reversion = 0
    monto_max = tc.monto_max
    try:
        gastado = db.session.query(func.sum(Transaccion.Transaccion.monto_trans)).filter(Transaccion.Transaccion.id_tipo_trans == 1, Transaccion.Transaccion.id_tc == tc.id_tc).scalar() or 0

    except Exception as e:
        print(f"error al obtener el saldo gastado",{str(e)})

    try:
        abonado = db.session.query(func.sum(Transaccion.Transaccion.monto_trans)).filter(Transaccion.Transaccion.id_tipo_trans == 2, Transaccion.Transaccion.id_tc == tc.id_tc).scalar() or 0

    except Exception as e:
        print(f"error al obtener el saldo abonado",{str(e)})

    try:
        reversion = db.session.query(func.sum(Transaccion.Transaccion.monto_trans)).filter(Transaccion.Transaccion.id_tipo_trans == 3, Transaccion.Transaccion.id_tc == tc.id_tc).scalar() or 0

    except Exception as e:
        print(f"error al obtener el saldo reversion",{str(e)})

    balance = monto_max - ((gastado + reversion) - (abonado))

    return balance
