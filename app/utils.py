# app/utils.py

import re

# app/utils.py
import re

def clean_text(text: str) -> str:
    """
    Cleans the input receipt text by removing unnecessary characters and ensuring proper spacing.
    """
    text = re.sub(r'\s+', ' ', text)  # Replaces all whitespace (including \n) with a single space
    return text.strip()