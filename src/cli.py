from pathlib import Path
import sys
import pandas as pd
from data.dictionary.data_bolivia import PDFConfig
from src.extract_clean import extract_clean
from src.utils import file_exists, generate_groped_ranges, is_pdf_file

def run_pipeline_for_pdf(pdf_key, pages):
    config = PDFConfig.get_config(pdf_key)
    pdf_path = config['pdf_path']
    type = config['type']
    first_top_cut = config['first_top_cut']

    #comprobamos si el pdf existe y si es un archivo pdf
    if not file_exists(pdf_path):
        print(f"Error: El archivo '{pdf_path}' no existe")
        return
    if not is_pdf_file(pdf_path):
        print(f"Error: El archivo '{pdf_path}' no es un archivo PDF válido")
        return

    if pages == "all":
        pages = config['all_pages']

    reason = 10 if type == 'normal' else 3
    page_groups = generate_groped_ranges(pages, first_top_cut, reason) if '-' in pages else None
    print(page_groups)
    if page_groups:
        for group in page_groups:
            extract_clean(pdf_key, group)
    else:
        extract_clean(pdf_key, pages)

if __name__ == "__main__":
    
    if len(sys.argv) < 3:
        print("comandos: <pdf_key> <pages>")
        sys.exit(1)

    pdf_key = sys.argv[1]
    pages = sys.argv[2]

    run_pipeline_for_pdf(pdf_key, pages)




