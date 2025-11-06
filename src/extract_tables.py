import re
import pandas as pd
import sys
from pathlib import Path
import camelot
import math
from src.utils import parse_date_from_filename, extract_dimensions_page, join_tables_csv, repair_broken_rows, repair_mixed_columns

DATA_DIR = Path(__file__).resolve().parents[1] / "data"


#normal
def extract_pdf_tables(pdf_path: str, output_dir: str = None, flavor = "stream", pages = "all", column_names = None):
    
    pdf_path = Path(pdf_path)
    output_dir = Path(output_dir or DATA_DIR / "extracted")
    
    print(f"Extrayendo tablas de: {pdf_path} / flavor = {flavor} / pages = {pages}")

    tables = camelot.read_pdf(
        str(pdf_path), 
        pages=pages, 
        flavor=flavor, 
        split_text=True, 
        flag_size=True,
    )
    print(f"Tablas encontradas: {len(tables)}")

    #unir tablas csv
    csv_paths = join_tables_csv(tables, pdf_path, output_dir, pages, column_names) 

    #obtener la fecha del nombre del documento
    pdf_date = parse_date_from_filename(str(pdf_path))

    return {"pdf": str(pdf_path), "pdf_date": pdf_date, "csvs": csv_paths}

#areas
def extract_pdf_tables_areas(pdf_path, output_dir: str = None, flavor = 'stream', pages = 'all', all_top_cut = None, column_separators = None, column_names = None):
    
    pdf_path = Path(pdf_path)
    output_dir = Path(output_dir or DATA_DIR / "extracted")
    
    print(f"Extrayendo tablas de: {pdf_path} / flavor = {flavor} / pages = {pages}")

    # Para extraer las areas de la página
    page_width, page_height = extract_dimensions_page(pdf_path, 5)
    table_areas_list = []
    all_top_cut = float(all_top_cut) if all_top_cut else None

    if(all_top_cut):
        table_areas_list = [
            [f'0,0,{1/3*float(page_width)},{all_top_cut*float(page_height)}'],
            [f'{1/3*float(page_width)},0,{2/3*float(page_width)},{all_top_cut*float(page_height)}'],
            [f'{2/3*float(page_width)},0,{page_width},{all_top_cut*float(page_height)}']
        ]
    else:
        table_areas_list = [
            [f'0,0,{1/3*float(page_width)},{page_height}'],
            [f'{1/3*float(page_width)},0,{2/3*float(page_width)},{page_height}'],
            [f'{2/3*float(page_width)},0,{page_width},{page_height}']
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
            columns=column_separators[i]
        )
        repaired_broken_rows = repair_broken_rows(table_list)
        repaired_columns_mixed = repair_mixed_columns(repaired_broken_rows)
        tables.extend(repaired_columns_mixed)
    
    print(f"Tablas encontradas: {len(tables)}")

    #ordenar tablas de acuerdo al pdf extraído
    cols = 3
    reason = math.ceil(len(tables)/cols)
    tables_ordered = [tables[j] for i in range(reason) for j in range(i, len(tables), reason)]
    tables = tables_ordered

    #unir tablas csv
    csv_paths = join_tables_csv(tables, pdf_path, output_dir, pages, column_names) 

    #obtener la fecha del nombre del documento
    pdf_date = parse_date_from_filename(str(pdf_path))

    return {"pdf": str(pdf_path), "pdf_date": pdf_date, "csvs": csv_paths}
