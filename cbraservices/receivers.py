import hashlib
import base64
from django.core.mail import send_mail, EmailMessage
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

        # create and assign the case ID hash
        case = kwargs['instance']
        case.case_hash = _get_hash(case.id)
        case.save()

        # TODO: finalize the email settings (message text, addresses, etc)
        # construct and send the confirmation email
        # subject = "CBRA Determination Request Confirmation"
        # body = "Your request has been submitted. Here is your case ID: " + case.case_hash
        # from_address = "admin@cbra.fws.gov"
        # to_addresses_list = [case.requester.email, ]
        # bcc_addresses_list = ["astephenson@usgs.gov", ]
        # reply_to_list = None
        # headers = None  # {'Message-ID': 'foo'}
        # #send_mail(subject, message, from_address, to_addresses_list, fail_silently=False)
        # email = EmailMessage(subject, body, from_address, to_addresses_list, bcc_addresses_list, reply_to_list, headers)
        # email.send(fail_silently=False)
