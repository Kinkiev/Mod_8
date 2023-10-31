import json
import pika
from mongoengine import connect
from models import Contact
import connect

credentials = pika.PlainCredentials("guest", "guest")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials)
)
channel = connection.channel()
channel.queue_declare(queue="contacts")


def send_email(contact_id):
    # Встановити логічне поле для контакту в True
    contact = Contact.objects(id=contact_id).first()
    if contact:
        contact.message_sent = True
        contact.save()


def callback(ch, method, properties, body):
    message = json.loads(body)
    contact_id = message.get("contact_id")
    if contact_id:
        print(f"Отримано повідомлення для контакту з ID {contact_id}")
        send_email(contact_id)


channel.basic_consume(queue="contacts", on_message_callback=callback, auto_ack=True)

print("Очікування повідомлень... Для виходу натисніть CTRL+C")
channel.start_consuming()
