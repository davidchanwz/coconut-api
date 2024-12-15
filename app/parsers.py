# app/parsers.py

import spacy
from typing import List, Dict
import re
import logging
from app.nlp.entity_ruler import add_entity_ruler

# Initialize SpaCy NLP model with custom Entity Ruler

try:
    nlp = spacy.load("en_core_web_sm", exclude=["lemmatizer", "tagger", "morphologizer"])
except Exception as e:
    raise ValueError(f"Could not load SpaCy model 'en_core_web_sm'. Error: {e}")
nlp = add_entity_ruler(nlp)
print("Pipeline components:", nlp.pipe_names)

def extract_prices_with_regex(text: str) -> List[float]:
    """
    Extracts prices from text using regex as a fallback mechanism.
    
    Args:
        text (str): The input text containing prices.
    
    Returns:
        List[float]: A list of extracted prices.
    """
    # Regex to match prices like 5.50 or 5,50
    price_matches = re.findall(r'\b\d+[.,]\d{2}\b', text)
    prices = []
    for price in price_matches:
        price = price.replace(',', '.')
        try:
            prices.append(float(price))
        except ValueError:
            continue
    return prices

def parse_receipt_text(text: str) -> List[Dict[str, float]]:
    """
    Parses receipt text using SpaCy to extract items and prices.
    
    Args:
        text (str): OCR-extracted text from the receipt.
    
    Returns:
        List[Dict[str, float]]: A list of dictionaries containing 'item' and 'amount'.
    """
    items = []
    doc = nlp(text)
    
    # Debug named entities
    debug_named_entities(doc)
    
    # Extract entities with labels PRODUCT and MONEY
    products = [ent for ent in doc.ents if ent.label_ == "PRODUCT"]
    money = [ent for ent in doc.ents if ent.label_ == "MONEY"]
    
    # Convert MONEY entities to float amounts
    money_amounts = []
    for ent in money:
        price_str = ent.text.replace(',', '.').replace('$', '').replace('€', '').replace('¥', '').strip()
        try:
            amount = float(price_str)
            money_amounts.append(amount)
        except ValueError:
            continue
    
    # Line-by-line parsing to maintain context
    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue  # Skip empty lines
        
        # Exclude lines that are not items
        if is_excluded_line(line):
            logging.debug(f"Excluded line: {line}")
            continue
        
        # Attempt to extract item and price from the same line
        match = extract_item_price(line)
        if match:
            item_name, item_price = match
            if item_price <= 0:
                logging.debug(f"Skipped invalid amount in line: {line}")
                continue
            items.append({"item": item_name, "amount": item_price})
            logging.debug(f"Matched line: {line} -> Item: {item_name}, Amount: {item_price}")
        else:
            logging.debug(f"No pattern matched for line: {line}")
            continue
    
    # Additional verification to ensure items are correctly parsed
    if not items:
        # Attempt to extract using fallback regex if no items are found
        regex_prices = extract_prices_with_regex(text)
        logging.debug(f"Fallback regex extracted prices: {regex_prices}")
        # Depending on your strategy, you might want to handle this differently
        # For now, raise an exception
        raise ValueError("No valid items with positive amounts were found.")
    
    return items

def is_excluded_line(line: str) -> bool:
    """
    Determines if a line should be excluded from item extraction based on predefined patterns.
    
    Args:
        line (str): A single line of text from the receipt.
    
    Returns:
        bool: True if the line should be excluded, False otherwise.
    """
    exclude_patterns = [
        r'(?i)\bsubtotal\b',
        r'(?i)\btax\b',
        r'(?i)\btotal\b',
        r'(?i)\bchange\b',
        r'(?i)\brefund\b',
        r'(?i)\bdiscount\b',
        r'(?i)\bthank you\b',
        r'(?i)\bpurchase date\b',
        r'(?i)\bdate\b',
        r'(?i)\bbalance due\b',
        r'(?i)\bguests\b',
        r'(?i)\bpax\b',
        r'(?i)\breprint\b',
        r'(?i)\bserver\b',
        r'(?i)\bservice charge\b',
        r'(?i)\bfees\b',
        r'(?i)\bgst\b',
    ]
    
    for pattern in exclude_patterns:
        if re.search(pattern, line):
            return True
    return False

def extract_item_price(line: str):
    """
    Extracts the item name and price from a single line using regex patterns.
    
    Args:
        line (str): A single line of text from the receipt.
    
    Returns:
        tuple or None: Returns a tuple (item_name, amount) if a pattern matches, else None.
    """
    # Define multiple regex patterns to handle different receipt formats
    patterns = [
        # Pattern 1: "Item Name    123.45" or "Item Name 123.45"
        r'^([^\d]+?)\s+(\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})?)$',
        # Pattern 2: "Item Name ..... 123.45"
        r'^([^\d]+?)\.{3,}\s+(\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})?)$',
        # Pattern 3: "Item Name - 123.45"
        r'^([^\d]+?)\s*-\s*(\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})?)$',
        # Pattern 4: "Item Name x2 123.45" (handling quantities)
        r'^([^\d]+?)\s*x\d+\s+(\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})?)$',
        # Pattern 5: "Item Name 2 @ 61.72 each = 123.44"
        r'^([^\d]+?)\s+\d+\s*@\s*\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})?\s*(?:each)?\s*=\s*(\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})?)$'
    ]
    
    for pattern in patterns:
        match = re.match(pattern, line)
        if match:
            item_name, item_price = match.groups()
            # Clean item name: remove trailing dots, hyphens, and extra spaces
            item_name = re.sub(r'[.\-]+$', '', item_name).strip()
            # Normalize price by replacing comma with dot
            item_price = item_price.replace(',', '.')
            try:
                amount = float(item_price)
                return item_name, amount
            except ValueError:
                return None
    return None

def debug_named_entities(doc):
    """
    Prints the named entities for debugging purposes.
    
    Args:
        doc (Doc): A spaCy Doc object.
    """
    print("\n=== DEBUG: Named Entities ===")
    for ent in doc.ents:
        print(f"Text: {ent.text}, Label: {ent.label_}")
    print("\n")