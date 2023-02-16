import json
import pika
from pika.exceptions import AMQPConnectionError
import django
import os
import sys
import time
from django.core.mail import send_mail


sys.path.append("")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "presentation_mailer.settings")
django.setup()

while True:
    try:
        parameters = pika.ConnectionParameters(host="rabbitmq")
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.queue_declare(queue="process_approval")
        channel.queue_declare(queue="process_rejection")


        def process_approval(ch, method, properties, body):
            content = json.loads(body)
            presenter_email = content["presenter_email"]
            presenter_name = content["presenter_name"]
            presentation_title = content["title"]

            send_mail(
                "Your presentation has been accepted",
                f"{presenter_name}, we're happy to tell you that your presentation {presentation_title} has been accepted.",
                "admin@conference.go",
                [presenter_email],
                fail_silently=False,
            )


        def process_rejection(ch, method, properties, body):
            content = json.loads(body)
            presenter_email = content["presenter_email"]
            presenter_name = content["presenter_name"]
            presentation_title = content["title"]

            send_mail(
                "Your presentation has been rejected",
                f"We're sorry, {presenter_name}, but your presentation {presentation_title} has been rejected.",
                "admin@conference.go",
                [presenter_email],
                fail_silently=False,
            )


        channel.basic_consume(
            queue="process_approval",
            on_message_callback=process_approval,
            auto_ack=True,
        )
        channel.basic_consume(
            queue="process_rejection",
            on_message_callback=process_rejection,
            auto_ack=True,
        )
        channel.start_consuming()
    except AMQPConnectionError:
        print("Could not connect to RabbitMQ")
        time.sleep(2.0)
