# Brand-Specific Badge Event API

## Endpoint

- `GET /badges/events?user_id={userid}`
  - Returns badge award event history for a user, for Whirlpool, Maytag, KitchenAid, and Jenn-Air uploads only.
  - Each event includes badge name, reason, appliance, brand, and timestamp.

## How It Works

- Shows when and why each badge was awarded for supported brand contributions.
- Enables users and admins to audit contributions and badge history.

## Example Response

```json
[
  {
    "user_id": "niko4244",
    "appliance_id": "maytag_dryer_003",
    "badge": "Schematic Uploader",
    "reason": "Uploaded a Maytag dryer schematic.",
    "brand": "maytag",
    "timestamp": "2025-08-09T04:05:47"
  }
]
```

## Notes

- Only badge events for supported brands are returned.
- Keeps audit and badge history focused on business-relevant content.

---