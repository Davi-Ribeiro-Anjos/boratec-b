from django.core.exceptions import ValidationError


def file_size(file, value: int):
    limit = value * 1024 * 1024

    if file and file.size > limit:
        raise ValidationError(
            f"Arquivo muito grande insira um arquivo menor que {value}mb."
        )
