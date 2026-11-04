import re
import unicodedata


def slugify(input):
    if not isinstance(input, str):
        return ""

    folded = "".join(
        ch for ch in unicodedata.normalize("NFKD", input) if not unicodedata.combining(ch)
    )
    return re.sub(r"[^a-z0-9]+", "-", folded.lower().strip()).strip("-")
