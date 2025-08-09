# Brand-Specific Badge Event Logging

## How It Works

- Whenever a badge is awarded for a Whirlpool, Maytag, KitchenAid, or Jenn-Air upload, an event is logged.
- Events include user ID, appliance ID, badge name, reason, brand, and timestamp.

## Uses

- Enables audit trails for badge awards.
- Supports user-facing badge history and analytics.
- Can be used to reward top contributors or investigate disputes.

## Example Event

```json
{
  "user_id": "niko4244",
  "appliance_id": "maytag_dryer_003",
  "badge": "Schematic Uploader",
  "reason": "Uploaded a Maytag dryer schematic.",
  "brand": "maytag",
  "timestamp": "2025-08-09T04:05:47"
}
```

## Notes

- Only badge awards for supported brands are logged.
- Easy to extend to include more details or new badge types.

---