"""
Brand Validation for Document Uploads and Extraction
- Ensures only Whirlpool, Maytag, KitchenAid, and Jenn-Air appliances are accepted for ingestion.
"""

ALLOWED_BRANDS = ["whirlpool", "maytag", "kitchenaid", "jenn-air"]

def extract_brand_from_text(text: str) -> str:
    """
    Extract brand from given text using keyword matching.
    Args:
        text (str): Text from tech sheet/manual.
    Returns:
        str: Brand name if found, else empty string.
    """
    text_lower = text.lower()
    for brand in ALLOWED_BRANDS:
        if brand in text_lower:
            return brand
    return ""

def validate_brand_for_upload(text: str) -> bool:
    """
    Validate if the extracted text contains a supported brand.
    Args:
        text (str): Extracted text from tech sheet.
    Returns:
        bool: True if brand is allowed, False otherwise.
    """
    return bool(extract_brand_from_text(text))

# Example usage:
if __name__ == "__main__":
    sample_text = "Whirlpool Cabrio Washer Model WTW8500DC"
    print(validate_brand_for_upload(sample_text))  # True
    print(extract_brand_from_text(sample_text))    # whirlpool