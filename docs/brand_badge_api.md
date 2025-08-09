# Brand-Specific Badge API

## Endpoints

- `GET /badges?user_id={userid}`
  - Returns badge history for a user, filtered to Whirlpool, Maytag, KitchenAid, and Jenn-Air related contributions.
  - Includes badge names and descriptions.

- `GET /badges/all`
  - Returns descriptions for all possible badges awarded for supported brand uploads.

## Badges

- **Symbol Scout:** Tech sheets with 5+ unique symbols.
- **Schematic Uploader:** At least 1 schematic or wiring diagram uploaded.
- **Documentation Champion:** 500+ characters of useful text.

## How It Works

- Only badges earned through supported brand contributions are shown.
- Keeps gamification focused on business-relevant content.

## Example Response

```json
{
  "badges": ["Symbol Scout", "Documentation Champion"],
  "details": {
    "Symbol Scout": "Awarded for uploading tech sheets with 5 or more unique symbols.",
    "Schematic Uploader": "Awarded for uploading at least one schematic or wiring diagram.",
    "Documentation Champion": "Awarded for uploading tech sheets with over 500 characters of useful text."
  }
}
```

---