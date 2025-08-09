# CSV Reports for Brand-Filtered Tech Sheet System

## Endpoints

- `GET /admin/report/leaderboard.csv`  
  Download all user uploads and badges (supported brands only).
- `GET /admin/report/badge_events.csv`  
  Download badge event log (supported brands only).
- `GET /admin/report/feedback.csv`  
  Download feedback log (supported brands only).

## Use Cases

- **Business analytics:** Import into BI tools.
- **Compliance:** Audit full engagement and feedback history.
- **Feedback:** Analyze satisfaction and technician comments by brand.

## Compliance

- All data strictly filtered to supported brands.
- No unsupported brand data in reports.

## Next Steps

- Add role-based authentication to restrict report access.
- Integrate CSV export into automated reporting workflows.
- Add more analytics columns as needed.

---