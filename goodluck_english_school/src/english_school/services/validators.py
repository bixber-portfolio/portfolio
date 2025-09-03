from PIL import Image
import io
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile

from .constants import (
    MAX_IMAGE_SIZE,
    IMAGE_LIMIT_MB,
    REQUIRED_WIDTH_PX,
    REQUIRED_HEIGTH_PX,
)


def image_size_validator(value):
    try:
        image_content = value.read()
        img = Image.open(io.BytesIO(image_content))
        width, height = img.size
        if (width, height) != (REQUIRED_WIDTH_PX, REQUIRED_HEIGTH_PX):
            raise ValidationError(
                f'Изображение должно быть размером '
                f'{REQUIRED_WIDTH_PX}x{REQUIRED_HEIGTH_PX} пикселей.'
            )
    except Exception as e:
        raise ValidationError('Возникла ошибка в проверке размера изображения')


def image_file_size_validator(value):
    if isinstance(value, InMemoryUploadedFile) and value.size > MAX_IMAGE_SIZE:
        raise ValidationError(
            f'Размер файла слишком большой. '
            f'Максимальный размер - {IMAGE_LIMIT_MB} МБ.'
        )