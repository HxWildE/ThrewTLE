import re



def sanitize_input_string(value: str) -> str:
    """Strip dangerous characters and trim excessive whitespace."""
    if not value:
        return ""
    # Strip null bytes and non-printable control characters
    cleaned = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', value)
    return cleaned.strip()


def validate_slug_format(slug: str) -> bool:
    """Validate that problem slug follows lowercase kebab-case convention."""
    return bool(re.match(r'^[a-z0-9]+(?:-[a-z0-9]+)*$', slug))
