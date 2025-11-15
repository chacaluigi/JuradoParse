import os
from pathlib import Path
from datetime import datetime
import re
import pandas as pd
import pdfplumber

from data.dictionary.data_bolivia import BoliviaData

def ensure_dir(p):
    Path(p).mkdir(parents=True, exist_ok=True)

# Funciones de Ordenado de Columnas

def extract_dimensions_page(pdf_file, page_number):
    with pdfplumber.open(pdf_file) as pdf:
        page = pdf.pages[page_number+1]
    return page.width, page.height

def repair_broken_rows(table_list):
    for table in table_list:
        df = table.df.fillna('')  # reemplaza NaN con strings vacíos
        repaired_rows = []
        
        for _, row in df.iterrows():
            # se convierte a strings y se limpia
            row = [str(cell).strip() for cell in row]
            
            #si la primera columna vacía y hay filas anteriores
            if row[0] == '' and repaired_rows:
                # se une con ultima fila
                last_row = repaired_rows[-1]
                for i in range(len(row)):
                    if row[i] != '':
                        last_row[i] = (last_row[i] + ' ' + row[i]).strip()
            else:
                repaired_rows.append(row)

        table.df = pd.DataFrame(repaired_rows)
    
    return table_list

def repair_mixed_columns(table_list):
    for table in table_list:
        df = table.df.fillna('')  # reemplaza NaN con strings vacíos
        
        for idx in range(1, len(df)):
            #se usa .iloc para acceso seguro por índice
            nombre = str(df.iloc[idx, 0]) if pd.notna(df.iloc[idx, 0]) else ''
            documento = str(df.iloc[idx, 1]) if pd.notna(df.iloc[idx, 1]) else ''
            municipio = str(df.iloc[idx, 2]) if pd.notna(df.iloc[idx, 2]) else ''
            recinto = str(df.iloc[idx, 3]) if pd.notna(df.iloc[idx, 3]) else ''
            mesa = str(df.iloc[idx, 4]) if pd.notna(df.iloc[idx, 4]) else ''
            
            pattern_nombre_doc = r'^(.+?)([A-Z]-?\d+)$'
            pattern_mesa = r'\d{1,2}$'
            pattern_exchanged = r'^\d+$'
            pattern_remove_number = r'\d'
            
            changes_made = False
            
            if documento == '' and nombre != '':
                match = re.search(pattern_nombre_doc, nombre)
                if match:
                    nombre = match.group(1).strip()
                    documento = match.group(2).strip()
                    changes_made = True
                else:
                    print(f'repair_mixed_columns: No se pudo separar el nombre del documento. DOC={documento} | NOMBRE={nombre}')

            if recinto == '' and mesa != '':
                #print(f'Fila {idx}: Recinto vacío, Mesa tiene contenido')
                recinto = mesa
                mesa = ''
                changes_made = True
            
            if mesa == '' and recinto != '':
                #print(f'Fila {idx}: Recinto tiene contenido, Mesa vacío')
                match = re.search(pattern_mesa, recinto)
                if match:
                    mesa = match.group(0)
                    recinto = re.sub(pattern_mesa, '', recinto).strip()
                    changes_made = True
                elif (re.sub(pattern_remove_number, '', municipio)):
                    municipio = re.sub(pattern_remove_number, '', municipio).strip()
                    changes_made = True
                    print(f'repair_mixed_columns: No se pudo separar el recinto de mesa, pero, se eliminaron numeros de MUNICIPIO. DOC = {documento}')
                else:
                    print(f'repair_mixed_columns: No se pudo separar el recinto de mesa. DOC = {documento}')
            
            match_number = re.search(pattern_exchanged, recinto)

            if match_number:
                #print(f'Fila {idx}: Recinto es solo número, moviendo a Mesa')
                recinto = mesa
                mesa = match_number.group(0)
                changes_made = True
            
            if changes_made:
                df.iloc[idx, 0] = nombre
                df.iloc[idx, 1] = documento
                df.iloc[idx, 2] = municipio
                df.iloc[idx, 3] = recinto
                df.iloc[idx, 4] = mesa
        
        table.df = df
    
    return table_list

def is_header_row(first_row):
    return any('APELLIDOS' in str(cell).upper() for cell in first_row)

def join_tables_csv(tables, output_csv, column_names):
    csv_paths = []

    if len(tables) > 0:
        all_dataframes = []

        for _, table in enumerate(tables, start=1):
            first_row = table.df.iloc[0]
            if is_header_row(first_row):
                all_dataframes.append(table.df.iloc[1:])
            else:
                all_dataframes.append(table.df)
            
        combined_df = pd.concat(all_dataframes, ignore_index=True)
        del all_dataframes

        try:
            combined_df.columns = column_names
        except ValueError as e:
            expected_length = len(column_names)
            current_length = combined_df.shape[1]
            print(f"---ERROR: Se esperaban {expected_length} nombres de columna, pero el DataFrame tiene {current_length} columnas.")
            return None
        
        combined_df.to_csv(output_csv, index=False, header=True)
        csv_paths.append(str(output_csv))
        print(f"Archivo extraido guardado en: {output_csv}  Dimensiones: {combined_df.shape[0]} filas x {combined_df.shape[1]} columnas")
    return csv_paths


# Funciones de Limpieza de datos

