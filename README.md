# Coconut API

## Directory
```
receipt-parser/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI entry point
│   ├── models.py        # Pydantic models for request/response
│   ├── parsers.py       # NLP-based parsing logic
│   ├── utils.py         # Helper functions (e.g., text normalization)
│   ├── nlp/
│   │   ├── __init__.py
│   │   ├── entity_ruler.py  # Custom entity patterns
│   └── __init__.py
├── tests/
│   ├── __init__.py
│   ├── test_parsers.py  # Unit tests for parsers.py
│   └── test_api.py      # Integration tests for API endpoints
├── requirements.txt     # Python dependencies
├── Dockerfile           # Docker configuration for containerization
├── README.md            # Project documentation
└── .gitignore           # Files/directories to ignore in Git

```