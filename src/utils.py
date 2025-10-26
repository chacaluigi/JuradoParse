from pathlib import Path
from datetime import datetime
import re
from PyPDF2 import PdfReader
import pandas as pd
import pdfplumber

from data.dictionary.data_bolivia import BoliviaData
nombres_bolivia = BoliviaData.NOMBRES

def separate_last_and_first_names(text):

    if pd.isna(text):
        return pd.Series(['','',''])
    
    parts=str(text).strip().split()

    if len(parts) < 2:
        print(f'ERROR: EXTRACCIÓN NOMBRE INCORRECTO. El nombre {text} no puede ser menos de 2 palabras.')
        return pd.Series([text, '', ''])
    
    conectors={'de', 'del', 'la', 'tezanos', 'le'}

    processed_parts = []
    i=0
    while i<len(parts):
        current_part=parts[i]

        if current_part.lower() in conectors and parts[i+1].lower() in conectors and i+2 < len(parts):
            combined = f"{current_part} {parts[i+1]} {parts[i+2]}"
            processed_parts.append(combined)
            i+=3
        elif current_part.lower() in conectors and i+1<len(parts):
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

def repair_columns_mixed(table_list):
    for table in table_list:
        df = table.df.fillna('')  # reemplaza NaN con strings vacíos
        
        for idx in range(len(df)):
            #se usa .iloc para acceso seguro por índice
            recinto = str(df.iloc[idx, 3]) if pd.notna(df.iloc[idx, 3]) else ''
            mesa = str(df.iloc[idx, 4]) if pd.notna(df.iloc[idx, 4]) else ''
            
            pattern = r'\d{1,2}$'
            pattern_number = r'^\d+$'
            
            
            cambios_realizados = False
            
            if recinto == '' and mesa != '':
                print(f'Fila {idx}: Recinto vacío, Mesa tiene contenido')
                recinto = mesa
                mesa = ''
                cambios_realizados = True
            
            if mesa == '' and recinto != '':
                print(f'Fila {idx}: Mesa vacío, Recinto tiene contenido')
                match = re.search(pattern, recinto)
                if match:
                    print('mesa: ',mesa, 'recinto: ', recinto)
                    mesa = match.group(0)
                    recinto = re.sub(pattern, '', recinto).strip()
                    print('mesa: ',mesa, 'recinto: ', recinto)
                    cambios_realizados = True
            
            match_number = re.search(pattern_number, recinto)

            if match_number:
                print(f'Fila {idx}: Recinto es solo número, moviendo a Mesa')
                recinto = mesa
                mesa = match_number.group(0)
                cambios_realizados = True
            
            if cambios_realizados:
                print(f'Fila {idx}: cambios realizados, con: ', recinto, '/', mesa)
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
        combined_csv = output_dir / f"{pages}___{pdf_path.stem}.csv"
        combined_df.to_csv(combined_csv, index=False, header=False)
        csv_paths.append(str(combined_csv))
        print(f"guardado en: {combined_csv}  Dimensiones: {combined_df.shape[0]} filas x {combined_df.shape[1]} columnas")
    return csv_paths

def extract_dimensions_page(pdf_file, page_number):
    with pdfplumber.open(pdf_file) as pdf:
        page = pdf.pages[page_number+1]
    return page.width, page.height

def parse_date_from_filename(filename: str):
    #intenta extraer fecha YYYYMMDD o YYYY-MM-DD del nombre de archivo.
    m = re.search(r'(\d{4})[-_]?(\d{2})[-_]?(\d{2})', filename)
    if m:
        return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3))).date()
    return None

def normalize_document(doc_text):
    complement=''
    if pd.isna(doc_text):
        return pd.Series(['','',''])
    
    parts=str(doc_text).strip().split('-', 1)

    if parts[0].upper() == 'I':
        doc_type='C.I.'
    elif parts[0].upper() == 'P':
        doc_type='PAS.'
    else:
        doc_type=parts[0]

    doc_number=parts[1]
    
    return pd.Series([doc_type, doc_number, complement]) 



