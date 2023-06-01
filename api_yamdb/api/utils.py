from django.core.mail import EmailMessage
from threading import Thread


class EmailThread(Thread):
    def __init__(self, email):
        self.email = email
        Thread.__init__(self)

    def run(self):
        self.email_send()


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            to=data['to_email'],
        )
        EmailThread(email=email).start()
