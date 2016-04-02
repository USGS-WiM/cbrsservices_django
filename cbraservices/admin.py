from django.contrib import admin
from django import forms
from cbraservices.models import *
#from db_file_storage.form_widgets import DBAdminClearableFileInput


# class CaseFileForm(forms.ModelForm):
#     class Meta:
#         model = CaseFile
#         exclude = []
#         widgets = {
#             'picture': DBAdminClearableFileInput
#         }
#
#
# class CaseFileAdmin(admin.ModelAdmin):
#     form = CaseFileForm


admin.site.register(Case, SimpleHistoryAdmin)
admin.site.register(CaseFile, SimpleHistoryAdmin)
admin.site.register(Property, SimpleHistoryAdmin)
admin.site.register(Requester, SimpleHistoryAdmin)
admin.site.register(CaseTag, SimpleHistoryAdmin)
admin.site.register(Tag, SimpleHistoryAdmin)
admin.site.register(Comment, SimpleHistoryAdmin)
admin.site.register(Determination, SimpleHistoryAdmin)
admin.site.register(SystemUnit, SimpleHistoryAdmin)
admin.site.register(SystemUnitProhibitionDate, SimpleHistoryAdmin)
admin.site.register(SystemMap, SimpleHistoryAdmin)
admin.site.register(FieldOffice, SimpleHistoryAdmin)