import urllib.request

for url in ["http://127.0.0.1:3000", "http://127.0.0.1:8000/docs", "http://127.0.0.1:8000/api/v1/triad/evaluate/NABIL"]:
    try:
        with urllib.request.urlopen(url, timeout=3) as resp:
            print(f"GET {url} -> Status {resp.status} OK")
    except Exception as e:
        print(f"GET {url} -> Failed: {e}")
