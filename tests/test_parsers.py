# tests/test_parsers.py

from app.parsers import parse_receipt_text

def test_parse_receipt_text_standard():
    input_text = "Chicken Rice 5.50\nFries 3.50\nDrink 2.00"
    expected_output = [
        {"item": "Chicken Rice", "amount": 5.50},
        {"item": "Fries", "amount": 3.50},
        {"item": "Drink", "amount": 2.00}
    ]
    assert parse_receipt_text(input_text) == expected_output

def test_parse_receipt_text_european_format():
    input_text = "Chicken Rice 5,50\nFries 3,50\nDrink 2,00"
    expected_output = [
        {"item": "Chicken Rice", "amount": 5.50},
        {"item": "Fries", "amount": 3.50},
        {"item": "Drink", "amount": 2.00}
    ]
    assert parse_receipt_text(input_text) == expected_output

def test_parse_receipt_text_no_items():
    input_text = "Subtotal: 11.00\nTax: 0.99"
    try:
        parse_receipt_text(input_text)
    except ValueError as e:
        assert str(e) == "No items found in receipt."
    else:
        assert False, "Expected ValueError for no items found"

def test_parse_receipt_text_malformed_price():
    input_text = "Chicken Rice five.fifty\nFries 3.50"
    expected_output = [
        {"item": "Fries", "amount": 3.50}
    ]
    assert parse_receipt_text(input_text) == expected_output