import uuid
from pathlib import Path

from fastapi import UploadFile, HTTPException

from src.core.config import settings


def validate_file_extension(*, filename: str, allowed_file_extensions: list[str]):
    file_extension = Path(filename).suffix
    if not file_extension:
        raise HTTPException(status_code=400, detail="Invalid file extension")
    if file_extension not in allowed_file_extensions:
        raise HTTPException(status_code=400, detail="Invalid file extension")


def generate_unique_filename(filename: str) -> str:
    # TODO: Добавить валидацию файла из библиотеки werkzeug.secure_filename
    pic_name = str(uuid.uuid1()) + "_" + filename
    return pic_name


def write_file_on_disk(uploaded_file: UploadFile, prefix: str = None) -> str:
    filename = generate_unique_filename(uploaded_file.filename)
    if prefix:
        file_location = f"{settings.MEDIA_ROOT}/{prefix}{filename}"
    else:
        file_location = f"{settings.MEDIA_ROOT}/{filename}"
    output_file = Path(file_location)
    output_file.parent.mkdir(exist_ok=True, parents=True)
    output_file.write_bytes(uploaded_file.file.read())
    return file_location
