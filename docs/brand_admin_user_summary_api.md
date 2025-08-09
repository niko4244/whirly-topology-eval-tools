# Admin & User Summary API for Supported Brands

## Endpoints

- `GET /admin/summary`
  - Overview: uploads, badges, user count, uploads by brand, trending badge reasons, feedback count.

- `GET /user/summary?user_id={userid}`
  - Shows a user their uploads, badges, last upload, badge event history, and feedback for supported brands.

## Purpose

- **Admin:** Track system health, user engagement, and content growth for Whirlpool, Maytag, KitchenAid, and Jenn-Air.
- **User:** See personal impact, progress, and feedback history.

## Notes

- All stats are filtered to the four supported brands.
- Easy to extend for more brands or analytics.

---