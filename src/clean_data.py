import os
import pandas as pd
from pathlib import Path
from src.utils import ensure_dir, parse_date_from_filename, normalize_document, separate_last_and_names, separate_lastname
import sys

def clean_csv(input_csv: str, output_dir: str = None, source_pdf=None, pdf_date=None):
    
    input_path = Path(input_csv)
    ensure_dir(output_dir)
    output_csv = output_dir / f"{input_path.stem}_clean.csv"
    if os.path.exists(output_csv):
        os.remove(output_csv)

    df = pd.read_csv(input_csv, dtype=str, keep_default_na=False)

    if 'APELLIDOS Y NOMBRES' in df.columns:
        split_name = df['APELLIDOS Y NOMBRES'].apply(separate_last_and_names)
        df[['APELLIDO_PATERNO', 'APELLIDO_MATERNO', 'NOMBRES']] = split_name
        df.drop(columns='APELLIDOS Y NOMBRES', inplace=True)
        
    elif 'APELLIDOS' in df.columns and 'NOMBRES' in df.columns:
        split_lastname = df['APELLIDOS'].apply(separate_lastname)
        df[['APELLIDO_PATERNO', 'APELLIDO_MATERNO']] = split_lastname
        df.drop(columns='APELLIDOS', inplace=True)

    if 'DOCUMENTO' in df.columns and 'TIPO' not in df.columns:
        split_document = df['DOCUMENTO'].apply(normalize_document)
        df.drop(columns='DOCUMENTO', inplace=True)
        df[['TIPO', 'DOCUMENTO', 'COMP']] = split_document
    
    #limpiar columnas vacías y columnas que no necesitemos
    columns_to_drop = ['MESA', 'Nro.', 'NRO', '', ' ', '   ']
    unnamed_columns = [col for col in df.columns if str(col).startswith('Unnamed')] #para las Unnamed
    columns_to_drop.extend(unnamed_columns)
    df.drop(columns_to_drop, axis=1, inplace=True, errors='ignore')

    if source_pdf:
        df['FUENTE_PDF'] = source_pdf
    
    if pdf_date:
        df['FECHA_PDF'] = pdf_date
    elif source_pdf:
        extracted_date = parse_date_from_filename(source_pdf)
        if extracted_date:
            df['FECHA_PDF'] = extracted_date

     # ordenar columnas
    column_order = ['APELLIDO_PATERNO','APELLIDO_MATERNO','NOMBRES','TIPO','DOCUMENTO','COMP','MUNICIPIO','RECINTO','FUENTE_PDF','FECHA_PDF']
    available_columns = [col for col in column_order if col in df.columns]
    df = df[available_columns]

    df.to_csv(output_csv, index=False, encoding='utf-8')
    print(f"Archivo limpio guardado en: {output_csv}  Dimensiones: {df.shape[0]} filas x {df.shape[1]} columnas")

    return df

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Sin argumentos en la línea de comandos. Colocar los argumentos correctos, ver .README")
    else:
        if len(sys.argv) < 2:
            print("Uso: python clean_data.py <input_csv> [source_pdf] [pdf_date]")
            print("O: python clean_data.py (para ejecutar pruebas)")
            sys.exit(1)
        
        input_csv = sys.argv[1]
        source_pdf = sys.argv[2] if len(sys.argv) > 2 else None
        pdf_date = sys.argv[3] if len(sys.argv) > 3 else None
        
        print(f"Se está procesando el archivo: {input_csv}. Waiting....")
        
        clean_csv(input_csv, source_pdf=source_pdf, pdf_date=pdf_date)