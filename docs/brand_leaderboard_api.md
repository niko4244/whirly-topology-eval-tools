# Brand-Specific Gamified Leaderboard API

## Endpoint

- `GET /leaderboard`
  - Returns user contribution stats for Whirlpool, Maytag, KitchenAid, and Jenn-Air uploads only.
  - Includes upload count, badges earned, last upload timestamp.

## How It Works

- Leaderboard tracks only uploads and badges for the four supported brands.
- All other contributions are ignored for leaderboard and gamification.
- Badges may include "Symbol Scout", "Schematic Uploader", "Documentation Champion", etc.

## Example Response

```json
{
  "niko4244": {
    "uploads": 15,
    "badges": ["Symbol Scout", "Schematic Uploader"],
    "last_upload": "2025-08-09T03:45:00"
  },
  "techguru": {
    "uploads": 11,
    "badges": ["Documentation Champion"],
    "last_upload": "2025-08-08T23:10:00"
  }
}
```

## Notes

- Only Whirlpool, Maytag, KitchenAid, and Jenn-Air uploads count toward leaderboard stats and badges.
- Keeps gamification focused on business-relevant content.
- Easily extendable if brand scope changes.

---