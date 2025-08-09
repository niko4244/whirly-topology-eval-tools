"""
API Endpoints for Brand-Filtered Symbol and Schematic Search
- Ensures search results are limited to Whirlpool, Maytag, KitchenAid, and Jenn-Air.
"""

from fastapi import FastAPI, Query
from typing import List, Dict
from knowledge.search import search_symbols, search_diagrams
from knowledge.brand_filter import is_allowed_brand

app = FastAPI()

def filter_results_by_brand(results: List[Dict]) -> List[Dict]:
    """
    Filter search results to only include supported brands.
    """
    return [r for r in results if is_allowed_brand(r.get("appliance_id", ""))]

@app.get("/search/symbols")
def api_search_symbols(query: str = Query(..., description="Symbol or keyword to search for")) -> List[Dict]:
    """
    Search for symbols/components in the knowledge base, limited to supported brands.
    """
    results = search_symbols(query)
    filtered = filter_results_by_brand(results)
    return filtered

@app.get("/search/diagrams")
def api_search_diagrams(query: str = Query(..., description="Keyword or symbol for diagram search")) -> List[Dict]:
    """
    Search for wiring diagrams/schematics in the knowledge base, limited to supported brands.
    """
    results = search_diagrams(query)
    filtered = filter_results_by_brand(results)
    return filtered