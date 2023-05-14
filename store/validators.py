from django.core.exceptions import ValidationError


def file_size_validator(file):
    max_size_kb = 1000
    if file.size > max_size_kb * 1024:
        raise ValidationError(f'file can not be larger than {max_size_kb}KB')
