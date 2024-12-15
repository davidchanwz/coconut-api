# app/parsers.py

import spacy
from typing import List, Dict
from app.nlp.entity_ruler import add_entity_ruler

# Initialize SpaCy NLP model with custom Entity Ruler
nlp = spacy.load("en_core_web_sm")
nlp = add_entity_ruler(nlp)

def parse_receipt_text(text: str) -> List[Dict[str, float]]:
    """
    Parses receipt text using SpaCy's NER to extract items and their prices.
    
    Args:
        text (str): OCR-extracted text from the receipt.
    
    Returns:
        List[Dict[str, float]]: A list of dictionaries containing 'item' and 'amount'.
    """
    items = []
    doc = nlp(text)
    
    # Extract entities
    products = []
    prices = []
    
    for ent in doc.ents:
        if ent.label_ == "PRODUCT":
            products.append(ent.text)
        elif ent.label_ == "MONEY":
            # Clean the price string and convert to float
            price_str = ent.text.replace(',', '.').replace('$', '').strip()
            try:
                price = float(price_str)
                prices.append(price)
            except ValueError:
                continue
    
    # Pair products with prices based on their order
    for product, price in zip(products, prices):
        items.append({"item": product, "amount": price})
    
    if not items:
        raise ValueError("No items found in receipt.")
    
    return items