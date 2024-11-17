import pika
from config import get_pika_connection

def sms_sender(tarjeta_credito, tipo_trans, monto, lugar, hora, enviado_por):
    num_tc = tarjeta_credito.numero_tc
    channel, conexion = get_pika_connection()

    channel.queue_declare(queue='cola', durable=True)

    message = (f"{num_tc}|{tipo_trans}|{monto}|{lugar}|{hora}|{enviado_por}|")

    channel.basic_publish(exchange='', routing_key='cola', body=message, properties=pika.BasicProperties(delivery_mode=2))

    print(f"sent message: {message}")

    channel.close()
    conexion.close()