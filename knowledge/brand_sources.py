"""
Official Documentation Sources for Supported Brands
- Whirlpool, Maytag, KitchenAid, Jenn-Air
- Centralizes URLs for targeted crawling and knowledge base expansion.
"""

BRAND_DOC_SOURCES = {
    "whirlpool": [
        "https://www.whirlpool.com/services/manuals.html",
        "https://www.whirlpool.com/support/",
    ],
    "maytag": [
        "https://www.maytag.com/services/manuals.html",
        "https://www.maytag.com/support/",
    ],
    "kitchenaid": [
        "https://www.kitchenaid.com/services/manuals.html",
        "https://www.kitchenaid.com/support/",
    ],
    "jenn-air": [
        "https://www.jennair.com/services/manuals.html",
        "https://www.jennair.com/support/",
    ]
}

def get_brand_sources(brand: str) -> list:
    """
    Return official documentation sources for a given brand.
    Args:
        brand (str): Brand name (case-insensitive).
    Returns:
        list of str: URLs.
    """
    return BRAND_DOC_SOURCES.get(brand.lower(), [])

def get_all_sources() -> list:
    """
    Return all official documentation sources for supported brands.
    Returns:
        list of str: URLs.
    """
    all_sources = []
    for srcs in BRAND_DOC_SOURCES.values():
        all_sources.extend(srcs)
    return all_sources

# Example usage:
if __name__ == "__main__":
    print(get_all_sources())