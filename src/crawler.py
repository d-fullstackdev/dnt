"""
Unified Extraction & Crawler Module for Celios 9 Danantara Monitor
Combines:
- Puppeteer Stealth (Node.js runner for hard Cloudflare/WAF paywalls)
- curl_cffi (Fast TLS/JA3 impersonation for standard Cloudflare domains)
- Google News RSS (Zero-ban syndication feed for targeted media monitoring)
- Direct HTTPX poller for regulatory portals

Complies strictly with .agents/rules
"""

import os
import json
import subprocess
import urllib.parse
from typing import Dict, List, Optional
import feedparser
from curl_cffi import requests as cffi_requests
import httpx

WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STEALTH_FETCHER_JS = os.path.join(WORKSPACE_ROOT, "tools", "puppeteer_engine", "stealth_fetcher.js")

# List of domains known for strict Cloudflare/PerimeterX/Akamai WAF
STRICT_WAF_DOMAINS = [
    "bloomberg.com",
    "bloombergtechnoz.com",
    "reuters.com",
    "kompas.id",
    "thejakartapost.com",
    "spglobal.com",
    "moodys.com"
]

def is_strict_waf_domain(url: str) -> bool:
    parsed = urllib.parse.urlparse(url)
    domain = parsed.netloc.lower()
    return any(waf_d in domain for waf_d in STRICT_WAF_DOMAINS)

def fetch_with_puppeteer(url: str, output_path: Optional[str] = None, headless: bool = True) -> Dict:
    """Invokes Puppeteer Stealth runner via Node.js subprocess to bypass tough WAF/Cloudflare challenges."""
    cmd = ["node", STEALTH_FETCHER_JS, url]
    if output_path:
        cmd.append(output_path)
    if not headless:
        cmd.append("--headless=false")
        
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60,
            cwd=WORKSPACE_ROOT
        )
        if proc.returncode != 0:
            return {"success": False, "url": url, "error": proc.stderr.strip()}
            
        if output_path and os.path.exists(output_path):
            with open(output_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # Parse from stdout
            lines = proc.stdout.strip().split("\n")
            for line in reversed(lines):
                if line.startswith("{") and line.endswith("}"):
                    return json.loads(line)
            return {"success": True, "raw_stdout": proc.stdout}
    except Exception as e:
        return {"success": False, "url": url, "error": str(e)}

def fetch_with_curl_cffi(url: str, timeout: int = 15) -> Dict:
    """Fast TLS fingerprint (JA3/Chrome 124) impersonation request."""
    try:
        session = cffi_requests.Session(impersonate="chrome124")
        resp = session.get(url, timeout=timeout)
        return {
            "success": resp.status_code == 200,
            "status": resp.status_code,
            "url": str(resp.url),
            "text": resp.text,
            "text_length": len(resp.text)
        }
    except Exception as e:
        return {"success": False, "url": url, "error": str(e)}

def smart_fetch(url: str, output_path: Optional[str] = None) -> Dict:
    """
    Intelligent routing:
    - If domain is known strict WAF -> uses Puppeteer Stealth directly
    - Otherwise -> attempts curl_cffi Chrome 124 impersonation first
    - If curl_cffi hits 403/Cloudflare -> seamlessly falls back to Puppeteer Stealth
    """
    if is_strict_waf_domain(url):
        return fetch_with_puppeteer(url, output_path=output_path, headless=True)
    
    # Try fast curl_cffi first
    res = fetch_with_curl_cffi(url)
    if res.get("success") and res.get("status") == 200:
        # Check if response text looks like a Cloudflare challenge
        lower_txt = res.get("text", "").lower()
        if "just a moment..." in lower_txt or "cf-browser-verification" in lower_txt:
            # WAF challenge triggered, elevate to Puppeteer
            return fetch_with_puppeteer(url, output_path=output_path, headless=True)
        return res
    else:
        # Elevated fallback
        return fetch_with_puppeteer(url, output_path=output_path, headless=True)

def query_google_news_rss(domain: str, query: str = "Danantara") -> List[Dict]:
    """
    Fetches Google News RSS search feed for a specific target domain.
    Returns cleaned list of news metadata without rate-limits or IP bans.
    """
    q_encoded = urllib.parse.quote(f'"{query}" site:{domain}')
    rss_url = f"https://news.google.com/rss/search?q={q_encoded}&hl=id&gl=ID&ceid=ID:id"
    
    feed = feedparser.parse(rss_url)
    articles = []
    
    for entry in feed.entries:
        title = getattr(entry, "title", "")
        link = getattr(entry, "link", "")
        published = getattr(entry, "published", "")
        summary = getattr(entry, "summary", "")
        source = getattr(entry, "source", {}).get("title", domain) if hasattr(entry, "source") else domain
        
        articles.append({
            "title": title,
            "target_domain": domain,
            "url": link,
            "published_at": published,
            "publisher": source,
            "snippet": summary,
            "query_used": query
        })
        
    return articles
