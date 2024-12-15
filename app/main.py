# app/main.py

from fastapi import FastAPI, HTTPException, Header, Depends
from app.models import ReceiptRequest, ReceiptResponse
from app.parsers import parse_receipt_text
from app.utils import clean_text
from typing import Optional
import os
import logging

app = FastAPI(
    title="Receipt Parsing API",
    description="API to parse receipt text and extract items with prices.",
    version="1.0.0"
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API Key for authentication
API_KEY = os.getenv("API_KEY", "your-default-secure-api-key")

def verify_api_key(x_api_key: Optional[str] = Header(None)):
    if x_api_key != API_KEY:
        logger.warning(f"Unauthorized access attempt with key: {x_api_key}")
        raise HTTPException(status_code=403, detail="Forbidden")

@app.post("/parse-receipt", response_model=ReceiptResponse, summary="Parse Receipt Text")
async def parse_receipt(
    request: ReceiptRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Parses receipt text into items and their corresponding prices.
    """
    if not request.text:
        logger.warning("Empty text received.")
        raise HTTPException(status_code=400, detail="Input text is empty.")

    try:
        cleaned_text = clean_text(request.text)
        logger.info(f"Cleaned text: {cleaned_text}")
        items = parse_receipt_text(cleaned_text)
        logger.info(f"Parsed items: {items}")
        return {"items": items}
    except ValueError as ve:
        logger.error(f"Parsing error: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.exception("Unexpected error during parsing.")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")