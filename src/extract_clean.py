from pathlib import Path
from src.extract import extract_pdf_tables, extract_pdf_tables_areas
from src.clean_data import clean_csv
from data.dictionary.data_bolivia import PDFConfig

DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "extracted"
CLEAN_DIR = Path(__file__).resolve().parents[1] / "data" / "cleaned"

def extract_clean(pdf_key, pages):
    config = PDFConfig.get_config(pdf_key)
    pdf_path = config['pdf_path']
    type = config['type']
    top_cut = config['all_top_cut']

    # Generar archivos csv de salida
    output_dir_extract = DATA_DIR / f'{pdf_key}'
    output_dir_clean = CLEAN_DIR / f'{pdf_key}'
    
    #si se pide extraer de todas las páginas o solo la primera
    first_page = config['first_page']
    first_res = ''

    if pages == first_page:
        top_cut = config['first_top_cut']

    """ if pages == "all":
        pages = config['all_pages']
        first_top_cut = config['first_top_cut']
        #extraemos primero la 1ra página
        if first_top_cut:
            first_res = extract_pdf_tables_areas(
                pdf_path=pdf_path,
                output_dir=output_dir_extract,
                flavor=config['flavor'],
                pages=first_page,
                top_cut=first_top_cut,
                column_separators=config['column_separators'],
                column_names=config['column_names']
            ) """

    if type == 'normal':
        res = extract_pdf_tables(
            pdf_path=pdf_path,
            output_dir=output_dir_extract,
            flavor = config['flavor'],
            pages = pages,
            column_names = config['column_names']
        )
    elif type == 'areas':
        res = extract_pdf_tables_areas(
            pdf_path=pdf_path,
            output_dir=output_dir_extract,
            flavor=config['flavor'],
            pages=pages,
            top_cut=top_cut,
            column_separators=config['column_separators'],
            column_names=config['column_names']
        )
    else:
        print('especificar tipo de extracción')

    print(res['pdf_date'])

    if first_res:
        clean_csv(input_csv=first_res['csv'][0], output_dir=output_dir_clean, source_pdf=first_res['pdf'], pdf_date=first_res['pdf_date'])

    csvs = res['csv']
    for csv in csvs:
        clean_csv(input_csv=csv, output_dir=output_dir_clean, source_pdf=res['pdf'], pdf_date=res['pdf_date'])