class ModelFieldDescriptions:
    def __init__(self, field_name_list):
        for k, v in field_name_list.items():
            setattr(self, k, v)


case = ModelFieldDescriptions({
    'case_reference': 'An alphanumeric value of the case reference',
    'duplicate': 'An integer value that indicates the case number of the original case if this case is a duplicate',
    'request_date': 'The date the request for this case was submitted in "YYYY-MM-DD" format',
    'requester': 'A foreign key integer value identifying the person who submitted the case request',
    'property': 'A foreign key integer value identifying the property this case represents',
    'cbrs_unit': 'A foreign key integer value identifying the cbrs unit closest to/containing the property',
    'map_number': 'A foreign key integer value identifying a system map containing the property',
    'cbrs_map_date': 'The system map date in "YYYY-MM-DD" format',
    'determination': 'A foreign key integer value identifying the determination of the property',
    'prohibition_date': 'The flood insurance prohibition date in "YYYY-MM-DD" format',
    'distance': 'A numeric value representing the distance the property is from a system unit',
    'fws_fo_received_date': 'The date the field office received the request in "YYYY-MM-DD" format',
    'fws_hq_received_date': 'The date the headquarters received the request in "YYYY-MM-DD" format',
    'final_letter_date': 'The final letter date in "YYYY-MM-DD" format',
    'close_date': 'The date the case was closed in "YYYY-MM-DD" format',
    'final_letter_recipient': 'An alphanumeric value of the full name of the final letter recepient',
    'analyst': 'A foreign key integer value identifying the user who analyzed the case',
    'analyst_signoff_date': 'The date the analyst signed off in "YYYY-MM-DD" format',
    'qc_reviewer': 'A foreign key integer value identifying the QC reviewer',
    'qc_reviewer_signoff_date': 'The date the QC reviewer signed off in "YYYY-MM-DD" format',
    'fws_reviewer': 'A foreign key integer value identifying the FWS reviewer',
    'fws_reviewer_signoff_date': 'The date the FWS reviewer signed off in "YYYY-MM-DD" format',
    'priority': 'A boolean value (True/False) indicating if the case is a priority',
    'on_hold': 'A boolean value (True/False) indicating if the case is on hold',
    'invalid': 'A boolean value (True/False) indicating if the case is invalid',
    'hard_copy_map_reviewed': 'A boolean value (True/False) indicating if the hard copy of the system map has been reviewed',
    'tags': 'A many to many relationship of tags based on a foreign key integer value identifying a tag',
    'analyst_string': "An alphanumeric value of the analyst's username",
    'qc_reviewer_string': "An alphanumeric value of the QC reviewer's username",
    'property_string': 'An alphanumeric value of the combined string of the property address',
    'tags': 'A comma-separated list of the tags for the given case',
    'comments': 'A comma-separated list of the comments for the given case',
    'status': 'An alphanumeric value representing the status of this case (e.g. "Final", "Awaiting QC", etc)',
    'case_number': 'A numeric value representing the case number'
})

casefile = ModelFieldDescriptions({
    'file': 'An alphanumeric value of the file path of the uploaded file, which is used to find the file name',
    'case': 'A foreign key integer value identifying the case',
    'from_requester': 'A boolean value (True/False) indicating if the file is from the requester',
    'final_letter': 'A boolean value (True/False) indicating if the file is the final letter',
    'uploader': 'A foreign key integer value identifying the user uploading the file',
    'uploaded_date': 'The date the file was uploaded in "YYYY-MM-DD" format'    
})

address = ModelFieldDescriptions({
    'legal_description': 'An alphanumeric value of the legal description of the property',
    'subdivision': 'An alphanumeric value of the subdivision name of the property',
    'policy_number': 'An alphanumeric value of the policy number of the property',
    'street': 'An alphanumeric value of the street name of this address',
    'unit': 'An alphanumeric value of the unit at which this address is located',
    'city': 'An alphanumeric value of the city in which this address is located',
    'state': 'An alphanumeric value of the state in which this address is located',
    'zipcode': 'An alphanumeric value of the zipcode at which this address is located'
})

requester = ModelFieldDescriptions({
    'salutation': 'An alphanumeric value of the preferred salutation of the requester',
    'first_name': "An alphanumeric value of the requester's first name",
    'last_name': "An alphanumeric value of the requester's last name",
    'organization': "An alphanumeric value of the requester's organization",
    'email': "An alphanumeric value of the requester's email"
})

