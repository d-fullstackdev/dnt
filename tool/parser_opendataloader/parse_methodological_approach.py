import os
import opendataloader_pdf

def parse_methodological_approach():
    base_dir = r"C:\Users\yooma\OneDrive\Desktop\duniahub\client\28. Celios9-danantara"
    pdf_path = os.path.join(base_dir, "ref", "20260831_Methodological Approach.pdf")
    out_dir = os.path.join(base_dir, "ref")
    
    print(f"Parsing {pdf_path} to {out_dir} using OpenDataLoader...")
    opendataloader_pdf.convert(
        input_path=pdf_path,
        output_dir=out_dir,
        format="markdown,json,html",
        image_output="external",
        image_format="png"
    )
    print("Parsing completed successfully!")

if __name__ == "__main__":
    parse_methodological_approach()
