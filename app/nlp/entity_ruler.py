# app/nlp/entity_ruler.py

import spacy
from spacy.pipeline import EntityRuler

def add_entity_ruler(nlp):
    ruler = EntityRuler(nlp, overwrite_ents=True)
    
    patterns = [
        {"label": "PRODUCT", "pattern": [{"LOWER": "chicken"}, {"LOWER": "rice"}]},
        {"label": "PRODUCT", "pattern": [{"LOWER": "fries"}]},
        {"label": "PRODUCT", "pattern": [{"LOWER": "drink"}]},
        # Add more product patterns as needed
    ]
    
    ruler.add_patterns(patterns)
    nlp.add_pipe("entity_ruler", before="ner")
    return nlp