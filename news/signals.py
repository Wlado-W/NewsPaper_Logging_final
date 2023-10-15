from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from .models import PostCategory
from .tasks.basic import new_post_subscription
from django.db.models.signals import m2m_changed


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
