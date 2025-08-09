"""
API Endpoints for Symbol and Schematic Search
- Allows users and technicians to search for symbols, keywords, and diagrams via HTTP requests.
- Returns annotated results, wiring diagrams, and related troubleshooting guides.
"""

from fastapi import FastAPI, Query
from typing import List, Dict
from knowledge.search import search_symbols, search_diagrams

app = FastAPI()

@app.get("/search/symbols")
def api_search_symbols(query: str = Query(..., description="Symbol or keyword to search for")) -> List[Dict]:
    """
    Search for symbols/components in the knowledge base.
    Returns annotated results including symbols, diagrams, and text matches.
    """
    results = search_symbols(query)
    return results

@app.get("/search/diagrams")
def api_search_diagrams(query: str = Query(..., description="Keyword or symbol for diagram search")) -> List[Dict]:
    """
    Search for wiring diagrams/schematics in the knowledge base.
    Returns entries with relevant diagrams and context.
    """
    results = search_diagrams(query)
    return results