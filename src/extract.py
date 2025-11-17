import os
from pathlib import Path
import camelot
from src.utils import ensure_dir, parse_date_from_filename, extract_dimensions_page, join_tables_csv, repair_broken_rows, repair_mixed_columns

#normal
def extract_pdf_tables(pdf_path: str, output_dir: str = None, flavor = "stream", pages = "all", column_names = None):
    
    pdf_path = Path(pdf_path)
    ensure_dir(output_dir)
    output_csv = output_dir / f"{pages}__{pdf_path.stem}.csv"
    if os.path.exists(output_csv):
        os.remove(output_csv)

    print(f"====Extrayendo tablas de: {pdf_path} / flavor = {flavor} / pages = {pages}")

    tables = camelot.read_pdf(
        str(pdf_path), 
        pages=pages, 
        flavor=flavor, 
        split_text=True, 
        flag_size=True,
    )
    print(f"Tablas encontradas: {len(tables)}")

    #unir tablas csv
    csv_path = join_tables_csv(tables, output_csv, column_names) 

    #obtener la fecha del nombre del documento
    pdf_date = parse_date_from_filename(str(pdf_path))

    return {"pdf": str(pdf_path), "pdf_date": pdf_date, "csv": csv_path}

#areas
def extract_pdf_tables_areas(type: str, pdf_path, output_dir: str = None, flavor = 'stream', pages = 'all', coord_multiplier = None, column_separators = None, column_names = None):
    
    pdf_path = Path(pdf_path)
    ensure_dir(output_dir)
    output_csv = output_dir / f"{pages}__{pdf_path.stem}.csv"
    
    print(f"===Extrayendo tablas de: {pdf_path} / flavor = {flavor} / pages = {pages}")

    # Para extraer las areas de la página
    page_width, page_height = extract_dimensions_page(pdf_path, 5)
    table_areas_list = []
    coord_multiplier = [float(item) for item in coord_multiplier] if coord_multiplier else [0, 0, 1, 1]
    if(coord_multiplier):
        mx1, my1, mx2, my2 = coord_multiplier
        x1, y1, x2, y2 = mx1*float(page_width), my1*float(page_height), mx2*float(page_width), my2*float(page_height)
        page_width = x2-x1
        page_height = y2-y1
        table_areas_list = [
            [x1, y1, x2, y2]
        ]
        if type == 'areas':
            table_areas_list = [
                [x1, y1, 1/3*float(page_width)+x1, y2],
                [1/3*float(page_width) + x1, y1, 2/3*float(page_width) + x1, y2],
                [2/3*float(page_width) + x1, y1, page_width + x1, y2],
            ]
        #parseamos a strings
        table_areas_list = [
            ",".join(str(coord) for coord in sublist)
            for sublist in table_areas_list
        ]
    tables=[]
    
    table_list = camelot.read_pdf(
        str(pdf_path), 
        pages=pages, 
        flavor=flavor, 
        split_text=False, #FALSE: evita divisiones de columnas inexactas
        flag_size=True, 
        table_areas=table_areas_list,
        columns=column_separators
    )
    repaired_broken_rows = repair_broken_rows(table_list)
    repaired_columns_mixed = repair_mixed_columns(repaired_broken_rows) if type == 'areas' else repaired_broken_rows
    tables = repaired_columns_mixed
    
    print(f"Tablas encontradas: {len(tables)}")

    #unir tablas csv
    csv_path = join_tables_csv(tables, output_csv, column_names) 

    #obtener la fecha del nombre del documento
    pdf_date = parse_date_from_filename(str(pdf_path))

    return {"pdf": str(pdf_path), "pdf_date": pdf_date, "csv": csv_path}
