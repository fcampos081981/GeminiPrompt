#!/usr/bin/env python3
import os
import sys
import json
import time
from typing import Any, Dict, List, Optional

import requests

API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
TIMEOUT_SECONDS = 30
RETRIES = 2
BACKOFF_SECONDS = 1.5


def get_api_key() -> str:
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise RuntimeError(
            "Missing GEMINI_API_KEY environment variable. "
            "Set it before running, e.g., export GEMINI_API_KEY='your_key_here'"
        )
    return key


def build_request(prompt: str) -> Dict[str, Any]:
    return {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }


def extract_text(resp_json: Dict[str, Any]) -> Optional[str]:

    try:
        candidates = resp_json.get("candidates", [])
        if not candidates:
            return None
        parts: List[Dict[str, Any]] = candidates[0].get("content", {}).get("parts", [])
        texts = [p.get("text") for p in parts if isinstance(p, dict) and "text" in p]
        # Join in case model returns multiple parts
        return "\n".join(t for t in texts if isinstance(t, str))
    except Exception:
        return None


def request_gemini(prompt: str) -> str:
    api_key = get_api_key()
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": api_key,
    }
    payload = build_request(prompt)

    last_error: Optional[str] = None
    for attempt in range(1, RETRIES + 2):
        try:
            resp = requests.post(API_URL, headers=headers, data=json.dumps(payload), timeout=TIMEOUT_SECONDS)
            if resp.status_code == 200:
                data = resp.json()
                text = extract_text(data)
                if text:
                    return text

                last_error = f"Empty or unexpected response format: {json.dumps(data)[:500]}..."
            else:

                try:
                    data = resp.json()
                except Exception:
                    data = None
                if isinstance(data, dict):
                    err_msg = data.get("error", {}).get("message") or data
                    last_error = f"HTTP {resp.status_code}: {err_msg}"
                else:
                    last_error = f"HTTP {resp.status_code}: {resp.text[:500]}..."
        except requests.Timeout:
            last_error = f"Request timed out after {TIMEOUT_SECONDS}s."
        except requests.RequestException as e:
            last_error = f"Network error: {e}"

        if attempt <= RETRIES:
            time.sleep(BACKOFF_SECONDS * attempt)

    raise RuntimeError(last_error or "Failed to get a valid response from Gemini.")


def main(argv: List[str]) -> int:
    if len(argv) < 2:
        print(f"Usage: {argv[0]} 'your prompt here'")
        return 1

    prompt = " ".join(argv[1:]).strip()
    if not prompt:
        print("Error: prompt must not be empty.")
        return 1

    try:
        result = request_gemini(prompt)
        print(result)
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))