from config import db
from models import smsdr

def data_record(data):

    data_parts = data.split('|')

    numero_tc = data_parts[0]
    tipo_trans = data_parts[1]
    monto = data_parts[2]
    lugar = data_parts[3]
    hora = data_parts[4]
    enviado_por = data_parts[5]
    mensaje_enviado = f"Se ha realizado un {tipo_trans} a su tarjeta de credito numero {numero_tc}, por un monto de Q.{monto}, en {lugar}, a la hora {hora}, autorizado por {enviado_por}."


    nueva_transaccion = smsdr.Mdr(
        numero_tc = numero_tc,
        tipo_trans = tipo_trans,
        monto = monto,
        lugar = lugar,
        hora = hora,
        enviado_por = enviado_por,
        mensaje_enviado = mensaje_enviado
    )

    try:
        db.session.add(nueva_transaccion)
        db.session.commit()
        print("Registro guardado en la base de datos")
        return "Registro guardado correctamente", mensaje_enviado
    except Exception as e:
        db.session.rollback()
        print(f"Error al guardar el registro: {e}")
        return "Error al guardar el registro", str(e)