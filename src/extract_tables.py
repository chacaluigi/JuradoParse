import re
import pandas as pd
import sys
from pathlib import Path
import camelot
import math
from src.utils import parse_date_from_filename, extract_dimensions_page, join_tables_csv, repair_broken_rows_simple

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

def extract_special_pages(pdf_path: str, output_dir: str = None, pages="4", flavor="stream", top_cut = 0.178):
    
    pdf_path = Path(pdf_path)
    output_dir = Path(output_dir or DATA_DIR / "extracted")
    
    print(f"Extrayendo tablas de: {pdf_path} / flavor = {flavor} / pages = {pages}")

    page_width, page_height = extract_dimensions_page(pdf_path, 5)

    special_table_areas_list = [
        [f'0,0,{1/3*float(page_width)},{top_cut*float(page_height)}'],
        [f'{1/3*float(page_width)},0,{2/3*float(page_width)},{top_cut*float(page_height)}'],
        [f'{2/3*float(page_width)},0,{page_width},{top_cut*float(page_height)}']
    ]

    columns = [
        ['78.10,113.30,154.7,244.17'],
        ['338.5,366.7,415.67,492.93'],
        ['587.14,615.14,663.92,740.95']
    ]

    tables=[]

    for i, table_areas in enumerate(special_table_areas_list):
        table_list = camelot.read_pdf(
            str(pdf_path), 
            pages=pages, 
            flavor=flavor, 
            split_text=False, #FALSE: evita divisiones de columnas inexactas
            flag_size=True, 
            table_areas=table_areas,
            columns=columns[i]
        )
        repaired_tables = repair_broken_rows_simple(table_list)
        tables.extend(repaired_tables)

    print(f"Cantidad de tablas encontradas: {len(tables)}")
 
    #ordenar tablas de acuerdo al pdf
    """ cols = 3
    reason = math.ceil(len(tables)/cols)
    tables_ordered = [tables[j] for i in range(reason) for j in range(i, len(tables), reason)]
    tables = tables_ordered """

    #unir csvs extraídos
    csv_paths = join_tables_csv(tables, pdf_path, output_dir, pages) 

    pdf_date = parse_date_from_filename(str(pdf_path))

    return {"pdf": str(pdf_path), "pdf_date": pdf_date, "csvs": csv_paths}

def extract_pdf_tables_areas(pdf_path: str, output_dir: str = None, pages="all", flavor="stream"):
    
    pdf_path = Path(pdf_path)
    output_dir = Path(output_dir or DATA_DIR / "extracted")
    
    print(f"Extrayendo tablas de: {pdf_path} / flavor = {flavor} / pages = {pages}")

    page_width, page_height = extract_dimensions_page(pdf_path, 5)

    table_areas_list = [
        [f'0,0,{1/3*float(page_width)},{page_height}'],
        [f'{1/3*float(page_width)},0,{2/3*float(page_width)},{page_height}'],
        [f'{2/3*float(page_width)},0,{page_width},{page_height}']
    ]

    columns = [
        ['78.10,113.30,154.7,244.17'],
        ['338.5,366.7,415.67,492.93'],
        ['587.14,615.14,663.92,740.95']
    ]

    tables=[]
    
    for i, table_areas in enumerate(table_areas_list):
        table_list = camelot.read_pdf(
            str(pdf_path), 
            pages=pages, 
            flavor=flavor, 
            split_text=False, #FALSE: evita divisiones de columnas inexactas
            flag_size=True, 
            table_areas=table_areas,
            columns=columns[i]
        )
        repaired_tables = repair_broken_rows_simple(table_list)
        tables.extend(repaired_tables)

    print(f"Cantidad de tablas encontradas: {len(tables)}")
 
    #ordenar tablas de acuerdo al pdf extraído
    cols = 3
    reason = math.ceil(len(tables)/cols)
    tables_ordered = [tables[j] for i in range(reason) for j in range(i, len(tables), reason)]
    tables = tables_ordered

    #unir tablas csv
    csv_paths = join_tables_csv(tables, pdf_path, output_dir, pages) 

    pdf_date = parse_date_from_filename(str(pdf_path))

    return {"pdf": str(pdf_path), "pdf_date": pdf_date, "csvs": csv_paths}


def extract_pdf_tables(pdf_path: str, output_dir: str = None, pages="all", flavor="stream"):
    
    pdf_path = Path(pdf_path)
    output_dir = Path(output_dir or DATA_DIR / "extracted")
    
    print(f"Extrayendo tablas de: {pdf_path} --- flavor = {flavor} --- pages = {pages}")

    tables = camelot.read_pdf(str(pdf_path), pages=pages, flavor=flavor, split_text=True, flag_size=True)
    print(f"Tablas encontradas: {len(tables)}")

    csv_paths = join_tables_csv(tables, pdf_path, output_dir, pages) 

    pdf_date = parse_date_from_filename(str(pdf_path))
    return {"pdf": str(pdf_path), "pdf_date": pdf_date, "csvs": csv_paths}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python extract_tables.py <pdf_path> [pages] [flavor]")
        sys.exit(1)
    pdf = sys.argv[1]
    pages = sys.argv[2] if len(sys.argv) > 2 else "all"
    flavor = sys.argv[3] if len(sys.argv) > 3 else "stream"
    #top_cut = sys.argv[4]
    #res = extract_pdf_tables(pdf, pages=pages, flavor=flavor)
    #res = extract_pdf_tables_areas(pdf, pages=pages, flavor=flavor)
    res = extract_special_pages(pdf, pages=pages, flavor=flavor)
