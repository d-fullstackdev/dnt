import os
import sys
import time
import opendataloader_pdf

def main():
    base_dir = r"C:\Users\yooma\OneDrive\Desktop\duniahub\client\28. Celios9-danantara"
    pdf_path = os.path.join(base_dir, "ref", "BUKU METODOLOGI PENELITIAN, KUANTITATIF, KUALITATIF DAN MIXED METHODS.pdf")
    out_dir = os.path.join(base_dir, "ref")
    
    if not os.path.exists(pdf_path):
        print(f"Error: File not found: {pdf_path}")
        sys.exit(1)
        
    print(f"Parsing 370-page book using OpenDataLoader...")
    print(f"Input: {pdf_path}")
    print(f"Output dir: {out_dir}")
    t0 = time.time()
    
    try:
        opendataloader_pdf.convert(
            input_path=pdf_path,
            output_dir=out_dir,
            format="markdown,json,html",
            image_output="external",
            image_format="png",
            threads="4"
        )
        elapsed = time.time() - t0
        print(f"Parsing completed successfully in {elapsed:.1f}s!")
    except Exception as e:
        elapsed = time.time() - t0
        print(f"Error during parsing ({elapsed:.1f}s): {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
