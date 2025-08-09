# Brand-Filtered Search Feedback & Analytics API

## Endpoints

- `POST /search/feedback`
  - Submit a rating (1–5) and optional comment for a search result.
  - Feedback only accepted for Whirlpool, Maytag, KitchenAid, and Jenn-Air related queries.

- `GET /search/feedback/summary?query={keyword}`
  - Returns aggregated rating and comments for a given query (brand-filtered).

- `GET /search/trending?top_n=5`
  - Returns the top trending searched symbols/components for supported brands only.

## How It Works

- Ensures user ratings, comments, and trending analytics are focused on the four supported brands.
- Feedback loop helps improve KB quality specifically for Whirlpool, Maytag, KitchenAid, and Jenn-Air appliances.

## Example Usage

```http
POST /search/feedback?query=whirlpool relay&user_id=niko4244&rating=5&feedback=Found right diagram!
GET /search/feedback/summary?query=maytag motor
GET /search/trending?top_n=5
```

## Notes

- Feedback and analytics for Samsung, LG, or other brands are not accepted or shown.
- Keeps system targeted, relevant, and compliant with business scope.
- Easy to extend if brand list changes.

---