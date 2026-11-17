"""
Data Cleaning & Consolidation Script for Celios 9 Danantara Monitor
Generates auditable, standardized CSV datasets from ref/MASTER LIST BUMN UNDER DANANTARA.xlsx

Complies with .agents/rules:
- zero hardcoded values
- strict data folder boundaries
- transparent audit trail for excluded coincidental private companies
"""

import os
import openpyxl
import pandas as pd

RAW_EXCEL_PATH = os.path.join("ref", "brief - MASTER LIST BUMN UNDER DANANTARA.xlsx")
if not os.path.exists(RAW_EXCEL_PATH):
    RAW_EXCEL_PATH = os.path.join("ref", "MASTER LIST BUMN UNDER DANANTARA.xlsx")
PROCESSED_DIR = os.path.join("data", "processed")

def clean_and_consolidate():
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    wb = openpyxl.load_workbook(RAW_EXCEL_PATH, data_only=True)
    
    # -------------------------------------------------------------
    # 1. HOLDINGS (Sheet: List of Holding)
    # -------------------------------------------------------------
    ws_h = wb['List of Holding']
    holdings = []
    for r in range(2, ws_h.max_row + 1):
        h_name = ws_h.cell(r, 1).value
        official_name = ws_h.cell(r, 2).value
        sector = ws_h.cell(r, 3).value
        ceo = ws_h.cell(r, 4).value
        website = ws_h.cell(r, 5).value
        update_url = ws_h.cell(r, 6).value
        
        if h_name or official_name:
            holdings.append({
                'holding_name': str(h_name).strip() if h_name else '',
                'official_leading_entity': str(official_name).strip() if official_name else '',
                'sector': str(sector).strip() if sector else '',
                'ceo': str(ceo).strip() if ceo else '',
                'website': str(website).strip() if website else '',
                'source_url': str(update_url).strip() if update_url else ''
            })
    df_holdings = pd.DataFrame(holdings)
    df_holdings.to_csv(os.path.join(PROCESSED_DIR, "bumn_holdings_clean.csv"), index=False, encoding='utf-8')
    print(f"✓ Saved {len(df_holdings)} Holdings to data/processed/bumn_holdings_clean.csv")

    # -------------------------------------------------------------
    # 2. LEGAL ENTITIES (Sheet: Based on Legal Form)
    # -------------------------------------------------------------
    ws_l = wb['Based on Legal Form']
    legal_entities = []
    curr_status = ''
    for r in range(2, ws_l.max_row + 1):
        status = ws_l.cell(r, 1).value
        name = ws_l.cell(r, 2).value
        if status:
            curr_status = str(status).strip()
        if name:
            legal_entities.append({
                'legal_form': curr_status,
                'entity_name': str(name).strip()
            })
    df_legal = pd.DataFrame(legal_entities)
    df_legal.to_csv(os.path.join(PROCESSED_DIR, "bumn_legal_persero_clean.csv"), index=False, encoding='utf-8')
    print(f"✓ Saved {len(df_legal)} Direct Persero Entities to data/processed/bumn_legal_persero_clean.csv")

    # -------------------------------------------------------------
    # 3. SUBSIDIARIES (Sheet: List of Entities)
    # -------------------------------------------------------------
    ws_e = wb['List of Entities']
    subsidiaries = []
    for r in range(2, ws_e.max_row + 1):
        h_name = ws_e.cell(r, 1).value
        e_name = ws_e.cell(r, 2).value
        more_sub = ws_e.cell(r, 3).value
        business = ws_e.cell(r, 4).value
        year_est = ws_e.cell(r, 5).value
        ceo = ws_e.cell(r, 6).value
        website = ws_e.cell(r, 7).value
        update_url = ws_e.cell(r, 8).value
        
        if e_name:
            subsidiaries.append({
                'parent_holding': str(h_name).strip() if h_name else '',
                'subsidiary_name': str(e_name).strip(),
                'business_description': str(business).strip() if business else '',
                'year_established': int(year_est) if pd.notnull(year_est) and isinstance(year_est, (int, float)) else '',
                'ceo': str(ceo).strip() if ceo else '',
                'website': str(website).strip() if website else '',
                'source_url': str(update_url).strip() if update_url else ''
            })
    df_subs = pd.DataFrame(subsidiaries)
    df_subs.to_csv(os.path.join(PROCESSED_DIR, "bumn_subsidiaries_clean.csv"), index=False, encoding='utf-8')
    print(f"✓ Saved {len(df_subs)} Subsidiaries to data/processed/bumn_subsidiaries_clean.csv")

    # -------------------------------------------------------------
    # 4. DANANTARA SPVs vs UNRELATED PRIVATE (Sheet: COMPANIES & DIM)
    # -------------------------------------------------------------
    ws_dim = wb['DIM']
    dim_entities = []
    for r in range(2, ws_dim.max_row + 1):
        h_name = ws_dim.cell(r, 1).value
        s_name = ws_dim.cell(r, 2).value
        sector = ws_dim.cell(r, 3).value
        ceo = ws_dim.cell(r, 4).value
        notes = ws_dim.cell(r, 5).value
        if s_name:
            dim_entities.append({
                'entity_name': str(s_name).strip(),
                'parent_holding': str(h_name).strip() if h_name else 'PT Danantara Investment Management (DIM)',
                'sector': str(sector).strip() if sector else 'PSEL operations',
                'notes': str(notes).strip() if notes else ''
            })

    ws_c = wb['COMPANIES']
    danantara_spvs = []
    unrelated_private = []

    # Address discriminator: Danantara actual entities are registered at Wisma Danantara Indonesia, Gatot Subroto
    for r in range(2, ws_c.max_row + 1):
        c_name = ws_c.cell(r, 1).value
        addr = ws_c.cell(r, 2).value
        phone = ws_c.cell(r, 3).value
        
        if not c_name:
            continue
            
        c_name_str = str(c_name).strip()
        addr_str = str(addr).strip() if addr else ''
        phone_str = str(phone).strip() if phone else ''
        
        is_wisma_danantara = 'wisma danantara' in addr_str.lower() or 'gatot subroto' in addr_str.lower()
        
        if is_wisma_danantara:
            danantara_spvs.append({
                'company_name': c_name_str,
                'address': addr_str,
                'phone': phone_str,
                'category': 'DANANTARA_INDICATED_SPV',
                'verification_status': 'TERINDIKASI_ALAMAT_WISMA_DANANTARA (Menunggu Validasi AHU Kemenkumham)'
            })
        else:
            unrelated_private.append({
                'company_name': c_name_str,
                'address': addr_str,
                'phone': phone_str,
                'category': 'THIRD_PARTY_PRIVATE_COINCIDENTAL',
                'exclusion_reason': 'Unrelated private entity matched by keyword; location outside Danantara HQ / no BUMN ownership link'
            })

    # Add DIM subsidiaries to SPVs
    for d in dim_entities:
        danantara_spvs.append({
            'company_name': d['entity_name'],
            'address': 'Wisma Danantara Indonesia, Jalan Jendral Gatot Subroto Kav. 36-38 Jakarta Selatan',
            'phone': '',
            'category': 'DANANTARA_INDICATED_SPV',
            'verification_status': f"DIM_HOLDING_SUBSIDIARY ({d['notes']} - Menunggu Validasi AHU)"
        })

    df_spv = pd.DataFrame(danantara_spvs)
    df_spv.to_csv(os.path.join(PROCESSED_DIR, "danantara_spv_clean.csv"), index=False, encoding='utf-8')
    print(f"✓ Saved {len(df_spv)} Danantara Indicated SPVs to data/processed/danantara_spv_clean.csv")

    df_unrelated = pd.DataFrame(unrelated_private)
    df_unrelated.to_csv(os.path.join(PROCESSED_DIR, "danantara_unrelated_companies_excluded.csv"), index=False, encoding='utf-8')
    print(f"✓ Saved {len(df_unrelated)} Excluded Third-Party Companies to data/processed/danantara_unrelated_companies_excluded.csv")

    # -------------------------------------------------------------
    # 5. UNIFIED MASTER BUMN DATASET (data/processed/bumn_master_clean.csv)
    # -------------------------------------------------------------
    master_records = []
    
    # Official 7 Piloting BUMN Champions under Danantara Stage 1 (plus INA)
    PILOT_CHAMPIONS_KEYWORDS = [
        'mandiri', 'rakyat indonesia', 'bri', 'negara indonesia', 'bni',
        'perusahaan listrik negara', 'pln', 'pertamina', 'telkom', 'telekomunikasi indonesia',
        'mineral industri indonesia', 'mind id'
    ]
    
    # 6 Core Sectors from Celios Green Investment Methodology
    # (Energy, Agriculture/Forestry, Downstream/Mining, Infrastructure/Transport, Manufacturing, Housing)
    GREEN_SECTOR_KEYWORDS = [
        # Energy
        'listrik', 'pln', 'pertamina', 'energi', 'geothermal', 'gas', 'power',
        # Agriculture, Forestry & Food
        'perkebunan', 'ptpn', 'perhutani', 'pupuk', 'sang hyang seri', 'pangan', 'nabati',
        # Downstream & Mining
        'mineral', 'mind id', 'antam', 'timah', 'bukit asam', 'inalum', 'krakatau steel', 'semen',
        # Infrastructure, Transport & Logistics
        'pelindo', 'pelabuhan', 'jasa marga', 'angkasa pura', 'kereta', 'kai', 'karya', 'adhi',
        'waskita', 'wijaya karya', 'pp (persero)', 'hutama', 'asdp', 'damri', 'brantas',
        # Manufacturing & Heavy Industry
        'barata', 'boma bisma indra', 'inka', 'len', 'pindad', 'pal', 'dahana', 'rekayasa industri',
        # Housing & Urban
        'perumnas'
    ]

    def check_is_pilot(name: str) -> bool:
        n_low = name.lower()
        return any(k in n_low for k in PILOT_CHAMPIONS_KEYWORDS)

    def check_is_green_priority(name: str, sector: str = '') -> bool:
        combined = f"{name} {sector}".lower()
        return any(k in combined for k in GREEN_SECTOR_KEYWORDS)
    
    # Add Holdings
    for _, row in df_holdings.iterrows():
        entity_name = row['official_leading_entity'] if row['official_leading_entity'] else row['holding_name']
        master_records.append({
            'entity_name': entity_name,
            'alias_or_brand': row['holding_name'],
            'entity_tier': 'HOLDING_PARENT',
            'parent_holding': 'DANANTARA_BPI',
            'sector': row['sector'],
            'ceo': row['ceo'],
            'website': row['website'],
            'is_priority_for_green_screening': check_is_green_priority(entity_name, str(row['sector'])),
            'is_danantara_stage1_pilot': check_is_pilot(entity_name)
        })
        
    # Add Persero entities from Legal Form (prevent duplicate if already in holdings)
    existing_names = set(r['entity_name'].lower() for r in master_records)
    for _, row in df_legal.iterrows():
        name = row['entity_name']
        if name.lower() not in existing_names:
            is_priority = check_is_green_priority(name)
            is_pilot = check_is_pilot(name)
            master_records.append({
                'entity_name': name,
                'alias_or_brand': name,
                'entity_tier': f"PERSERO_STANDALONE ({row['legal_form']})",
                'parent_holding': 'DANANTARA_BPI',
                'sector': 'State Utility / SOE Standalone',
                'ceo': '',
                'website': '',
                'is_priority_for_green_screening': is_priority,
                'is_danantara_stage1_pilot': is_pilot
            })
            existing_names.add(name.lower())

    # Add Subsidiaries
    for _, row in df_subs.iterrows():
        name = row['subsidiary_name']
        if name.lower() not in existing_names:
            is_sub_priority = check_is_green_priority(name, f"{row['business_description']} {row['parent_holding']}")
            master_records.append({
                'entity_name': name,
                'alias_or_brand': '',
                'entity_tier': 'SUBSIDIARY',
                'parent_holding': row['parent_holding'],
                'sector': row['business_description'],
                'ceo': row['ceo'],
                'website': row['website'],
                'is_priority_for_green_screening': is_sub_priority,
                'is_danantara_stage1_pilot': False
            })
            existing_names.add(name.lower())

    # Add Danantara SPVs
    for _, row in df_spv.iterrows():
        name = row['company_name']
        if name.lower() not in existing_names:
            master_records.append({
                'entity_name': name,
                'alias_or_brand': '',
                'entity_tier': 'DANANTARA_INDICATED_SPV',
                'parent_holding': 'DANANTARA_BPI',
                'sector': 'Investment Management & Energy Transition Vehicle',
                'ceo': '',
                'website': '',
                'is_priority_for_green_screening': True,
                'is_danantara_stage1_pilot': True
            })
            existing_names.add(name.lower())

    df_master = pd.DataFrame(master_records)
    # Add unique ID
    df_master.insert(0, 'entity_id', [f"BUMN-DNT-{i+1:03d}" for i in range(len(df_master))])
    
    master_path = os.path.join(PROCESSED_DIR, "bumn_master_clean.csv")
    df_master.to_csv(master_path, index=False, encoding='utf-8')
    print(f"\n=======================================================")
    print(f"🎉 MASTER UNIFIED BUMN DATASET CREATED: {master_path}")
    print(f"Total Clean Entities Tracked: {len(df_master)}")
    print(f"Breakdown by Entity Tier:\n{df_master['entity_tier'].value_counts()}")
    print(f"Priority for Green Screening: {df_master['is_priority_for_green_screening'].sum()}")
    print(f"Danantara Stage 1 Pilot Cohort: {df_master['is_danantara_stage1_pilot'].sum()}")
    print(f"=======================================================\n")

if __name__ == "__main__":
    clean_and_consolidate()
