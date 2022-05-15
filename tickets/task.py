from time import sleep

from celery import shared_task
from django.core.mail import send_mail


@shared_task
def sleepy(duration):
    sleep(duration)
    return None


@shared_task
def send_email_task_befor_response(email):
    send_mail('Support',
              'Ваша проблема добавлена',
              'aks8slava@mail.ru',
              [email])

    return None

@shared_task
def send_email_task_after_response(email):
    send_mail('Support',
              'Ваша проблема решена',
              'aks8slava@mail.ru',
              [email])

    return None