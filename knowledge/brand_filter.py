"""
Brand Filtering for Knowledge Ingestion and Search
- Restricts crawling, indexing, and searching to Whirlpool, Maytag, KitchenAid, and Jenn-Air appliances.
"""

ALLOWED_BRANDS = ["whirlpool", "maytag", "kitchenaid", "jenn-air"]

def is_allowed_brand(appliance_name: str) -> bool:
    """
    Check if the appliance belongs to an allowed brand.
    Args:
        appliance_name (str): Full appliance model or description.
    Returns:
        bool: True if allowed brand, else False.
    """
    name_lower = appliance_name.lower()
    return any(brand in name_lower for brand in ALLOWED_BRANDS)

# Example usage:
if __name__ == "__main__":
    print(is_allowed_brand("Whirlpool Cabrio Washer"))  # True
    print(is_allowed_brand("Samsung Dryer"))            # False