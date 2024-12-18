from better_profanity import profanity
from django.conf import settings
from django.core.mail import send_mail


def check_swearing(text: str) -> bool:
    """
    Check if the given text contains any profanity.

    Args:
        text (str): The text to be checked for profanity.

    Returns:
        bool: True if the text contains profanity, False otherwise.
    """
    try:
        return bool(profanity.contains_profanity(text))
    except Exception as e:
        print(f"Error while checking profanity: {e}")
        return False


def send_custom_email(subject: str, message: str) -> None:
    """
    Send an email with the given subject and message to a predefined recipient.

    Args:
        subject (str): The subject of the email.
        message (str): The body of the email.

    Raises:
        Exception: If the email fails to send.
    """
    from_email: str = settings.DEFAULT_FROM_EMAIL
    recipient_list: list[str] = ['danya.tkachenko.1997@gmail.com']

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False,
        )
        print("Email sent successfully.")
    except Exception as e:
        print(f"Error while sending email: {e}")