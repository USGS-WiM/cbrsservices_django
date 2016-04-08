import hashlib
import base64
from django.core.mail import send_mail
from django.dispatch import receiver
from django.db.models.signals import post_save
from cbraservices import models


def _get_hash(id):
    """Returns a hash of a portion of the string of the id of the record"""
    algorithm = "sha256"
    value = str(id)
    salt = "CBRA"
    # keylength = random.randint(10000, 99999)
    keylength = 99999
    key = hashlib.pbkdf2_hmac(algorithm, value.encode(), salt.encode(), keylength)
    keyhash = base64.b16encode(key).decode()[-8:]
    return keyhash


# listen for new instances, then create the case hash (public ID) and send a confirmation email
@receiver(post_save, sender=models.Case)
def case_post_save(sender, **kwargs):
    if kwargs['created']:
        case = kwargs['instance']
        case.case_hash = _get_hash(case.id)
        case.save()

        # TODO: send email confirmation!
        # https://docs.djangoproject.com/en/1.8/topics/email/
        # Mail is sent using the SMTP host and port specified in the EMAIL_HOST and EMAIL_PORT settings.
        # The EMAIL_HOST_USER and EMAIL_HOST_PASSWORD settings, if set, are used to authenticate to the SMTP server,
        # and the EMAIL_USE_TLS and EMAIL_USE_SSL settings control whether a secure connection is used.

        subject = "CBRA Determination Request Confirmation"
        message = "Your request has been submitted. Here is your case ID: " + case.case_hash
        from_address = "astephensonusgs@gmail.com"
        to_addresses_list = ["astephenson@usgs.gov"]
        send_mail(subject, message, from_address, to_addresses_list, fail_silently=False)
