import os
from django.core.mail import send_mail
from mailings.models import Mailing, DeliveryStatus


def send_email(mailing: Mailing):
    """
    Отправка письма всем подписчикам рассылки с логированием попыток.
    """
    for subscriber in mailing.subscribers.all():
        try:
            send_mail(
                subject=mailing.message.subject,
                message=mailing.message.content,
                from_email=os.getenv("EMAIL_HOST"),
                recipient_list=[subscriber.email],
                fail_silently=False,
            )
            DeliveryStatus.objects.create(
                mailing=mailing, status="success", server_response="OK"
            )
        except Exception as e:
            DeliveryStatus.objects.create(
                mailing=mailing, status="failed", server_response=str(e)
            )

    mailing.save()
