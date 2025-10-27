import sys
from src.extract_tables import extract_pdf_tables
from src.clean_data import clean_csv
#from src.dedupe_merge import load_all_cleaned, dedupe_keep_latest
#from src.db.loader import create_tables, upsert_dataframe
#from src.db.models import Jurado
import pandas as pd

def run_pipeline_for_pdf(pdf_path, pages, flavor):
    res = extract_pdf_tables(pdf_path, pages=pages, flavor=flavor)
    csvs = res['csvs']
    for csv in csvs:
        clean_csv(csv, source_pdf=res['pdf'], pdf_date=res['pdf_date'])

""" def run_all_and_load():
    # merge & dedupe
    full = load_all_cleaned("data/cleaned")
    ded = dedupe_keep_latest(full, key_cols=['ci'])
    # persist
    create_tables()
    upsert_dataframe(ded, Jurado) """

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("comandos: extract <pdf>, run_all")
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "extract-clean":
        run_pipeline_for_pdf(sys.argv[2], sys.argv[3], sys.argv[4])
    elif cmd == "run_all":
        print('run_all')
        #run_all_and_load()
