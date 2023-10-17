from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from .models import PostCategory
from .tasks.basic import new_post_subscription
from django.db.models.signals import m2m_changed
from django.core.mail import send_mail


@receiver(post_save, sender=User)
def add_to_common_group(sender, instance, created, **kwargs):
    if created:
        common_group, created = Group.objects.get_or_create(name='common')
        common_group.user_set.add(instance)




@receiver(m2m_changed, sender=PostCategory)
def notify_subscribers(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        pass
        new_post_subscription(instance)

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        subject = 'Добро пожаловать в наше приложение'
        message = 'Здравствуйте, спасибо за регистрацию в нашем приложении. Надеемся, вам здесь понравится!'
        from_email = 'vasiliygolicin@yandex.ru'  # Замените на вашу электронную почту
        recipient_list = [instance.email]

        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
