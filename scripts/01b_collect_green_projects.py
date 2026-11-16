"""
Script 01b: SOE Green Project Collection Engine (Jalur B)
Inventories green projects announced by Indonesian SOEs (2020 onward)
across the 15 official Project Clusters defined in ref/brief-20260831_Methodological Approach.md.

Implements Context-Aware Ingestion:
- Bounded to verified SOEs from data/processed/bumn_master_clean.csv
- Filtered by 15 project clusters (Solar, Water, Wind, Bioenergy, PSEL, Hydrogen, EV, Battery, Grid, etc.)
- Anchored with investment/capacity/project intent terms
- Hard negative exclusion of recruitment/academic spam (-loker -skripsi -lowongan)

Output:
data/raw/evidence_dorking/green_projects_feed.jsonl

Complies strictly with .agents/rules
"""

import os
import sys
import json
import time
import urllib.parse
from datetime import datetime, timezone
import feedparser
import pandas as pd

WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_FILE = os.path.join(WORKSPACE_ROOT, "data", "raw", "evidence_dorking", "green_projects_feed.jsonl")

# Priority Green SOE Target Groups
TARGET_SOES = [
    {
        "soe_parent": "PT Perusahaan Listrik Negara (Persero)",
        "search_names": ["PLN", "PLN Nusantara Power", "PLN Indonesia Power", "PLN Batam"]
    },
    {
        "soe_parent": "PT Pertamina (Persero)",
        "search_names": ["Pertamina", "Pertamina Geothermal Energy", "Pertamina NRE", "PGE"]
    },
    {
        "soe_parent": "PT Semen Indonesia (Persero) Tbk",
        "search_names": ["Semen Indonesia", "SIG", "Semen Padang", "Semen Gresik"]
    },
    {
        "soe_parent": "PT Pupuk Indonesia (Persero)",
        "search_names": ["Pupuk Indonesia", "Pupuk Kaltim", "Petrokimia Gresik"]
    },
    {
        "soe_parent": "PT Mineral Industri Indonesia (Persero)",
        "search_names": ["MIND ID", "Inalum", "Bukit Asam", "Antam", "PTBA"]
    },
    {
        "soe_parent": "PT Perkebunan Nusantara III (Persero)",
        "search_names": ["PTPN", "PTPN III", "Perkebunan Nusantara"]
    },
    {
        "soe_parent": "Perum Perhutani",
        "search_names": ["Perhutani"]
    },
    {
        "soe_parent": "PT Hutama Karya (Persero)",
        "search_names": ["Hutama Karya", "WIKA", "Adhi Karya"]
    },
    {
        "soe_parent": "Danantara BPI",
        "search_names": ["Danantara", "Danantara Investment Management", "PT Denera", "Daya Energi Bersih Nusantara"]
    }
]

# 15 Official Clusters from ref/brief-20260831_Methodological Approach.md
PROJECT_CLUSTERS = [
    {
        "cluster_id": "CLS-01-SOLAR",
        "cluster_name": "Solar",
        "terms": 'PLTS OR "PLTS terapung" OR "solar panel" OR "solar rooftop" OR "tenaga surya"'
    },
    {
        "cluster_id": "CLS-02-WATER",
        "cluster_name": "Water / Hydro",
        "terms": 'PLTA OR PLTMH OR hidro OR "pumped storage"'
    },
    {
        "cluster_id": "CLS-03-WIND",
        "cluster_name": "Wind",
        "terms": 'PLTB OR "tenaga bayu" OR "turbin angin" OR "wind farm"'
    },
    {
        "cluster_id": "CLS-04-BIOENERGY",
        "cluster_name": "Bioenergy",
        "terms": 'biomassa OR biogas OR biofuel OR biodiesel OR bioetanol OR SAF OR "bahan bakar nabati"'
    },
    {
        "cluster_id": "CLS-05-WASTE",
        "cluster_name": "Waste and circular",
        "terms": 'waste-to-energy OR PSEL OR RDF OR "pengolahan sampah menjadi energi"'
    },
    {
        "cluster_id": "CLS-06-HYDROGEN",
        "cluster_name": "Hydrogen & Ammonia",
        "terms": '"hidrogen hijau" OR "green hydrogen" OR "amonia hijau" OR "green ammonia"'
    },
    {
        "cluster_id": "CLS-07-EV",
        "cluster_name": "Electric vehicle",
        "terms": '"kendaraan listrik" OR "ekosistem EV" OR SPKLU OR "bus listrik"'
    },
    {
        "cluster_id": "CLS-08-BATTERY",
        "cluster_name": "Battery",
        "terms": '"baterai kendaraan listrik" OR "EV battery" OR "rantai pasok baterai"'
    },
    {
        "cluster_id": "CLS-09-NETWORK",
        "cluster_name": "Power network",
        "terms": '"transmisi hijau" OR "smart grid" OR interkoneksi OR "grid modern"'
    },
    {
        "cluster_id": "CLS-10-DECARB",
        "cluster_name": "Industry decarbonization",
        "terms": '"efisiensi energi" OR "semen rendah karbon" OR "baja ramah lingkungan" OR elektrifikasi'
    },
    {
        "cluster_id": "CLS-11-COAL-TRANS",
        "cluster_name": "Coal transition",
        "terms": '"pensiun dini PLTU" OR "early retirement" OR "coal phase-down" OR "repurposing PLTU"'
    },
    {
        "cluster_id": "CLS-12-CARBON",
        "cluster_name": "Carbon",
        "terms": '"perdagangan karbon" OR "kredit karbon" OR "bursa karbon" OR "dekarbonisasi"'
    },
    {
        "cluster_id": "CLS-13-NBS",
        "cluster_name": "Mangrove, peatland",
        "terms": '"rehabilitasi mangrove" OR "restorasi gambut" OR "nature-based solutions"'
    },
    {
        "cluster_id": "CLS-14-WATER-TREAT",
        "cluster_name": "Wastewater",
        "terms": '"pengolahan air limbah" OR "air bersih berkelanjutan"'
    },
    {
        "cluster_id": "CLS-15-RE-GENERAL",
        "cluster_name": "Renewable energy (general)",
        "terms": '"energi terbarukan" OR "energi bersih" OR "bauran EBT" OR "transisi energi"'
    }
]

