"""
Script 04: Local Clean Markdown Extraction (Langkah 4 / Phase 2)
Parses full raw HTML files from disk into clean, normalized Markdown text.

Key Principles:
1. 100% Offline: Reads strictly from data/raw/evidence_dorking/html/ (zero network calls).
2. Trafilatura Engine: Strips boilerplate, ads, navigation menus, and footers while preserving text structure.
3. Fallback Parser: BeautifulSoup text extraction if Trafilatura produces insufficient body text (< 50 words).
4. Output: data/processed/articles_clean_text.jsonl
   - Fields: evidence_id, track, title, publisher, published_at, canonical_url, word_count, body_markdown
5. Audit & Manifest Integrity: Re-checks against master_urls_manifest.csv.

Complies strictly with .agents/rules
"""

import os
import sys
import json
import re
import pandas as pd
from bs4 import BeautifulSoup
import trafilatura

WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST_PATH = os.path.join(WORKSPACE_ROOT, "data", "raw", "evidence_dorking", "master_urls_manifest.csv")
HTML_DIR = os.path.join(WORKSPACE_ROOT, "data", "raw", "evidence_dorking", "html")
LOG_PATH = os.path.join(WORKSPACE_ROOT, "data", "raw", "evidence_dorking", "html_download_log.csv")
OUTPUT_JSONL = os.path.join(WORKSPACE_ROOT, "data", "processed", "articles_clean_text.jsonl")
OUTPUT_STATS = os.path.join(WORKSPACE_ROOT, "data", "processed", "extraction_stats.csv")

def clean_with_soup(html_text: str) -> str:
    """Fallback text extractor using BeautifulSoup."""
    soup = BeautifulSoup(html_text, 'lxml')
    # Remove script, style, nav, footer, aside, header tags
    for tag in soup(["script", "style", "nav", "footer", "aside", "header", "noscript", "iframe"]):
        tag.decompose()
        
    paragraphs = []
    # Target article containers or p tags
    for p in soup.find_all('p'):
        text = p.get_text(separator=' ', strip=True)
        if len(text) > 25: # Filter out short UI fragments
            paragraphs.append(text)
            
    if not paragraphs:
        text = soup.get_text(separator='\n', strip=True)
        lines = [line.strip() for line in text.splitlines() if len(line.strip()) > 30]
        return "\n\n".join(lines)
        
    return "\n\n".join(paragraphs)

def extract_markdown_from_html(html_text: str) -> tuple[str, str]:
    """
    Extracts clean markdown body text.
    Returns (body_markdown, extraction_method).
    """
    # 1. Primary: Trafilatura
    try:
        extracted = trafilatura.extract(
            html_text,
            include_links=False,
            include_images=False,
            include_tables=True,
            output_format="markdown",
            favor_precision=True
        )
        if extracted and len(extracted.split()) >= 40:
            return extracted.strip(), "trafilatura"
    except Exception:
        pass
        
    # 2. Fallback: BeautifulSoup
    soup_text = clean_with_soup(html_text)
    if soup_text and len(soup_text.split()) >= 25:
        return soup_text.strip(), "beautifulsoup_fallback"
        
    return "", "insufficient_content"

def run_extraction_pipeline():
    print("=" * 75)
    print("🧹 EXECUTING LANGKAH 4: OFFLINE CLEAN MARKDOWN EXTRACTION")
    print("=" * 75)
    
    if not os.path.exists(MANIFEST_PATH):
        print(f"❌ Manifest not found at {MANIFEST_PATH}")
        return
        
    df_manifest = pd.read_csv(MANIFEST_PATH)
    total_manifest = len(df_manifest)
    print(f"Total manifest articles: {total_manifest}")
    
    # Load canonical URLs from download log if available
    url_map = {}
    if os.path.exists(LOG_PATH):
        try:
            df_log = pd.read_csv(LOG_PATH)
            for _, r in df_log.iterrows():
                if r.get("status") == "SUCCESS" and pd.notna(r.get("canonical_url")):
                    url_map[str(r["evidence_id"])] = str(r["canonical_url"])
        except Exception:
            pass
            
    os.makedirs(os.path.dirname(OUTPUT_JSONL), exist_ok=True)
    
    records = []
    stats_list = []
    trafilatura_count = 0
    soup_count = 0
    empty_count = 0
    missing_file_count = 0
    
    for idx, row in df_manifest.iterrows():
        ev_id = str(row["evidence_id"])
        track = str(row.get("track", ""))
        title = str(row.get("title", ""))
        publisher = str(row.get("publisher", ""))
        published_at = str(row.get("published_at", ""))
        gnews_url = str(row.get("url", ""))
        canonical_url = url_map.get(ev_id, gnews_url)
        
        html_file = os.path.join(HTML_DIR, f"{ev_id}.html")
        
        if not os.path.exists(html_file):
            missing_file_count += 1
            stats_list.append({
                "evidence_id": ev_id,
                "status": "MISSING_HTML",
                "method": "none",
                "word_count": 0,
                "file_size_bytes": 0
            })
            continue
            
        file_size = os.path.getsize(html_file)
        if file_size < 500:
            missing_file_count += 1
            stats_list.append({
                "evidence_id": ev_id,
                "status": "HTML_TOO_SMALL",
                "method": "none",
                "word_count": 0,
                "file_size_bytes": file_size
            })
            continue
            
        with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
            html_content = f.read()
            
        body_md, method = extract_markdown_from_html(html_content)
        word_count = len(body_md.split())
        
        if method == "trafilatura":
            trafilatura_count += 1
        elif method == "beautifulsoup_fallback":
            soup_count += 1
        else:
            empty_count += 1
            
        if word_count >= 25:
            record = {
                "evidence_id": ev_id,
                "track": track,
                "title": title,
                "publisher": publisher,
                "published_at": published_at,
                "canonical_url": canonical_url,
                "word_count": word_count,
                "body_markdown": body_md
            }
            records.append(record)
            stats_list.append({
                "evidence_id": ev_id,
                "status": "SUCCESS",
                "method": method,
                "word_count": word_count,
                "file_size_bytes": file_size
            })
        else:
            stats_list.append({
                "evidence_id": ev_id,
                "status": "LOW_WORD_COUNT",
                "method": method,
                "word_count": word_count,
                "file_size_bytes": file_size
            })
            
    # Save clean JSONL
    with open(OUTPUT_JSONL, 'w', encoding='utf-8') as out_f:
        for r in records:
            out_f.write(json.dumps(r, ensure_ascii=False) + "\n")
            
    # Save stats
    pd.DataFrame(stats_list).to_csv(OUTPUT_STATS, index=False, encoding='utf-8')
    
    print("-" * 75)
    print("📊 EXTRACTION SUMMARY:")
    print(f"Total Processed from Manifest: {total_manifest}")
    print(f"Successfully Extracted Articles: {len(records)} ({(len(records)/total_manifest)*100:.1f}%)")
    print(f"  - Extracted via Trafilatura: {trafilatura_count}")
    print(f"  - Extracted via BeautifulSoup Fallback: {soup_count}")
    print(f"  - Low word count (<25 words): {empty_count}")
    print(f"  - Missing or undersized HTML: {missing_file_count}")
    print(f"Output Dataset: {OUTPUT_JSONL}")
    print(f"Extraction Statistics: {OUTPUT_STATS}")
    print("=" * 75 + "\n")

if __name__ == "__main__":
    run_extraction_pipeline()
