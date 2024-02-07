import pika
import json
from time import sleep
from models import Contact

# Підключення до RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='contact_queue')

# Функція-заглушка для надсилання повідомлення по email
def send_email(contact):
    # Логіка надсилання повідомлення по email
    print("Sending email to", contact['email'])
    # Оновлення логічного поля для контакту
    contact['contacted'] = True
    print("Contact updated:", contact)

# Метод, який викликається при отриманні повідомлення з черги
def callback(ch, method, properties, body):
    message = json.loads(body)
    contact_id = message['contact_id']

    # Отримання контакту з бази даних за його ID
    contact = Contact.objects.get(id=contact_id)

    # Виклик функції для надсилання повідомлення по email та оновлення контакту
    send_email(contact)

    # Підтвердження обробки повідомлення
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Встановлення максимальної кількості повідомлень, яку можна обробляти одночасно
channel.basic_qos(prefetch_count=1)

# Встановлення методу-слухача для черги
channel.basic_consume(queue='contact_queue', on_message_callback=callback)

# Нескінченний цикл очікування повідомлень з черги
print('Waiting for emails...') 
channel.start_consuming()