def normalize_document(doc_text):
    complement = ''
    doc_text = doc_text.strip()
    if pd.isna(doc_text) or doc_text == '':
        print(f'Error: DOCUMENTO está vacío. DOC = {doc_text}')
        return pd.Series(['','',''])
    

    separators = r"\s+|-"
    divisions = re.split(separators, str(doc_text).strip())
    parts = [item for item in divisions if item]

    if parts[0].upper() == 'I':
        doc_type='C.I.'
    elif parts[0].upper() == 'P':
        doc_type='PAS.'
    else:
        doc_type=parts[0]
    
    doc_number = parts[1] if len(parts) > 1 else None
    complement = parts[2] if len(parts) > 2 else None
    if len(parts) < 2:
        #captura del problema
        print(f'Error: DOCUMENTO no se pudo dividir en partes, debido a que no tiene suficientes elementos. DOC = {doc_text}')
        print('parts: ',parts)
        doc_number = None
        complement = None
    
    return pd.Series([doc_type, doc_number, complement]) 

def combine_special_parts(parts: list, conectors: list):
    processed_parts = []
    i = 0
    num_parts = len(parts)

    while i<num_parts:
        current_part = parts[i]
        mercado_pinell_exist = (
            current_part.lower() == 'mercado' and 
            i + 1 < num_parts and 
            parts[i + 1].lower() == 'pinell'
        )

        if current_part.lower() in conectors and parts[i+1].lower() in conectors and i+2 < num_parts:
            combined = f"{current_part} {parts[i+1]} {parts[i+2]}"
            processed_parts.append(combined)
            i+=3
        elif current_part.lower() in conectors and i+1 < num_parts or mercado_pinell_exist:
            combined = f"{current_part} {parts[i+1]}"
            processed_parts.append(combined)
            i+=2
        else:
            processed_parts.append(current_part)
            i+=1
    
    return processed_parts

def separate_lastname(text):
    if pd.isna(text):
        return pd.Series(['',''])
    
    parts = str(text).strip().split()

    conectors={'de', 'del', 'la', 'tezanos', 'le', 'san'}
    
    processed_parts = combine_special_parts(parts, conectors)

    num_processed_parts = len(processed_parts)

    if num_processed_parts == 1:
        pat_surname = ''
        mat_surname = processed_parts[0]
    elif num_processed_parts == 2:
        pat_surname = processed_parts[0]
        mat_surname = processed_parts[1]
    else:
        pat_surname = processed_parts[0]
        mat_surname = ' '.join(processed_parts[1:])

    return pd.Series([pat_surname, mat_surname])

def separate_last_and_names(text):
    
    nombres_bolivia = BoliviaData.NOMBRES

    if pd.isna(text):
        return pd.Series(['','',''])
    
    parts = str(text).strip().split()

    if len(parts) < 2:
        print(f'---ERROR: EXTRACCIÓN NOMBRE INCORRECTO. El nombre {text} no puede ser menor a 2 palabras.')
        return pd.Series([text, '', ''])
    
    conectors={'de', 'del', 'la', 'tezanos', 'le', 'san'}
    
    processed_parts = combine_special_parts(parts, conectors)

    if len(processed_parts) == 2:
        pat_surname = ''
        mat_surname = processed_parts[0]
        names = processed_parts[1]

    elif len(processed_parts) == 3:
        if processed_parts[1] in nombres_bolivia:
            pat_surname = ""
            mat_surname = processed_parts[0]
            names = f'{processed_parts[1]} {processed_parts[2]}'
        else:
            pat_surname = processed_parts[0]
            mat_surname = processed_parts[1]
            names = processed_parts[2]
    else:
        pat_surname = processed_parts[0]
        mat_surname = processed_parts[1]
        names = ' '.join(processed_parts[2:])
    
    return pd.Series([pat_surname, mat_surname, names])

def remove_number_column(df, nombre_columna):
    df[nombre_columna] = df[nombre_columna].astype(str).str.replace(r'[\d\.]', '', regex=True).str.strip()
    return df


    """ def clean_header_column(text):
    pattern = r'^(RECINTO|MUNICIPIO)'
    match = re.match(pattern, text, re.IGNORECASE)
    
    if match:
        return match.group(0).upper()
    
    return text  """

# Otros

def parse_date_from_filename(filename: str):
    #intenta extraer fecha YYYYMMDD o YYYY-MM-DD del nombre de archivo.
    m = re.search(r'(\d{4})[-_]?(\d{2})[-_]?(\d{2})', filename)
    if m:
        return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3))).date()
    return None

def validate_pdf(pdf_path):
    return os.path.isfile(pdf_path) and pdf_path.lower().endswith('.pdf')

def validate_pages(pages):
    if pages.lower() == 'all':
        return True
    #solo un número o dos números separados por '-'
    num_pattern = r"^\d+$|^\d+-\d+$"
    if not re.match(num_pattern, pages):
        return False
    
    #validación de un rango
    if '-' in pages:
        try:
            start_page_str, end_page_str = pages.split('-')
            start_page = int(start_page_str)
            end_page = int(end_page_str)
            if start_page < 1 or end_page < 1 or start_page > end_page:
                return False
        except ValueError:
            return False
            
    #validación de un número
    else:
        try:
            page_num = int(pages)
            if page_num < 1:
                return False
        except ValueError:
            return False

    return True

def generate_groped_ranges(text: str, first_page: str, first_special_page: str, reason: int):
    start_str, end_str = text.split('-')
    start = int(start_str)
    end = int(end_str)
    
    ranges = []
    if first_special_page and int(first_page) == start:
        ranges.append(str(start))
        start += 1
        
    current_start = start
    while current_start <= end:
        range_end = current_start + reason - 1
        
        # formateamos en caso que esté en el límite
        if range_end > end:
            range_end = end
        
        range_str = f"{current_start}-{range_end}"
        ranges.append(range_str)
        current_start = range_end + 1
        
    return ranges