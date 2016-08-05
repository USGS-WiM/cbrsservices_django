from rest_framework import renderers
from docx import *
from io import BytesIO


from rest_framework import renderers
from docx import *
from io import BytesIO


class DOCXRenderer(renderers.BaseRenderer):
    media_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    format = 'docx'
    render_style = 'binary'
    document = None #This should be a docx object

    def render(self, data, media_type=None, renderer_context=None):
        return self.document


class FinalLetterDOCXRenderer(DOCXRenderer):

    def render(self, data, media_type=None, renderer_context=None):
        id = str(data[0]['id'])
        case_hash = data[0]['case_hash'] or ""
        determination = data[0]['determination'] or ""
        determination_string = data[0]['determination_string'] or ""
        cbrs_unit = data[0]['cbrs_unit_string'] or ""
        system_unit_type = data[0]['system_unit_type'] or ""
        prohibition_date = data[0]['prohibition_date'] or ""

        if determination == 1:
            content = "This property is within " + system_unit_type + " Unit " + cbrs_unit \
                      + ".  The prohibition date on Federal flood insurance is " + prohibition_date + "."
        elif determination == 2:
            content = "This property is not located within a System unit or an OPA of the CBRS."
        elif determination == 3:
            content = "This property is partially located within " + system_unit_type + " Unit " + cbrs_unit \
                      + ".  The existing structure located on the property is within Unit " + cbrs_unit \
                      + ".  The prohibition date on Federal flood insurance is " + prohibition_date + "."
        elif determination == 4:
            content = "This property is partially located within " + system_unit_type + " Unit " + cbrs_unit \
                      + ".  The existing structure located on the property is not within Unit " + cbrs_unit + "."
        elif determination == 5:
            content = "This property is partially located within " + system_unit_type + " Unit " + cbrs_unit \
                      + ".  There is no existing structure located on the property." \
                      + "The prohibition date on Federal flood insurance is " + prohibition_date + "."
        else:
            content = "A determination has not been made."

        document = Document()

        document.add_paragraph("Case: " + case_hash + " (" + id + ")")
        document.add_paragraph("Determination: " + determination_string)
        document.add_paragraph(content)
        document.add_paragraph()

        docx_buffer = BytesIO()
        document.save(docx_buffer)
        docx_buffer.seek(0)
        self.document = docx_buffer

        return super(FinalLetterDOCXRenderer, self).render(data, media_type, renderer_context)


# class FinalLetterDOCXRenderer(renderers.BaseRenderer):
#     media_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
#     format = 'docx'
#     render_style = 'binary'
#
#     def render(self, data, media_type=None, renderer_context=None):
#         document = Document()
#
#         document.add_paragraph('Case Distance: ' + str(data[0]['distance']))
#         document.add_paragraph()
#         document.add_paragraph('Dear Sir or Madam:')
#         document.add_paragraph('We are pleased to help you with your widgets.')
#         document.add_paragraph('Please feel free to contact me for any additional information.')
#         document.add_paragraph('I look forward to assisting you in this project.')
#
#         document.add_paragraph()
#         document.add_paragraph('Best regards,')
#         document.add_paragraph('Acme Specialist 1]')
#         document.add_page_break()
#
#         docx_buffer = BytesIO()
#         document.save(docx_buffer)
#         docx_buffer.seek(0)
#
#         return docx_buffer
