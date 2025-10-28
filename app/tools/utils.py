import base64
import hashlib
import re


def hash_password(password: str) -> str:
    """Хэширует пароль с использованием SHA-256."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def clean_text(text):
    """Очищает текст от markdown-стилей: **, *, ###, ##, #."""
    cleaned_text = re.sub(r"(\*\*|\*|###|##|#)", "", text)
    cleaned_text = re.sub(r"\n+", " ", cleaned_text)
    cleaned_text = re.sub(r"\s+", " ", cleaned_text)
    return cleaned_text


def encode_image_to_base64(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
