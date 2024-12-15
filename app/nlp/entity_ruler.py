# app/nlp/entity_ruler.py

import spacy
from spacy.pipeline import EntityRuler

import spacy
from spacy.pipeline import EntityRuler

def add_entity_ruler(nlp):

    ruler = nlp.add_pipe("entity_ruler", before="ner", name="custom_entity_ruler")
    # Custom patterns for identification
    product_patterns = [
        {"label": "PRODUCT", "pattern": [{"IS_ALPHA": True}, {"IS_ALPHA": True}]},
        {"label": "PRODUCT", "pattern": [{"IS_ALPHA": True}]},
    ]
    
    price_patterns = [
        {"label": "MONEY", "pattern": [{"TEXT": {"REGEX": r"^\d+[.,]\d{2}$"}}]},
        {"label": "MONEY", "pattern": [{"LIKE_NUM": True}, {"TEXT": {"REGEX": r"[.,]\d{2}$"}}]}
    ]
    
    # Combine all patterns
    all_patterns = product_patterns + price_patterns
    
    # Add patterns to the EntityRuler
    ruler.add_patterns(all_patterns)


    return nlp