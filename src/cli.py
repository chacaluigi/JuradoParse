import sys
from src.extract_tables import extract_pdf_tables, extract_pdf_tables_areas, extract_special_page
from src.clean_data import clean_csv
#from src.dedupe_merge import load_all_cleaned, dedupe_keep_latest
#from src.db.loader import create_tables, upsert_dataframe
#from src.db.models import Jurado
import pandas as pd

def run_pipeline_for_pdf(type, pdf_path, pages, flavor, top_cut):

    if(type == 'normal'):
        res = extract_pdf_tables(pdf_path, pages=pages, flavor=flavor)
    elif(type == 'areas'):
        res = extract_pdf_tables_areas(pdf_path, pages=pages, flavor=flavor)
    elif(type == 'special'):
        res = extract_special_page(pdf_path, pages=pages, flavor=flavor, top_cut = top_cut)
    else:
        print('colocar tipo')

    csvs = res['csvs']

    for csv in csvs:
        clean_csv(csv, source_pdf = res['pdf'], pdf_date = res['pdf_date'])


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("comandos: <type: normal|areas|special> <source: pdf> <pages> <flavor: stream|lattice> <top_cut>")
        sys.exit(1)
    type = sys.argv[1]
    pdf = sys.argv[2]
    pages = sys.argv[3] if len(sys.argv) > 3 else 'all' # 10-15 | 10,60, 70-end
    flavor = sys.argv[4] if len(sys.argv) > 4 else 'stream'
    top_cut = sys.argv[5] if len(sys.argv) > 5 and type == 'special' else "0.178" #El 17.8% de la página. Para doc especiales.
    
    run_pipeline_for_pdf(type, pdf, pages, flavor, top_cut)



