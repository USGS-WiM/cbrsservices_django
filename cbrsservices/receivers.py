import os
import hashlib
import base64
from django.core.mail import send_mail, EmailMessage
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete, post_delete
from cbrsservices import models


def _get_hash(id):
    """Returns a hash of a portion of the string of the id of the record"""
    algorithm = "sha256"
    value = str(id)
    salt = "CBRS"
    # keylength = random.randint(10000, 99999)
    keylength = 99999
    key = hashlib.pbkdf2_hmac(algorithm, value.encode(), salt.encode(), keylength)
    keyhash = base64.b16encode(key).decode()[-8:]
    return keyhash


# listen for new case instances, then create the case hash (public ID) and send a confirmation email
@receiver(post_save, sender=models.Case)
def case_post_save(sender, **kwargs):
    case = kwargs['instance']
    local_email_address = "CBRAdeterminations@fws.gov"
    cbrs_email_address = "CBRAdeterminations@fws.gov"
    other_cbrs_email_addresses = ["CBRA@fws.gov", ]

    if kwargs['created']:
        # create and assign the case ID hash
        case.case_reference = _get_hash(case.id)
        case.save()

        # construct and send the confirmation email
        subject = "Coastal Barrier Resources Act Determination Request Received"
        body = "Dear Requester,\r\n\r\nThe U.S. Fish and Wildlife Services has received your request."
        body += "\r\nThe Reference Number is: " + case.case_reference
        from_address = local_email_address
        to_addresses_list = [case.requester.email, ]
        bcc_addresses_list = other_cbrs_email_addresses
        reply_to_list = [cbrs_email_address, ]
        headers = None  # {'Message-ID': 'foo'}
        # send_mail(subject, message, from_address, to_addresses_list, fail_silently=False)
        email = EmailMessage(subject, body, from_address, to_addresses_list, bcc_addresses_list,
                             reply_to=reply_to_list, headers=headers)
        #email.send(fail_silently=False)

    elif case.final_letter_date is not None:

        # construct and send the final email with the final letter as attachment
        subject = "Coastal Barrier Resources Act Determination Case " + case.case_reference
        body = "Dear Requester,\r\n\r\nAttached is the Coastal Barrier Resources Act determination that you requested"
        body += " from the U.S. Fish and Wildlife Service. If you have any questions about this determination,"
        body += " please contact Teresa Fish, Program Specialist, at (703) 358-2171 or e-mail us at cbra@fws.gov."
        from_address = cbrs_email_address
        to_addresses_list = [case.requester.email, ]
        bcc_addresses_list = other_cbrs_email_addresses
        reply_to_list = [cbrs_email_address, ]
        headers = None  # {'Message-ID': 'foo'}
        attachments = []
        if hasattr(case, 'casefiles'):
            for casefile in case.casefiles:
                if casefile.final_letter:
                    attachments.append(casefile)
                    break
        # send_mail(subject, message, from_address, to_addresses_list, fail_silently=False)
        email = EmailMessage(subject, body, from_address, to_addresses_list, bcc_addresses_list,
                             reply_to=reply_to_list, headers=headers, attachments=attachments)
        #email.send(fail_silently=False)


# listen for new or updated system map instances, then toggle the 'effective' value on all system maps with same name
@receiver(post_save, sender=models.SystemMap)
def systemmap_post_save(sender, **kwargs):
    systemmap = kwargs['instance']

    if kwargs['created']:
        if systemmap:
            homonym_systemmaps = models.SystemMap.objects.filter(map_number__exact=systemmap.map_number)
            for homonym_systemmap in homonym_systemmaps:
                if homonym_systemmap.effective:
                    homonym_systemmap.effective = False
                    homonym_systemmap.save(update_fields=['effective'])


# listen for tag deletes, and only allow when the tag is not used by any cases
@receiver(pre_delete, sender=models.Tag)
def tag_pre_delete(sender, **kwargs):
    tag = kwargs['instance']
    casetags = models.CaseTag.objects.filter(tag__exact=tag.id)
    if len(casetags) > 0:
        # raise ValidationError("This tag cannot be removed because it is assigned to one or more determination cases.")
        models.CaseTag.objects.filter(tag__exact=tag.id).delete()


# listen for casefile deletes, and delete the actual file from the physical storage
@receiver(post_delete, sender=models.CaseFile)
def casefile_post_delete(sender, **kwargs):
    casefile = kwargs['instance']

    if casefile.file:
        if os.path.isfile(casefile.file.path):
            os.remove(casefile.file.path)


# listen for system unit deletes, and delete all many-to-many relations
@receiver(pre_delete, sender=models.SystemUnit)
def systemunit_pre_delete(sender, **kwargs):
    systemunit = kwargs['instance']
    systemunitmaps = models.SystemUnitMap.objects.filter(system_unit__exact=systemunit.id)
    if len(systemunitmaps) > 0:
        models.SystemUnitMap.objects.filter(system_unit__exact=systemunit.id).delete()


# listen for system map deletes, and delete all many-to-many relations
@receiver(pre_delete, sender=models.SystemMap)
def systemmap_pre_delete(sender, **kwargs):
    systemmap = kwargs['instance']
    systemunitmaps = models.SystemUnitMap.objects.filter(system_map__exact=systemmap.id)
    if len(systemunitmaps) > 0:
        models.SystemUnitMap.objects.filter(system_map__exact=systemmap.id).delete()
