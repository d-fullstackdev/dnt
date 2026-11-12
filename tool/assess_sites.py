import requests
import json
import time

urls = [
    "https://www.danantaraindonesia.co.id/",
    "https://jdih.setneg.go.id/",
    "https://peraturan.bpk.go.id/",
    "https://www.setneg.go.id/",
    "https://presidenri.go.id/",
    "https://setkab.go.id/",
    "https://www.kompas.id/",
    "https://www.kontan.co.id/",
    "https://www.bisnis.com/",
    "https://www.thejakartapost.com/",
    "https://www.kompas.com/",
    "https://www.cnbcindonesia.com/",
    "https://www.detik.com/",
    "https://www.reuters.com/",
    "https://www.bloombergtechnoz.com/",
    "https://www.bloomberg.com/",
    "https://www.spglobal.com/ratings/en",
    "https://www.moodys.com/researchandratings/region/asia-pacific/indonesia/0420AE"
]

results = []
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

for url in urls:
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        status = resp.status_code
        text = resp.text.lower()
        
        # Analyze outcome
        can_fetch = False
        error_reason = ""
        
        if status == 200:
            if "cloudflare" in text or "attention required" in text or "verify you are human" in text or "security check" in text:
                error_reason = "Terblokir Cloudflare / Bot Protection"
            else:
                can_fetch = True
                error_reason = "Aman (Bisa di-scrape)"
        elif status == 403:
            error_reason = "403 Forbidden (Terblokir Anti-Bot/Cloudflare)"
        elif status == 404:
            error_reason = "404 Not Found"
        elif status == 429:
            error_reason = "429 Too Many Requests (Rate Limited)"
        else:
            error_reason = f"Error {status}"
            
        results.append({
            "url": url,
            "status": status,
            "can_fetch": can_fetch,
            "reason": error_reason
        })
    except requests.exceptions.RequestException as e:
        results.append({
            "url": url,
            "status": "Failed",
            "can_fetch": False,
            "reason": "Connection Error / Timeout"
        })
    
    time.sleep(1) # Be polite

with open(r"C:\Users\yooma\OneDrive\Desktop\duniahub\client\28. Celios9-danantara\tool\assessment_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=4)

print("Assessment complete. Results saved to JSON.")
