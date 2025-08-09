# Brand-Filtered Reports API (CSV Download)

## Endpoints

- `GET /admin/report/leaderboard.csv`
  - Download a CSV of all user uploads, badges, last upload timestamp (supported brands only).

- `GET /admin/report/badge_events.csv`
  - Download a CSV of all badge award events for Whirlpool, Maytag, KitchenAid, and Jenn-Air uploads.

## Use Cases

- **Business Analytics:** Track technician engagement, upload stats, badge distribution.
- **Audit:** Full event log for badge awards, including timestamp, user, appliance, brand, and reason.

## Notes

- All data filtered to supported brands.
- CSV format enables easy import into BI tools, spreadsheets, or audit workflows.

---