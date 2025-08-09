# Brand-Specific Crawling and Knowledge Base Strategy

## Supported Brands
- Whirlpool
- Maytag
- KitchenAid
- Jenn-Air

## Official Documentation Sources

Crawling and ingestion are limited to the following official documentation portals:
- [Whirlpool Manuals & Support](https://www.whirlpool.com/support/)
- [Maytag Manuals & Support](https://www.maytag.com/support/)
- [KitchenAid Manuals & Support](https://www.kitchenaid.com/support/)
- [Jenn-Air Manuals & Support](https://www.jennair.com/support/)

## How It Works

- **Internet Ingestion:**  
  Scheduled crawls only target official support and manual pages from the four brands.
- **Brand Filtering:**  
  Any document, schematic, or tech sheet added to the knowledge base is verified by filename, metadata, or extracted text for brand.
- **Search & Results:**  
  User and technician searches only return results for supported brands, ensuring relevance and compliance.

## Example

- Uploads, crawls, and search results for "Whirlpool Cabrio Washer" are accepted and indexed.
- Documentation for "Samsung Dryer" or "LG Refrigerator" is ignored or rejected.

## Maintenance

- Easily extend the sources if Whirlpool, Maytag, KitchenAid, or Jenn-Air add new documentation portals.
- Update the brand filter if your service scope changes.

---