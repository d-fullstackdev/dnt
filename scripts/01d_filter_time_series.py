"""
Script 01d: Time-Series Bounding Filter
Enforces strict time-series criteria from ref/brief-20260831_Methodological Approach.md:
1. Green Projects (Track B): Announced 2020 onwards (year >= 2020)
2. Danantara Confirmed (Track A): Since launch in 2025 (year >= 2025)

Updates:
- data/raw/evidence_dorking/master_urls_manifest.csv (1,754 valid items)
- data/raw/evidence_dorking/urls_excluded_time_series.csv (93 auditable exclusions)

Complies strictly with .agents/rules
"""

import os
import pandas as pd
from dateutil import parser

MANIFEST_PATH = os.path.join("data", "raw", "evidence_dorking", "master_urls_manifest.csv")
EXCLUDED_PATH = os.path.join("data", "raw", "evidence_dorking", "urls_excluded_time_series.csv")

def filter_manifest_by_time_series():
    print("=" * 70)
    print("⏳ APPLYING TIME-SERIES BOUNDING RULES (TABITA BRIEF)")
    print("=" * 70)
    
    if not os.path.exists(MANIFEST_PATH):
        print(f"Error: {MANIFEST_PATH} not found!")
        return

    df = pd.read_csv(MANIFEST_PATH)
    print(f"Total manifest records before filter: {len(df)}")
    
    years = []
    for val in df['published_at']:
        try:
            dt = parser.parse(str(val))
            years.append(dt.year)
        except Exception:
            years.append(None)
            
    df['publication_year'] = years
    
    # Rule 1: Track B (Green SOE) >= 2020
    is_track_b_valid = (df['track'] == 'TRACK_B_GREEN_INVENTORY') & (df['publication_year'] >= 2020)
    # Rule 2: Track A (Danantara) >= 2025
    is_track_a_valid = (df['track'] == 'TRACK_A_DANANTARA_MONITOR') & (df['publication_year'] >= 2025)
    
    is_valid = is_track_b_valid | is_track_a_valid
    
    df_valid = df[is_valid].copy()
    df_excluded = df[~is_valid].copy()
    
    # Add exclusion reasons
    reasons = []
    for _, row in df_excluded.iterrows():
        track = row['track']
        yr = row['publication_year']
        if track == 'TRACK_A_DANANTARA_MONITOR':
            reasons.append(f"Pre-2025 article (year: {yr}) prior to Danantara official launch in 2025")
        else:
            reasons.append(f"Pre-2020 project announcement (year: {yr}) prior to 2020 brief mandate")
    df_excluded['exclusion_reason'] = reasons
    
    # Re-index clean IDs for valid manifest
    df_valid.drop(columns=['evidence_id', 'publication_year'], inplace=True, errors='ignore')
    df_valid.insert(0, 'evidence_id', [f"EVID-DNT-{i+1:04d}" for i in range(len(df_valid))])
    
    # Save clean manifest
    df_valid.to_csv(MANIFEST_PATH, index=False, encoding='utf-8')
    print(f"✓ Valid Time-Series Manifest saved to: {MANIFEST_PATH}")
    print(f"  Total Valid Articles: {len(df_valid)}")
    print(f"  Track Breakdown:\n{df_valid['track'].value_counts()}")
    
    # Save exclusion audit file
    df_excluded.to_csv(EXCLUDED_PATH, index=False, encoding='utf-8')
    print(f"\n✓ Excluded Audit Trail saved to: {EXCLUDED_PATH}")
    print(f"  Total Excluded Articles: {len(df_excluded)}")
    print(f"  Excluded Track Breakdown:\n{df_excluded['track'].value_counts()}")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    filter_manifest_by_time_series()
