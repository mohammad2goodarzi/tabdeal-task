from django.dispatch import receiver
from django_fsm import post_transition

from salesman.models import CreditRequest


@receiver(post_transition, sender=CreditRequest)
def save_new_state_transition(
        sender,
        instance,
        name,
        source,
        target,
        **kwargs):
    # new state won't be saved automatically
    instance.save()
