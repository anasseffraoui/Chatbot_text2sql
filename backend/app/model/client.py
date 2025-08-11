import os, requests
from ..config import settings

def call_model(prompt: str, timeout=60) -> str:
    headers = {"Authorization": f"Bearer {settings.HF_TOKEN}"}
    payload = {
        "model": settings.HF_MODEL,
        "messages": [{"role": "user", "content": prompt}]
    }
    r = requests.post(settings.FEATHERLESS_URL, headers=headers, json=payload, timeout=timeout)
    r.raise_for_status()
    data = r.json()
    msg = data.get("choices", [{}])[0].get("message", {}).get("content", "")
    return msg or ""
