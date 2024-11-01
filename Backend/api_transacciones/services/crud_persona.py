from flask import abort, jsonify
from models import Persona
from config import db

def crear_persona(nombre,apellido,edad,dpi,telefono,direccion,trabajo,salario,creador):
    dpi_obj = Persona.Persona.query.filter_by(dpi=dpi).first()
    if dpi_obj:
        abort(400, 'DPI ya registrado')
    new_persona = Persona.Persona(nombre=nombre,apellido=apellido,edad=edad,dpi=dpi,telefono=telefono,direccion=direccion,trabajo=trabajo,salario=salario,created_by=creador)

    try:
        db.session.add(new_persona)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        abort(500, f'Error al guardar la persona: {str(e)}')
    return new_persona.id_persona, new_persona.salario

def borrar_persona(id):
    persona = Persona.Persona.query.get(id)
    if persona is None:
        abort(400, f'No existe la persona con id: {id}')

    try:
        db.session.delete(persona)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        abort(500, f'Error al borrar la persona: {str(e)}')

    return jsonify({"message": f"La persona {id} borrada con exito"}), 200