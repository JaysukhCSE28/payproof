"""Optional Gemini client wrapper with truthful local fallback."""

import json
from typing import Dict, Any, Optional
from backend.app.config import settings


def extract_with_gemini(raw_text: str) -> Optional[Dict[str, Any]]:
    """
    Attempt structured extraction with Gemini API if key is available.
    Returns None if API key is empty or API fails, allowing local fallback.
    """
    if not settings.gemini_api_key or settings.gemini_api_key.startswith("your_"):
        return None

    try:
        import urllib.request
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={settings.gemini_api_key}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{
                "parts": [{
                    "text": f"Extract JSON fields (trip_id, vendor, distance_km, claimed_fare_inr) from: {raw_text}"
                }]
            }]
        }
        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
        with urllib.request.urlopen(req, timeout=5) as response:
            res_data = json.loads(response.read().decode())
            candidate = res_data["candidates"][0]["content"]["parts"][0]["text"]
            # Find JSON block
            if "{" in candidate and "}" in candidate:
                json_str = candidate[candidate.find("{"):candidate.rfind("}")+1]
                return json.loads(json_str)
    except Exception:
        pass
    return None
