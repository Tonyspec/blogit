# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string 

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        email = EmailMessage(
            'Welcome to Our Site!',
            render_to_string('welcome_email.html', {'user': instance}),
            'testerbender0131@gmail.com',
            [instance.email]
        )
        email.content_subtype = "html"
        email.send()