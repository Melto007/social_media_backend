from django.core.mail import send_mail
from rest_framework import exceptions

def send_email(url, email):
    try:
        res = send_mail(
            "Reset Your Password",
            "<a href='%s'>Click here</a> to reset your password" % url,
            "from@example.com",
            [email],
            fail_silently=False,
        )
        return res
    except Exception as e:
        raise exceptions.APIException('email not send', e.args)