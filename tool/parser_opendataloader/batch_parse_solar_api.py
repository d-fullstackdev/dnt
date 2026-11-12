import os
import sys
import time
import opendataloader_pdf

def main():
    target_dir = r"c:\Users\yooma\OneDrive\Desktop\duniahub\client\23. Celios8-solarpanel\data\processed\references\paper solar api"
    
    pdf_files = sorted([f for f in os.listdir(target_dir) if f.lower().endswith('.pdf')])
    print(f"Found {len(pdf_files)} PDF files to parse in: {target_dir}")
    print("=" * 80)
    
    success_count = 0
    fail_count = 0
    
    for idx, pdf in enumerate(pdf_files, 1):
        pdf_path = os.path.join(target_dir, pdf)
        base_name = os.path.splitext(pdf)[0]
        md_file = os.path.join(target_dir, f"{base_name}.md")
        json_file = os.path.join(target_dir, f"{base_name}.json")
        html_file = os.path.join(target_dir, f"{base_name}.html")
        img_dir = os.path.join(target_dir, f"{base_name}_images")
        
        # Check if already parsed
        if os.path.exists(md_file) and os.path.exists(json_file) and os.path.exists(html_file) and os.path.exists(img_dir):
            print(f"[{idx}/{len(pdf_files)}] ALREADY PARSED: {pdf}")
            success_count += 1
            continue
            
        print(f"[{idx}/{len(pdf_files)}] PARSING: {pdf} ...")
        t0 = time.time()
        try:
            opendataloader_pdf.convert(
                input_path=pdf_path,
                output_dir=target_dir,
                format="markdown,json,html",
                image_output="external",
                image_format="png"
            )
            elapsed = time.time() - t0
            print(f"  -> SUCCESS ({elapsed:.1f}s): {base_name}")
            success_count += 1
        except Exception as e:
            elapsed = time.time() - t0
            print(f"  -> ERROR ({elapsed:.1f}s) for {pdf}: {e}")
            fail_count += 1
            
    print("=" * 80)
    print(f"COMPLETED BATCH: {success_count} succeeded, {fail_count} failed out of {len(pdf_files)} PDFs.")

if __name__ == "__main__":
    main()
