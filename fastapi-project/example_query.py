from typing import Optional
from fastapi import FastAPI

app = FastAPI()

# Dummy database
products_db = [
    {"name": "Laptop", "category": "electronics", "price": 50000},
    {"name": "Phone", "category": "electronics", "price": 20000},
    {"name": "Shirt", "category": "clothing", "price": 1000},
]


@app.get("/products")
def filter_products(category: Optional[str] = None, limit: int = 10, skip: int = 0):
    results = products_db
    if category:
        results = [item for item in results if item["category"] == category]
    return results[skip : skip + limit]