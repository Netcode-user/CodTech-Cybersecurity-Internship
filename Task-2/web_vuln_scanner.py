import requests
from bs4 import BeautifulSoup

xss_payload = "<script>alert('XSS')</script>"
sql_payload = "' OR '1'='1"

def scan_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        forms = soup.find_all('form')
        print(f"Found {len(forms)} form(s). Scanning...")

        for form in forms:
            action = form.get("action")
            method = form.get("method", "get").lower()
            inputs = form.find_all("input")
            data = {inp.get("name"): xss_payload for inp in inputs if inp.get("name")}
            full_url = url if not action else requests.compat.urljoin(url, action)

            if method == "post":
                resp = requests.post(full_url, data=data)
            else:
                resp = requests.get(full_url, params=data)

            if xss_payload in resp.text:
                print(f"[VULNERABLE TO XSS] in {full_url}")
            if "sql" in resp.text.lower() or "error" in resp.text.lower():
                print(f"[POSSIBLE SQL INJECTION] in {full_url}")
    except Exception as e:
        print("Error:", e)

# Example:
# scan_url("http://testphp.vulnweb.com")
