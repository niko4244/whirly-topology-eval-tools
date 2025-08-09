# Brand-Filtered Gamified Tech Sheet System: API Overview

## Core Capabilities

### Upload, Extract, and Award
- **POST /techsheet/upload/{appliance_id}**  
  Upload tech sheet, extract symbols/diagrams/text, validate brand, award badges and log badge events (Whirlpool, Maytag, KitchenAid, Jenn-Air only).

### Search & Feedback
- **POST /search/feedback**  
  Submit rating/comment for search results (supported brands only).
- **GET /search/feedback/summary**  
  View feedback summary for a searched symbol/keyword (supported brands).
- **GET /search/trending**  
  Top trending search items for supported brands.

### Gamification & Leaderboard
- **GET /leaderboard**  
  See user upload stats and earned badges for supported brands.
- **GET /badges?user_id={userid}**  
  See badge history and details for a user (supported brands).
- **GET /badges/all**  
  View all possible badge definitions.

### Badge Event Audit
- **GET /badges/events?user_id={userid}**  
  See history of badge award events for a user (supported brands).

### User & Admin Summaries
- **GET /user/summary?user_id={userid}**  
  See personal uploads, badges, badge events, and feedback.
- **GET /admin/summary**  
  Overview: uploads, unique users, badges, uploads by brand, trending badge reasons, feedback count.

### CSV Report Download (Admin)
- **GET /admin/report/leaderboard.csv**  
  Download all user uploads and badges (supported brands only).
- **GET /admin/report/badge_events.csv**  
  Download badge event log (supported brands only).

---

## Security & Compliance

- All endpoints strictly filter and operate only for Whirlpool, Maytag, KitchenAid, and Jenn-Air appliances.
- Gamification, badge, leaderboard, feedback, audit, and reporting ignore unsupported brands.

## Extensibility

- Add brands by updating `ALLOWED_BRANDS`.
- Add new badges; update logic in `knowledge/gamification.py`, `knowledge/badge_award_events.py`, and API docs.
- CSV report logic can easily add more fields or export types.

## Testing

- Core logic covered by unit tests (`tests/test_brand_system.py`).
- Ensures uploads, badge awarding, event logging, leaderboard, report export, and brand compliance.

---

## Deployment Readiness

- API endpoints and logic modular for integration into FastAPI, Flask, Django, or serverless platforms.
- CSV export and audit logs ready for business analytics and compliance.
- Gamification and feedback loop ready for technician engagement.

---

## Next Steps

- Add CI/CD pipeline for automated testing.
- Integrate with frontend/dashboard for technician and admin use.
- Add OAuth/authentication for role-based access (user vs. admin).
- Expand badge logic, add new analytics, and enable notifications.

---