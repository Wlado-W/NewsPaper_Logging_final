from django.shortcuts import render

# Create your views here.
from django.shortcuts import reverse, redirect
from django.views import View
from datetime import datetime
from .models import Appointment

# для рассылок на почту
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives  # импортируем класс для создание объекта письма с html
from django.core.mail import mail_admins  # импортируем функцию для массовой отправки писем админам
from django.template.loader import render_to_string  # импортируем функцию, которая срендерит наш html в текст

# [D6.4. Отправка электронных писем по событию, знакомство с сигналами
# python manage.py runapscheduler
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import mail_managers
from .models import Appointment


# создаём функцию обработчик с параметрами под регистрацию сигнала
def notify_managers_appointment(sender, instance, created, **kwargs):
    # subject = f'{instance.client_name} {instance.date.strftime("%d %m %Y")}'

    mail_managers(
        subject=f'{instance.client_name} {instance.date.strftime("%d %m %Y")}',
        message=instance.message,
    )
    print(f'{instance.client_name} {instance.date.strftime("%d %m %Y")}')


# коннектим наш сигнал к функции обработчику и указываем, к какой именно модели после сохранения привязать функцию
post_save.connect(notify_managers_appointment, sender=Appointment)


# D6.4. Отправка электронных писем по событию, знакомство с сигналами ]


class AppointmentView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'make_appointment.html', {})

    def post(self, request, *args, **kwargs):
        appointment = Appointment(
            date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
            client_name=request.POST['client_name'],
            message=request.POST['message'],
        )
        appointment.save()


        mail_admins(
            subject=f'{appointment.client_name} {appointment.date.strftime("%d %m %Y")}',
            message=appointment.message,
        )

        return redirect('appointments:make_appointment')