casetag = ModelFieldDescriptions({
    'case': 'A foreign key integer value identifying a case',
    'tag': 'A foreign key integer value identifying a tag',
    'name': 'An alphanumeric value of the tag name',
    'description': 'An alphanumeric value of the tag description'
})

casecomment = ModelFieldDescriptions({
    'comment': 'An alphanumeric value of the comment',
    'acase': 'A foreign key integer value identifying a case'
})

casedetermination = ModelFieldDescriptions({
    'determination': 'An alphanumeric value indicating the determination value',
    'description': 'An alphanumeric value of a description of the determination'
})

systemunit = ModelFieldDescriptions({
    'system_unit_number': 'An alphanumeric value of the system unit number',
    'system_unit_name': 'An alphanumeric value of the system unit name',
    'system_unit_type': 'A foreign key integer value identifying the system unit type',
    'field_office': 'A foreign key integer value identifying a field office',
    'system_maps': 'A many to many relationship of system maps based on a foreign key integer value identifying a system map',
    'unit_type': 'A foreign key integer value identifying the system unit type',
    'unit_type_string': 'An alphanumeric value of the system unit type'
})

prohibitiondate = ModelFieldDescriptions({
    'prohibition_date': 'The flood insurance prohibition date in "YYYY-MM-DD" format',
    'system_unit': 'A foreign key integer value identifying the system unit the prohibition was placed on',
    'prohibition_date_mdy': 'The flood insurance prohibition date in "MM/DD/YYYY" format'
})

systemunitmap = ModelFieldDescriptions({
    'system_unit': 'A foreign key integer value identifying a system unit',
    'system_map': 'A foreign key integer value identifying a system map',
    'map_number': 'An alphanumeric value of the system map number',
    'map_title': 'An alphanumeric value of the title of the system map',
    'map_date': 'The system map date in "YYYY-MM-DD" format',
    'effective': 'A boolean value (True/False) indicating if the map is effective'
})

fieldoffice = ModelFieldDescriptions({
    'field_office_number': 'An alphanumeric value indicating the field office number',
    'field_office_name': 'An alphanumeric value of the name of the field office',
    'field_agent_name': 'An alphanumeric value of the name of the agent representing the field office',
    'field_agent_email': "An alphanumeric value of the field office agent's email",
    'city': 'An alphanumeric value of the city where the field office is located',
    'state': 'An alphanumeric value of the state in which the field office is located'
})

history = ModelFieldDescriptions({
    'created_date': 'The date this object was created in "YYYY-MM-DD" format',
    'created_by': 'A foreign key integer value identifying the user who created the object',
    'modified_date': 'The date this object was last modified in "YYYY-MM-DD" format',
    'modified_by': 'A foreign key integer value identifying the user who last modified the object',
    'created_by_string': 'An alphanumeric value of the username of the user who created this object',
    'modified_by_string': 'An alphanumeric value of the username of the user who last modified this object'
})

user = ModelFieldDescriptions({
    'password': "An alphanumeric value of the user's password",
    'is_superuser': 'A boolean value (True/False) indicating if the user is a superuser',
    'username': "An alphanumeric value of the user's password",
    'is_active': 'A boolean value (True/False) indicating if the user is active'
})

queryparams = ModelFieldDescriptions({
    'format': 'An alphanumeric value of the desired format of the document (e.g. "docx" or "csv")',
    'view': 'An alphanumeric value of the view (e.g. "workbench", "report" or "caseid")',
    'request_date_after': 'A date string in "YYYY-MM-DD" format of the date after which you want all returned requests to have been created',
    'request_date_before': 'A date string in "YYYY-MM-DD" format of the date before which you want all returned requests to have been created',
    'distance_from': 'A numeric value of the minimum distance you want the request to be from a system unit',
    'distance_to': 'A numeric value of the maximum distance you want the request to be from a system unit',
    'fiscal_year': 'A numeric value of the fiscal year you want the returned request to have been created in',
    'freetext': "An alphanumeric filter that will be applied to specific fields", #TODO specify which fields for which views?
    'case': 'A foreign key integer value identifying a case',
    'report': 'An alphanumeric value of the report to be produced (e.g. "casesbyunit", "daystoresolution", etc.)',
    'user': "An alphanumeric value of the username to filter for",
    'used_users': 'A boolean value (True) identifying whether to return only formerly and currently active users'
})

