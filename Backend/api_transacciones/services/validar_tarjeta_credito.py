from flask import abort
from models import Tarjeta_credito
from app import app

def validar_tc(numero_tc, cvv_tc, fech_exp_tc):
    with app.app_context():
        # validacion de numero de tarjeta de credito
        tarjeta_credito = Tarjeta_credito.Tarjeta_credito.query.filter_by(numero_tc=numero_tc).first()

        if not tarjeta_credito:
            abort(404, 'Numero de tarjeta no encontrada')

        # validacion de codigo de seguridad
        if not cvv_tc:
            abort(404, 'Se requiere numero de cvv')
        if tarjeta_credito.cvv_tc != cvv_tc:
            abort(404, 'Numero de cvv no coincide')

        # validacion fecha de expiracion
        if not fech_exp_tc:
            abort(404, 'Fecha de expiracion no encontrada')


        if fech_exp_tc != tarjeta_credito.fech_exp_tc:
            abort(404, f'Fecha invalida  {tarjeta_credito.fech_exp_tc}, {fech_exp_tc}')



        if tarjeta_credito.id_estado != 4:
            abort(404, 'La tarjeta de credito no se encuentra activa')

        return tarjeta_credito