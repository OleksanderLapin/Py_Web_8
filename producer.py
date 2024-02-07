from faker import Faker
from pymongo.errors import ConnectionFailure
import pika
import json
from models import Contact
import connect

# Підключаємося до RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='contact_queue')

# Функція для генерації фейкових контактів
def generate_fake_contacts(num_contacts):
    fake = Faker()
    contacts = []
    for _ in range(num_contacts):
        contact = {
            'full_name': fake.name(),
            'email': fake.email(),
            'contacted': False
        }
        contacts.append(contact)
    return contacts

# Функція для запису контактів у базу даних та розміщення повідомлення в черзі
def process_contacts(contacts):
    for contact in contacts:
        # Записуємо контакт у базу даних
        new_contact = Contact(**contact)
        new_contact.save()

        # Розміщуємо повідомлення в черзі RabbitMQ
        message = {'contact_id': str(new_contact.id)}
        channel.basic_publish(exchange='', routing_key='contact_queue', body=json.dumps(message))
        print("Sent message:", message)

# Генеруємо фейкові контакти
num_contacts = 10
fake_contacts = generate_fake_contacts(num_contacts)

# Обробляємо контакти
process_contacts(fake_contacts)

# Закриваємо з'єднання з RabbitMQ
connection.close()