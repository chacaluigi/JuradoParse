import pandas as pd
from pathlib import Path

DATA_BOL_DIR = Path(__file__).resolve().parents[1] / "data" / "dictionary"

from data.dictionary.data_bolivia import BoliviaData

nombres_bolivia = BoliviaData.NOMBRES
nombres_prueba = BoliviaData.NOMBRES_PRUEBA
apellidos_prueba = BoliviaData.APELLIDOS_PRUEBA
docs_prueba = BoliviaData.DOCUMENTOS_PRUEBA

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
    
    if pd.isna(text):
        return pd.Series(['','',''])
    
    parts = str(text).strip().split()

    if len(parts) < 2:
        print(f'ERROR: EXTRACCIÓN NOMBRE INCORRECTO. El nombre {text} no puede ser menor a 2 palabras.')
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



def probar_casos_especiales():
    print("PRUEBA DE CASOS ESPECIALES:")
    print("=" * 80)
    
    """ for caso in nombres_prueba:
        pat, mat, nom = separate_last_and_names(caso)
        print(f"ORIGINAL: {caso}")
        print(f"PATERNO:  {pat}")
        print(f"MATERNO:  {mat}") 
        print(f"NOMBRES:  {nom}")
        print("-" * 50) """

    for caso in apellidos_prueba:
        pat, mat = separate_lastname(caso)
        print(f"ORIGINAL: {caso}")
        print(f"PATERNO:  {pat}")
        print(f"MATERNO:  {mat}") 
        print("-" * 50)

    """ for doc in docs_prueba:
        doc_type, doc_number, comp = normalize_document(doc)
        print(f"ORIGINAL: {doc}")
        print(f"type:     {doc_type}")
        print(f"number:   {doc_number}") 
        print(f"comp:     {comp}")
        print("-" * 50) """

probar_casos_especiales()