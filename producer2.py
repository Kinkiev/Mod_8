import json
import random
import string
import pika
from mongoengine import connect, Document, StringField, BooleanField
from models import Contact
import connect


# З'єднання з RabbitMQ
credentials = pika.PlainCredentials("guest", "guest")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials)
)
channel = connection.channel()
channel.queue_declare(queue="contacts")

# Генерація фейкових контактів, запис до бази та надсилання в чергу
for _ in range(10):
    full_name = "".join(random.choice(string.ascii_letters) for _ in range(8))
    email = f"{full_name}@example.com"
    contact = Contact(full_name=full_name, email=email)
    contact.save()
    message = json.dumps({"contact_id": str(contact.id)})
    channel.basic_publish(exchange="", routing_key="contacts", body=message)

print("Контакти створено та відправлено в чергу")

connection.close()
