from flask import current_app
from flask_mail import Message
from screen_rekod import mail
from dotenv import load_dotenv
from threading import Thread

load_dotenv(".env")

def send_async_email(*args):
    """
    Asynchronously send an email using Flask-Mail within the application context.
    """
    with current_app.app_context():
        mail.send(args[0])

def send_email(subject, sender, recipients, text_body, html_body):
    """
    Send an email using Flask-Mail in a separate thread to avoid blocking the main thread.
    Args:
    subject: Subject of the email.
    sender: Sender's email address.
    recipients: List of recipients' email addresses.
    text_body: Plain text body of the email.
    html_body: HTML body of the email.
    """
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(msg,)).start()
