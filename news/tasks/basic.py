from django.template.loader import render_to_string
from django.core.mail.message import EmailMultiAlternatives
from django.conf import settings


def get_subscriber(category):
    user_email = []
    for user in category.subscribers.all():
        user_email.append(user.email)
    return user_email


def new_post_subscription(instance):  # вызывается в signals.py
    template = 'mail/new_post.html'  # шаблон

    for category in instance.postCategory.all():
        email_subject = f'Новый пост в категории: "{category}"'
        user_emails = get_subscriber(category)

        html = render_to_string(
            template_name=template,
            context={
                'category': category,
                'post': instance,
            },
        )
        msg = EmailMultiAlternatives(
            subject=email_subject,
            text_content = 'Простой текст письма'
            from_email=settings.DEFAULT_FROM_EMAIL,
            to_email= user_emails,
        )

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        msg.attach_alternative(html, 'text/html')
        msg.send()
