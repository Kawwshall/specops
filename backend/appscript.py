import os
import base64
import httpx

URL    = os.environ["APPSCRIPT_URL"]
SECRET = os.environ["APPSCRIPT_SECRET"]

def submit(payload: dict, pan_bytes: bytes | None, pan_name: str, pan_mime: str) -> dict:
    body = {"secret": SECRET, **payload}
    if pan_bytes is not None:
        body["pan_b64"]  = base64.b64encode(pan_bytes).decode("ascii")
        body["pan_name"] = pan_name
        body["pan_mime"] = pan_mime
    # Apps Script web apps redirect the POST to a googleusercontent URL; follow it.
    r = httpx.post(URL, json=body, timeout=120, follow_redirects=True)
    r.raise_for_status()
    data = r.json()
    if data.get("error"):
        raise RuntimeError(f"apps script: {data['error']}")
    return data
