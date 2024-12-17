from better_profanity import profanity
from django.conf import settings
from django.core.mail import send_mail


def check_swearing(text: str) -> bool:
    """
    Checks if the given text contains any profanity.
    """
    return bool(profanity.contains_profanity(text))


def send_custom_email(subject, message):
    from_email = settings.DEFAULT_FROM_EMAIL

    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=['danya.tkachenko.1997@gmail.com'],
        fail_silently=False,
    )
