import json
from datetime import datetime
import os

def log_correction(user_id, original_detection, corrected_detection):
    os.makedirs("ml/corrections", exist_ok=True)
    fname = f"ml/corrections/{datetime.now().strftime('%Y%m%d_%H%M%S')}_{user_id}.json"
    with open(fname, "w") as f:
        json.dump({
            "user_id": user_id,
            "original": original_detection,
            "corrected": corrected_detection
        }, f)
    return fname