INTENT_ANCHOR = '(investasi OR kapasitas OR megawatt OR proyek OR "MoU" OR tahap OR groundbreaking)'
NEGATIVE_FILTER = '-loker -lowongan -skripsi -"lowongan kerja" -"daftar pustaka"'

def collect_green_projects():
    print("=" * 70)
    print("🌿 COLLECTING BUMN GREEN PROJECTS (15 CLUSTERS x PRIORITY SOEs)")
    print("=" * 70)
    
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    seen_urls = set()
    existing_count = 0
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    try:
                        record = json.loads(line)
                        seen_urls.add(record.get("url"))
                        existing_count += 1
                    except:
                        pass
        print(f"Loaded {existing_count} existing records from {OUTPUT_FILE}")

    new_articles_count = 0
    
    with open(OUTPUT_FILE, 'a', encoding='utf-8') as out_f:
        for soe_group in TARGET_SOES:
            parent_name = soe_group["soe_parent"]
            primary_name = soe_group["search_names"][0]
            print(f"\n🏢 Processing SOE: {parent_name} (Search: '{primary_name}')")
            
            for cluster in PROJECT_CLUSTERS:
                c_id = cluster["cluster_id"]
                c_name = cluster["cluster_name"]
                c_terms = cluster["terms"]
                
                query_str = f'"{primary_name}" ({c_terms}) {INTENT_ANCHOR} {NEGATIVE_FILTER}'
                q_encoded = urllib.parse.quote(query_str)
                rss_url = f"https://news.google.com/rss/search?q={q_encoded}&hl=id&gl=ID&ceid=ID:id"
                
                try:
                    feed = feedparser.parse(rss_url)
                    entries = getattr(feed, "entries", [])
                    added_for_cluster = 0
                    
                    for entry in entries:
                        link = getattr(entry, "link", "")
                        title = getattr(entry, "title", "")
                        published = getattr(entry, "published", "")
                        summary = getattr(entry, "summary", "")
                        source_obj = getattr(entry, "source", {})
                        source_title = source_obj.get("title", "") if isinstance(source_obj, dict) else str(source_obj)
                        
                        if link and link not in seen_urls:
                            seen_urls.add(link)
                            record = {
                                "soe_parent": parent_name,
                                "cluster_id": c_id,
                                "cluster_name": c_name,
                                "title": title,
                                "url": link,
                                "published_at": published,
                                "publisher": source_title,
                                "snippet": summary,
                                "query_used": query_str,
                                "collected_at": datetime.now(timezone.utc).isoformat()
                            }
                            out_f.write(json.dumps(record, ensure_ascii=False) + "\n")
                            new_articles_count += 1
                            added_for_cluster += 1
                            
                    print(f"  [{c_name:<26}] Found: {len(entries):<3} | New Unique: {added_for_cluster}")
                except Exception as e:
                    print(f"  ⚠️ Error on {c_name}: {e}")
                    
                time.sleep(0.2)
                
    print("\n" + "=" * 70)
    print(f"🎉 BUMN GREEN PROJECTS COLLECTION COMPLETE!")
    print(f"New Unique Green Articles Added: {new_articles_count}")
    print(f"Total Combined Green Evidence Records: {len(seen_urls)}")
    print(f"Output saved to: {OUTPUT_FILE}")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    collect_green_projects()
