"""
Symbol/Component Analytics and Feedback Loop
- Tracks most searched symbols/components and diagrams.
- Provides insights for future internet ingestion and knowledge base enrichment.
- Accepts user ratings and flags for search result quality improvement.
"""

import json
import datetime
from typing import List, Dict

def log_search(query: str, user_id: str, analytics_path: str = "search_analytics.json"):
    """
    Log each search query for analytics and trending symbol/component tracking.
    Args:
        query (str): Searched keyword/symbol.
        user_id (str): User making the search.
        analytics_path (str): Path to analytics log.
    Returns:
        None
    """
    try:
        with open(analytics_path, "r") as f:
            analytics = json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        analytics = {}
    entry = analytics.get(query, {"count": 0, "users": [], "last_search": None})
    entry["count"] += 1
    entry["users"] = list(set(entry["users"] + [user_id]))
    entry["last_search"] = datetime.datetime.utcnow().isoformat()
    analytics[query] = entry
    with open(analytics_path, "w") as f:
        json.dump(analytics, f, indent=2)

def get_trending_symbols(top_n: int = 10, analytics_path: str = "search_analytics.json") -> List[str]:
    """
    Get top N most searched symbols/components.
    Args:
        top_n (int): Number of trending items to return.
        analytics_path (str): Path to analytics log.
    Returns:
        list of str: Trending symbols/components.
    """
    try:
        with open(analytics_path, "r") as f:
            analytics = json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return []
    sorted_trends = sorted(analytics.items(), key=lambda x: x[1]["count"], reverse=True)
    return [item[0] for item in sorted_trends[:top_n]]

def rate_search_result(query: str, user_id: str, rating: int, feedback: str = "", feedback_path: str = "search_feedback.json"):
    """
    Users can rate and comment on search results for quality improvement.
    Args:
        query (str): Search query.
        user_id (str): User rating the result.
        rating (int): 1 (poor) to 5 (excellent).
        feedback (str): Optional comment.
        feedback_path (str): Path to feedback log.
    Returns:
        None
    """
    try:
        with open(feedback_path, "r") as f:
            feedback_data = json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        feedback_data = {}
    entry = feedback_data.get(query, [])
    entry.append({
        "user_id": user_id,
        "rating": rating,
        "comment": feedback,
        "timestamp": datetime.datetime.utcnow().isoformat()
    })
    feedback_data[query] = entry
    with open(feedback_path, "w") as f:
        json.dump(feedback_data, f, indent=2)

def get_feedback_summary(query: str, feedback_path: str = "search_feedback.json"):
    """
    Get summary of feedback for a query.
    Args:
        query (str): Search query.
        feedback_path (str): Path to feedback log.
    Returns:
        dict: Average rating and comments.
    """
    try:
        with open(feedback_path, "r") as f:
            feedback_data = json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return {"average_rating": None, "comments": []}
    entries = feedback_data.get(query, [])
    if not entries:
        return {"average_rating": None, "comments": []}
    avg = sum(e["rating"] for e in entries) / len(entries)
    comments = [e["comment"] for e in entries if e["comment"]]
    return {"average_rating": avg, "comments": comments}

# Example usage:
if __name__ == "__main__":
    log_search("motor", "niko4244")
    print(get_trending_symbols())
    rate_search_result("motor", "niko4244", 5, "Great results, found correct diagram!")
    print(get_feedback_summary("motor"))