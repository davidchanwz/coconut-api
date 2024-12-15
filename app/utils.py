# app/utils.py

import re

def clean_text(text: str) -> str:
    """
    Cleans the input text by removing unwanted characters and normalizing spaces.
    
    Args:
        text (str): Raw OCR text.
    
    Returns:
        str: Cleaned text.
    """
    # Remove non-printable characters
    text = re.sub(r'[^\x20-\x7E]', '', text)
    # Replace multiple spaces and newlines with a single space and newline
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n+', '\n', text)
    return text.strip()