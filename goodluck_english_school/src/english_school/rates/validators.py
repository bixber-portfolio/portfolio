from lxml import etree
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile

from .constants import (
    FILE_EXTENSION_STR,
    MAX_SVG_SIZE,
    SVG_LIMIT_MB,
    REQUIRED_WIDTH_PX,
    REQUIRED_HEIGTH_PX,
)


def svg_size_validator(value):
    try:
        svg_content = value.read()
        root = etree.fromstring(svg_content)
        width_in_px = root.attrib.get('width', '').replace('px', '')
        height_in_px = root.attrib.get('height', '').replace('px', '')
        if (list(map(int, [width_in_px, height_in_px]))
            != [REQUIRED_WIDTH_PX, REQUIRED_HEIGTH_PX]):
            raise ValidationError(
                (f'{FILE_EXTENSION_STR.upper()} файл должен быть размером '
                 f'{REQUIRED_WIDTH_PX}x{REQUIRED_HEIGTH_PX} пикселей.')
            )

    except Exception as e:
        raise ValidationError('Возникла ошибка в проверке расширения файла')


def svg_file_size_validator(value):
    if isinstance(value, InMemoryUploadedFile) and value.size > MAX_SVG_SIZE:
        raise ValidationError(
            f'Размер файла {FILE_EXTENSION_STR.upper()} слишком большой. '
            f'Максимальный размер - {SVG_LIMIT_MB} МБ.'
        )