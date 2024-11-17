from config import get_pika_connection
from services import data_record
from app import app

def on_message_received(ch, method, properties, body):
    message = body.decode('utf-8')
    app.logger.info(f"received new message: {message}")
    with app.app_context():
        data_record.data_record(message)

def main():
    channel = get_pika_connection()
    if channel:
        channel.queue_declare(queue='cola', durable=True)
        channel.basic_consume(queue='cola', auto_ack=True, on_message_callback=on_message_received)
        print("Starting Consuming")

        try:
            channel.start_consuming()
        finally:
            channel.connection.close()
    else:
        print("No se pudo establecer la conexión con RabbitMQ")