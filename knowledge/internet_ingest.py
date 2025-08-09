from knowledge.brand_filter import is_allowed_brand
from knowledge.brand_sources import get_all_sources

def crawl_documentation(sources: list = None, download_dir: str = "internet_docs") -> list:
    """
    Crawl only official documentation for supported brands.
    """
    if sources is None:
        sources = get_all_sources()
    # ...existing crawl logic (filtered to sources for allowed brands)...
    # rest of function unchanged

def index_and_extract_from_internet(docs: list) -> list:
    """
    Index only documents for supported brands.
    """
    extracted = []
    from docs.tech_sheet_ingest import extract_symbols_and_diagrams, add_to_knowledge_base
    for doc in docs:
        # Use filename or extracted text to check for allowed brands
        if not is_allowed_brand(doc):
            continue
        sheet_data = extract_symbols_and_diagrams(doc)
        appliance_id = f"auto_{os.path.splitext(os.path.basename(doc))[0]}"
        add_to_knowledge_base(appliance_id, sheet_data)
        extracted.append({"appliance_id": appliance_id, "data": sheet_data})
    return extracted