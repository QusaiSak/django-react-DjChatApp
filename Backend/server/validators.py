from PIL import Image
from rest_framework.exceptions import ValidationError
import os


def validate_icon_image_size(image):
    if image:
        with Image.open(image) as img:
            if img.width > 70 or img.height > 70:
                raise ValidationError(
                    f"Icon image should be less than or equal to 70x70 pixels - size you uploaded : {image.width}x{image.height}."
                )


def validate_image_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = [".jpg", ".jpeg", ".png", ".gif"]
    if not ext.lower() in valid_extensions:
        raise ValidationError(f"Unsupported file extension. Only {', '.join(valid_extensions)} are allowed.")
