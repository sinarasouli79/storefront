from store.signals import order_created
from django.dispatch import receiver


@receiver(order_created)
def on_order_created(sender, **kwargs):
    print('*****************sender*****************')
    print(sender)
    print()
    print('*****************kwargs*****************')
    print(kwargs)
    print()
