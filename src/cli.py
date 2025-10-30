import sys
import pandas as pd
from src.extract_tables import extract_pdf_tables, extract_pdf_tables_areas, extract_special_page
from src.clean_data import clean_csv
from src.utils import file_exists, is_pdf_file

from data.dictionary.data_bolivia import PDFConfig

def run_pipeline_for_pdf(pdf_key, pages):

    type, pdf_path, flavor, first_page, first_top_cut, all_pages, all_top_cut, column_separators, column_names = PDFConfig.get_attributes(pdf_key, 'type', 'pdf_path', 'flavor', 'first_page', 'first_top_cut', 'all_pages', 'all_top_cut', 'column_separators', 'column_names')

    if(type == 'normal'):
        res = extract_pdf_tables(pdf_path, flavor = flavor, pages = pages)
    elif(type == 'areas'):
        res = extract_pdf_tables_areas(pdf_path, flavor = flavor, pages = pages, all_top_cut = all_top_cut, column_separators = column_separators, column_names = column_names)
            
            
    elif(type == 'special'):
        res = extract_special_page(pdf_path, pages=pages, flavor=flavor, top_cut = all_top_cut)
    else:
        print('colocar tipo')

    print(res['pdf_date'])

    """ csvs = res['csvs']

    for csv in csvs:
        clean_csv(csv, source_pdf = res['pdf'], pdf_date = res['pdf_date']) """


if __name__ == "__main__":
    
    if len(sys.argv) < 2:
        print("comandos: <type: normal|areas|special> <source: pdf> <pages> <flavor: stream|lattice> <top_cut>")
        sys.exit(1)

    pdf_key = sys.argv[1]
    pages = sys.argv[2]

    """ pdf = sys.argv[2]
    pages = sys.argv[3] if len(sys.argv) > 3 else 'all' # 10-15 | 10,60, 70-end
    flavor = sys.argv[4] if len(sys.argv) > 4 else 'stream'
    top_cut = sys.argv[5] if len(sys.argv) > 5 and type == 'special' else "0.178" #El 17.8% de la página. Para doc especiales. """
    
    """ if not file_exists(pdf):
        print(f"Error: El archivo '{pdf}' no existe")
        sys.exit(1)
    
    if not is_pdf_file(pdf):
        print(f"Error: El archivo '{pdf}' no es un archivo PDF válido")
        sys.exit(1) """

    run_pipeline_for_pdf(pdf_key, pages)



