import os
from pathlib import Path
from datetime import datetime
import re
from PyPDF2 import PdfReader
import pandas as pd
import pdfplumber

from data.dictionary.data_bolivia import BoliviaData

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
                    print(f'src.utils-repair_mixed_columns: No se pudo separar el nombre del documento. documento = {documento}')

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
                    print(f'src.utils-repair_mixed_columns: No se pudo separar el recinto de mesa, pero, se eliminaron numeros de municipio. documento = {documento}')
                else:
                    print(f'src.utils-repair_mixed_columns: No se pudo separar el recinto de mesa. documento = {documento}')
            
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

def join_tables_csv(tables, pdf_path, output_dir, pages):
    csv_paths = []

    if len(tables) > 0:
        all_dataframes = []

        for i, table in enumerate(tables, start=1):
            if i == 1:
                all_dataframes.append(table.df)
            else:
                all_dataframes.append(table.df.iloc[1:])
        
        combined_df = pd.concat(all_dataframes, ignore_index=True)
        combined_csv = output_dir / f"{pages}__{pdf_path.stem}.csv"
        combined_df.to_csv(combined_csv, index=False, header=False)
        csv_paths.append(str(combined_csv))
        print(f"Archivo extraido guardado en: {combined_csv}  Dimensiones: {combined_df.shape[0]} filas x {combined_df.shape[1]} columnas")
    return csv_paths


# Funciones de Limpieza de datos

def normalize_document(doc_text):
    complement=''
    if pd.isna(doc_text):
        return pd.Series(['','',''])
    
    parts = str(doc_text).strip().split('-', 1)

    if parts[0].upper() == 'I':
        doc_type='C.I.'
    elif parts[0].upper() == 'P':
        doc_type='PAS.'
    else:
        doc_type=parts[0]

    if len(parts) > 1:
        doc_number = parts[1]
    else:
        #captura del problema
        print(f'Error: "src.utils-normalize_document(doc_text)" parts no tiene suficientes elementos. parts = {parts} | doc_text = {doc_text}')
        doc_number = None
    
    return pd.Series([doc_type, doc_number, complement]) 

""" def remove_number_column(df, nombre_columna):
    df[nombre_columna] = df[nombre_columna].astype(str).str.replace(r'[\d\.]', '', regex=True).str.strip()
    return df """

def separate_last_and_first_names(text):
    nombres_bolivia = BoliviaData.NOMBRES

    if pd.isna(text):
        return pd.Series(['','',''])
    
    parts=str(text).strip().split()

    if len(parts) < 2:
        print(f'ERROR: EXTRACCIÓN NOMBRE INCORRECTO. El nombre {text} no puede ser menos de 2 palabras.')
        return pd.Series([text, '', ''])
    
    conectors={'de', 'del', 'la', 'tezanos', 'le', 'san', 'mercado pinell'}

    processed_parts = []
    i=0
    while i<len(parts):
        current_part=parts[i]
        mercado_pinell_exist = True if current_part.lower() == 'mercado' and parts[i+1].lower() == 'pinell' else False

        if current_part.lower() in conectors and parts[i+1].lower() in conectors and i+2 < len(parts):
            combined = f"{current_part} {parts[i+1]} {parts[i+2]}"
            processed_parts.append(combined)
            i+=3
        elif current_part.lower() in conectors and i+1<len(parts) or mercado_pinell_exist:
            combined = f"{current_part} {parts[i+1]}"
            processed_parts.append(combined)
            i+=2
        else:
            processed_parts.append(current_part)
            i+=1
    
    parts=processed_parts

    if len(parts) == 2:
        pat_surname=''
        mat_surname=parts[0]
        names=parts[1]

    elif len(parts) == 3:
        if parts[1] in nombres_bolivia:
            pat_surname=""
            mat_surname=parts[0]
            names=f'{parts[1]} {parts[2]}'
        else:
            pat_surname=parts[0]
            mat_surname=parts[1]
            names=parts[2]
    else:
        pat_surname=parts[0]
        mat_surname=parts[1]
        names = ' '.join(parts[2:])
    
    return pd.Series([pat_surname, mat_surname, names])

def clean_header_column(text):
    pattern = r'^(RECINTO|MUNICIPIO)'
    match = re.match(pattern, text, re.IGNORECASE)
    
    if match:
        return match.group(0).upper()
    
    return text 

# Otros

def file_exists(pdf_path):
    return os.path.isfile(pdf_path)

def is_pdf_file(pdf_path):
    return pdf_path.lower().endswith('.pdf')

def parse_date_from_filename(filename: str):
    #intenta extraer fecha YYYYMMDD o YYYY-MM-DD del nombre de archivo.
    m = re.search(r'(\d{4})[-_]?(\d{2})[-_]?(\d{2})', filename)
    if m:
        return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3))).date()
    return None
