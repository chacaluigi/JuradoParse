import sys
import pandas as pd
from src.extract_tables import extract_pdf_tables, extract_pdf_tables_areas
from src.clean_data import clean_csv
from src.utils import file_exists, is_pdf_file

from data.dictionary.data_bolivia import PDFConfig

def run_pipeline_for_pdf(pdf_key, pages):

    config = PDFConfig.get_config(pdf_key)
    pdf_path = config['pdf_path']
    type = config['type']

    if not file_exists(pdf_path):
        print(f"Error: El archivo '{pdf_path}' no existe")
        return
    
    if not is_pdf_file(pdf_path):
        print(f"Error: El archivo '{pdf_path}' no es un archivo PDF válido")
        return

    if(type == 'normal'):
        res = extract_pdf_tables(
            pdf_path=pdf_path,
            flavor = config['flavor'],
            pages = pages,
            column_names = config['column_names']
        )
    elif(type == 'areas'):
        res = extract_pdf_tables_areas(
            pdf_path=config['pdf_path'],
            flavor=config['flavor'],
            pages=pages,
            all_top_cut=config['all_top_cut'],
            column_separators=config['column_separators'],
            column_names=config['column_names']
        )
    else:
        print('especificar tipo de extracción')

    print(res['pdf_date'])

    csvs = res['csvs']

    for csv in csvs:
        clean_csv(csv, source_pdf = res['pdf'], pdf_date = res['pdf_date'])
   

if __name__ == "__main__":
    
    if len(sys.argv) < 3:
        print("comandos: <pdf_key> <pages>")
        sys.exit(1)

    pdf_key = sys.argv[1]
    pages = sys.argv[2]

    run_pipeline_for_pdf(pdf_key, pages)



