"""
API Endpoints for Search Result Feedback and Analytics (Brand-Filtered)
- Allows users to rate, comment, and flag results for Whirlpool, Maytag, KitchenAid, and Jenn-Air appliances.
- Analytics and feedback are brand-specific for targeted KB improvement.
"""

from fastapi import FastAPI, Query, HTTPException
from typing import List, Dict, Optional
from knowledge.analytics import rate_search_result, get_feedback_summary, get_trending_symbols
from knowledge.brand_filter import ALLOWED_BRANDS

app = FastAPI()

@app.post("/search/feedback")
def api_rate_search_result(
    query: str = Query(..., description="Searched symbol/component/keyword"),
    user_id: str = Query(..., description="User identifier"),
    rating: int = Query(..., ge=1, le=5, description="Rating (1=poor, 5=excellent)"),
    feedback: Optional[str] = Query("", description="Optional feedback/comment")
):
    # Only allow feedback for supported brands
    if not any(brand in query.lower() for brand in ALLOWED_BRANDS):
        raise HTTPException(
            status_code=400,
            detail="Feedback only accepted for Whirlpool, Maytag, KitchenAid, and Jenn-Air related queries."
        )
    rate_search_result(query, user_id, rating, feedback)
    return {"message": "Feedback submitted successfully."}

@app.get("/search/feedback/summary")
def api_get_feedback_summary(query: str = Query(..., description="Searched symbol/component/keyword")) -> Dict:
    # Only allow feedback summary for supported brands
    if not any(brand in query.lower() for brand in ALLOWED_BRANDS):
        raise HTTPException(
            status_code=400,
            detail="Feedback summary only available for Whirlpool, Maytag, KitchenAid, and Jenn-Air related queries."
        )
    summary = get_feedback_summary(query)
    return summary

@app.get("/search/trending")
def api_get_trending_symbols(top_n: int = Query(5, description="Number of top trending items to return")) -> List[str]:
    trending = get_trending_symbols(top_n)
    # Filter out non-supported brands
    filtered = [q for q in trending if any(brand in q.lower() for brand in ALLOWED_BRANDS)]
    return filtered