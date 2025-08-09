# (extend upload workflow to award badges and log badge events)
from knowledge.gamification import award_contribution_badge

@app.post("/techsheet/upload/{appliance_id}")
async def upload_tech_sheet(appliance_id: str, file: UploadFile = File(...), user_id: str = "unknown"):
    # Save file temporarily
    temp_path = f"temp_upload_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())
    # Extract symbols, diagrams, and text
    sheet_data = extract_symbols_and_diagrams(temp_path)
    # Brand validation
    brand = extract_brand_from_text(sheet_data.get("text", ""))
    if not brand:
        raise HTTPException(
            status_code=400,
            detail="Upload failed: Only Whirlpool, Maytag, KitchenAid, and Jenn-Air appliances are accepted."
        )
    # Save and index document
    saved_path = save_uploaded_sheet(temp_path)
    add_to_knowledge_base(appliance_id, sheet_data)
    # Award badges and log badge events for gamification
    sheet_data["brand"] = brand
    award_contribution_badge(user_id, appliance_id, sheet_data)
    # Log upload for analytics
    log_search(brand, user_id)
    return {
        "message": f"Tech sheet for {brand.title()} appliance ingested successfully.",
        "symbols": sheet_data["symbols"],
        "diagrams": sheet_data["diagrams"],
        "brand": brand
    }