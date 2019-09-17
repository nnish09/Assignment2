def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.jpg', '.png']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Unsupported file extension.')


def validate_file_extension1(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pdf', '.docx']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Unsupported file extension.')


# def submit_validator(value):
#     if value < 1900 or value > datetime.datetime.now().year:
#         raise ValidationError(
#             _('%(value)s is not a correcrt year!'),
#             params={'value': value},
#         )