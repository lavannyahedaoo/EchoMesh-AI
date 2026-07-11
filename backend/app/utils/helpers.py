import re
from uuid import UUID
from datetime import datetime, timezone
from typing import Optional

def clean_text_payload(text: str) -> str:
    """
    Cleans raw text by stripping leading/trailing whitespace, normalizing line endings,
    and removing excessive consecutive spacing.
    """
    if not text:
        return ""
    # Normalize whitespaces
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def validate_uuid(uuid_to_test: str) -> bool:
    """
    Safely asserts whether a string complies with the UUIDv4 standard structure.
    """
    try:
        uuid_obj = UUID(uuid_to_test, version=4)
        return str(uuid_obj) == uuid_to_test
    except ValueError:
        return False

def get_utc_now() -> datetime:
    """
    Returns the current timezone-aware UTC datetime.
    """
    return datetime.now(timezone.utc)
