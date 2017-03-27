import os
import hashlib
import base64
from django.core.mail import send_mail, EmailMessage
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete, post_delete
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


# listen for new case instances, then create the case hash (public ID) and send a confirmation email
@receiver(post_save, sender=models.Case)
def case_post_save(sender, **kwargs):
    case = kwargs['instance']
    cbra_email_address = "cbra@fws.gov"
    other_cbra_email_addresses = ["astephenson@usgs.gov", ]

    if kwargs['created']:
        # create and assign the case ID hash
        case.case_reference = _get_hash(case.id)
        case.save()

        # TODO: finalize the email settings (message text, addresses, etc)
        # construct and send the confirmation email
        subject = "Coastal Barrier Resources Act Determination Request Received"
        body = "Dear Requester,\r\n\r\nThe U.S. Fish and Wildlife Services has received your request."
        body += "\r\nThe Reference Number is: " + case.case_reference
        from_address = cbra_email_address
        to_addresses_list = [case.requester.email, ]
        bcc_addresses_list = other_cbra_email_addresses
        reply_to_list = [cbra_email_address, ]
        headers = None  # {'Message-ID': 'foo'}
        #send_mail(subject, message, from_address, to_addresses_list, fail_silently=False)
        email = EmailMessage(subject, body, from_address, to_addresses_list, bcc_addresses_list,
                             reply_to=reply_to_list, headers=headers)
        email.send(fail_silently=False)

    elif case.final_letter_date is not None:

        # TODO: finalize the email settings (message text, addresses, etc)
        # construct and send the final email with the final letter as attachment
        subject = "Coastal Barrier Resources Act Determination Case " + case.case_reference
        body = "Dear Requester,\r\n\r\nAttached is the Coastal Barrier Resources Act determination that you requested"
        body += " from the U.S. Fish and Wildlife Service. If you have any questions about this determination,"
        body += " please contact Teresa Fish, Program Specialist, at (703) 358-2171 or e-mail us at cbra@fws.gov."
        from_address = cbra_email_address
        to_addresses_list = [case.requester.email, ]
        bcc_addresses_list = other_cbra_email_addresses
        reply_to_list = [cbra_email_address, ]
        headers = None  # {'Message-ID': 'foo'}
        attachments = []
        for casefile in case.casefiles:
            if casefile.final_letter:
                attachments.append(casefile)
                break
        #send_mail(subject, message, from_address, to_addresses_list, fail_silently=False)
        email = EmailMessage(subject, body, from_address, to_addresses_list, bcc_addresses_list,
                             reply_to=reply_to_list, headers=headers, attachments=attachments)
        email.send(fail_silently=False)


# listen for tag deletes, and only allow when the tag is not used by any cases
@receiver(pre_delete, sender=models.Tag)
def tag_pre_delete(sender, **kwargs):
    tag = kwargs['instance']
    casetags = models.CaseTag.objects.all().filter(tag__exact=tag.id)
    if casetags.length > 0:
        #raise ValidationError("This tag cannot be removed because it is assigned to one or more determination cases.")
        models.CaseTag.objects.all().filter(tag__exact=tag.id).delete()


# listen for casefile deletes, and delete the actual file from the physical storage
@receiver(post_delete, sender=models.CaseFile)
def casefile_post_delete(sender, **kwargs):
    casefile = kwargs['instance']
    print(casefile)

    if casefile.file:
        print(casefile.file)
        if os.path.isfile(casefile.file.path):
            print(casefile.file.path)
            os.remove(casefile.file.path)
