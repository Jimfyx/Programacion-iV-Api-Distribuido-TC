from datetime import date

from models import Transaccion
from config import db

def guardar_transaccion(tarjeta_credito,Cargo,monto,lugar,hora,id_app):
    id_tc = tarjeta_credito.id_tc
    nueva_transaccion = Transaccion.Transaccion(
        id_tipo_trans = int(Cargo),
        id_tc = int(id_tc),
        lugar = lugar,
        hora = hora,
        monto_trans = monto,
        created_by = id_app
    )

    try:
        db.session.add(nueva_transaccion)
        db.session.commit()
        print("Registro guardado en la base de datos")
        return "Registro guardado correctamente", nueva_transaccion
    except Exception as e:
        db.session.rollback()
        print(f"Error al guardar el registro: {e}")
        return "Error al guardar el registro", str(e)