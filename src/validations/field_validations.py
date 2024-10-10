

def validate_teks_code_field(values):
    if values["assignmentType"] != "STAAR" and values["teksCode"] is not None:
        raise ValueError('TEKS Code field must be null.')
    return values

def validate_category_field(values):
    if values["assignmentType"] != "STAAR" and values["category"] is not None:
        raise ValueError('Category field must be null.')
    return values

def validate_deleted_field(values):
    if 'deleted' in values:
        raise ValueError("Deleted field must not be included in the payload.")
    return values

def validate_created_date_field(values):
    if 'createdDate' in values:
        raise ValueError("Created date field must not be included in the payload.")
    return values

def validate_updated_date_field(values):
    if 'updatedDate' in values:
        raise ValueError("Updated date field must not be included in the payload.")
    return values