import pandas as pd
from pathlib import Path
from src.utils import parse_date_from_filename, normalize_document, separate_last_and_first_names
import sys

CLEAN_DIR = Path(__file__).resolve().parents[1] / "data" / "cleaned"

def clean_csv(input_csv: str, output_csv: str = None, source_pdf=None, pdf_date=None):
    
    if output_csv is None:
        input_path = Path(input_csv)
        output_csv = CLEAN_DIR / f"{input_path.stem}_clean.csv"

    df = pd.read_csv(input_csv, dtype=str, keep_default_na=False)

    if 'APELLIDOS Y NOMBRES' in df.columns:
        split_name = df['APELLIDOS Y NOMBRES'].apply(separate_last_and_first_names)
        df[['APELLIDO_PATERNO', 'APELLIDO_MATERNO', 'NOMBRES']] = split_name
        df = df.drop(columns='APELLIDOS Y NOMBRES')
    
    if 'DOCUMENTO' in df.columns:
        split_document = df['DOCUMENTO'].apply(normalize_document)
        df[['TIPO', 'DOC_NUMBER', 'COMP']] = split_document
        df = df.drop(columns='DOCUMENTO')
        df = df.rename(columns={'DOC_NUMBER': 'DOCUMENTO'})
    
    #ordenar columnas
    end_columns = ['MUNICIPIO', 'RECINTO', 'MESA']
    all_columns = df.columns.tolist()
    first_columns = [col for col in all_columns if col not in end_columns]
    new_columns = first_columns + end_columns
    df = df[new_columns]

    if source_pdf:
        df['FUENTE_PDF'] = source_pdf
    
    if pdf_date:
        df['FECHA_PDF'] = pdf_date
    elif source_pdf:
        extracted_date = parse_date_from_filename(source_pdf)
        if extracted_date:
            df['FECHA_PDF'] = extracted_date

    

    df.to_csv(output_csv, index=False, encoding='utf-8')
    print(f"Archivo limpio guardado en: {output_csv}")

    return df

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Solo un argumento. Colocar los argumentos correctos, ver .README")
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