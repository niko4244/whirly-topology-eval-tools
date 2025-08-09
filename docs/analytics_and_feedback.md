# Analytics & Feedback Loop

## Search Analytics

**Purpose:**  
Track the most searched symbols, components, and diagrams to:
- Guide future internet ingestion and KB enrichment.
- Surface trending topics for technicians and users.
- Prioritize updates and internet crawling for high-demand items.

**How it Works:**
- Every symbol or schematic search is logged.
- Trending analytics (top 10, 50, etc.) are available for dashboard display or admin review.
- Used to adjust crawling, indexing, and model retraining priorities.

---

## User Rating & Feedback

**Purpose:**  
Improve result quality and curation by letting users rate and comment on search results.

**Features:**
- Users rate results from 1 (poor) to 5 (excellent).
- Optional comments allow flagging errors, missing diagrams, or confirming success.
- Feedback is aggregated for admin review and continuous improvement.

**API Examples:**

```python
# Log a search for trending analysis
log_search("relay", "niko4244")

# Get top searched symbols/components
trending = get_trending_symbols(top_n=5)

# User rates a search result
rate_search_result("relay", "niko4244", 4, "Quickly found the wiring diagram I needed.")

# Get feedback summary for a query
summary = get_feedback_summary("relay")
print("Average Rating:", summary["average_rating"])
print("Comments:", summary["comments"])
```

---

## Next Steps

- Display trending analytics and feedback summaries in UI dashboard.
- Use trends to focus autonomous internet ingestion (crawl more relay/fuse/motor docs if trending).
- Gamify feedback participation (badges for helpful ratings/comments).
- Integrate feedback loop into search and KB enrichment pipeline.

---