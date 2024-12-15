# app/parsers.py

import spacy
from typing import List, Dict
import re
from app.nlp.entity_ruler import add_entity_ruler

# Initialize SpaCy NLP model with custom Entity Ruler

# Load the NLP model directly as an installed package
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
    
    entities = list(doc.ents)
    print("Entities found:", [(ent.text, ent.label_) for ent in entities])
    
    for i, ent in enumerate(entities):
        if ent.label_ == "PRODUCT":
            # Initialize price as None
            price = None
            # Iterate over the subsequent entities to find the next PRICE/MONEY/CARDINAL
            for next_ent in entities[i+1:]:
                if next_ent.label_ in ["MONEY", "PRICE", "CARDINAL"]:
                    price_str = next_ent.text.replace(',', '.').replace('$', '').strip()
                    try:
                        price = float(price_str)
                        print(f"Pairing Product: {ent.text} with Price: {price}")
                        break
                    except ValueError:
                        print(f"Failed to convert price: {next_ent.text}")
                        continue
            if price is not None:
                items.append({"item": ent.text, "amount": price})
            else:
                print(f"No price found for product: {ent.text}")
    
    # Fallback: If some products are missing prices, attempt to extract prices via regex
    products_detected = len([ent for ent in entities if ent.label_ == "PRODUCT"])
    prices_detected = len(items)
    if prices_detected < products_detected:
        # Extract prices via regex
        regex_prices = extract_prices_with_regex(text)
        print(f"Regex extracted prices: {regex_prices}")
        # Find products without prices
        products = [ent.text for ent in entities if ent.label_ == "PRODUCT"]
        paired_prices = [item['amount'] for item in items]
        remaining_prices = [p for p in regex_prices if p not in paired_prices]
        for product, price in zip(products[prices_detected:], remaining_prices):
            print(f"Falling back to regex pairing Product: {product} with Price: {price}")
            items.append({"item": product, "amount": price})
    
    if not items:
        print("No items found after parsing.")
        raise ValueError("No items found in receipt.")
    
    print(f"Parsed items: {items}")
    return items

def debug_named_entities(doc):
    print("\n=== DEBUG: Named Entities ===")
    for ent in doc.ents:
        print(f"Text: {ent.text}, Label: {ent.label_}")
    print("\n")