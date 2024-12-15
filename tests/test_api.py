# tests/test_api.py

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_parse_receipt_success():
    response = client.post(
        "/parse-receipt",
        json={
            "text": "Chicken Rice 5.50\nFries 3.50\nDrink 2.00"
        },
        headers={"x-api-key": "your-secure-api-key"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "items": [
            {"item": "Chicken Rice", "amount": 5.50},
            {"item": "Fries", "amount": 3.50},
            {"item": "Drink", "amount": 2.00}
        ]
    }

def test_parse_receipt_european_format():
    response = client.post(
        "/parse-receipt",
        json={
            "text": "Chicken Rice 5,50\nFries 3,50\nDrink 2,00"
        },
        headers={"x-api-key": "your-secure-api-key"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "items": [
            {"item": "Chicken Rice", "amount": 5.50},
            {"item": "Fries", "amount": 3.50},
            {"item": "Drink", "amount": 2.00}
        ]
    }

def test_parse_receipt_no_items():
    response = client.post(
        "/parse-receipt",
        json={
            "text": "Subtotal: 11.00\nTax: 0.99"
        },
        headers={"x-api-key": "your-secure-api-key"}
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "No items found in receipt."
    }

def test_parse_receipt_empty_text():
    response = client.post(
        "/parse-receipt",
        json={
            "text": ""
        },
        headers={"x-api-key": "your-secure-api-key"}
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Input text is empty."
    }

def test_parse_receipt_malformed_price():
    response = client.post(
        "/parse-receipt",
        json={
            "text": "Chicken Rice five.fifty\nFries 3.50"
        },
        headers={"x-api-key": "your-secure-api-key"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "items": [
            {"item": "Fries", "amount": 3.50}
        ]
    }

def test_parse_receipt_missing_api_key():
    response = client.post(
        "/parse-receipt",
        json={
            "text": "Chicken Rice 5.50\nFries 3.50\nDrink 2.00"
        }
        # Missing headers
    )
    assert response.status_code == 403
    assert response.json() == {
        "detail": "Forbidden"
    }