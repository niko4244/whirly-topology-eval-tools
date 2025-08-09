# Brand-Filtered Symbol & Schematic Search API

## Endpoints

- `GET /search/symbols?query={keyword}`  
  Returns all matching symbols/components for Whirlpool, Maytag, KitchenAid, and Jenn-Air appliances only.

- `GET /search/diagrams?query={keyword}`  
  Returns all matching schematics/diagrams for supported brands only.

## How It Works

- All search results are filtered to show only appliances from the four supported brands.
- This ensures technicians only receive relevant, compliant information.

## Example Use Case

- Searching for "relay" will only show diagrams and symbols from Whirlpool, Maytag, KitchenAid, and Jenn-Air.
- Searching for "motor" will exclude results from any non-supported brand, even if found in the knowledge base.

## Maintenance

- The brand filter is automatically applied to all endpoints.
- Easy to update if brand list changes.

---