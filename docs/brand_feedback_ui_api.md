# Feedback Feature for Brand-Filtered Tech Sheet System

## Features

- **Technicians** can submit ratings/comments for uploads or search results (supported brands only).
- **Admins/Users** can view feedback summary for each appliance.

## UI Flow

1. Technician goes to **Submit Feedback** page.
2. Enters user ID, appliance ID, rating, and comment.
3. Feedback is sent via API (filtered for Whirlpool, Maytag, KitchenAid, Jenn-Air).
4. All feedback viewable by appliance ID, with average rating.

## Compliance

- Feedback is ignored for unsupported brands.
- All feedback endpoints and summaries filter for brand compliance.

## Next Steps

- Add authentication.
- Show feedback on achievement/leaderboard pages.
- Add feedback analytics to admin dashboard.

---