def search_symbols(query: str, kb_path: str = "knowledge_base.json") -> List[Dict]:
    # ...existing code...
    for appliance_id, entry in kb.items():
        # Only include entries for allowed brands
        if not is_allowed_brand(appliance_id):
            continue
        # ...rest of logic...