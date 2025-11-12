PROYECTO DE EXTRACCIÓN DE PDFS
- pylint, flakeo ruff?
- Un colegio puede tener filiales en varios municipios.
- Un municipio puede tener varios colegios.
## desinstalar java y Tabula-py junto a todo sus archivos residuales y cache en WSL. Después instalar camelot-py
## Subir proyecto en venv Ubuntu a git hub.
## quitar los enumeramientos de las columnas en la extracción de la tabla.
## modificar la función de extract_pdf_tables: unir las tablas encontradas de un pdf, en un solo archivo csv, ya que, las tablas de un pdf tienen el mismo encabezado y formato en todas sus páginas. Además que los pdfs tienen cientos de páginas con tablas.
## Tipos de documentos
## Extraer el 2do pdf


## PROBLEMAS EN LA EXTRACCIÓN
python -m src.cli 2021_ES_CBBA 5-6

ACUÑA GOMEZ FAUSTINO,I-8804647,Villa Tunari,Unidad Educativa 1ro de Mayo,1
ACUÑA GUTIERREZ PRIMITIVA,I-7991132,San Benito (Villa José Quintín Mendoza)Unidad Educativa Wañakahua,,1
ACUÑA TORRICO HILARIA,I-9371689,San Benito (Villa José Quintín Mendoza)Colegio Simon Bolivar (Huaricaya),,1
AGUILAR ROJAS JHONATAN,I-6548643,San Benito (Villa José Quintín Mendoza)U. E. 27 de Mayo (Ex Jose B. Pereira),,1
ALBA TORRICO HILDA,I-3135570,San Benito (Villa José Quintín Mendoza)U. E. 27 de Mayo (Ex Jose B. Pereira),,1

page18
CANAVIRI FERNANDEZ MARIA,,,,
DE LOS ANGELES LUCET,I-9478016,Sacaba,Unidad Educativa Hernán Rivero Fiorilo,3

## PROBLEMS EN LA DIVISION DE NOMBRES
* Existen nombres que son apellidos a la vez.
FRANCO
VICENTE

- dividir la función "separate_last_and_names", para separar primero apellidos de nombres ya luego los apellidos en paterno y materno

# extraer tablas del pdf
python -m src.extract_tables data/raw/2019-10-20-Elecciones-Generales-Cochabamba.pdf 1-3 lattice
python -m src.extract_tables data/raw/2020-10-18-Elecciones-Generales-Cochabamba.pdf 5-6 stream areas

# limpiar una tabla extraída
python -m src.clean_data data/extracted/2019-10-20-Elecciones-Generales-Cochabamba_combined.csv data/raw/2019-10-20-Elecciones-Generales-Cochabamba.pdf
python -m src.clean_data data/extracted/82___2020-10-18-Elecciones-Generales-Cochabamba.csv

# ejecutar cli.py
python -m src.cli 2019_EG_CBBA 1-505
python -m src.cli 2020_EG_CBBA 4-97
python -m src.cli 2021_ES_CBBA 4-99
python -m src.cli 2024_EJ_CBBA 16-337
python -m src.cli 2025_EG_CBBA 2-351
python -m src.cli 2025_EG_2V_CBBA 1-1906

2019
152-304 | 153 | 96 seg
2020
4-30 | 78 | 75 seg
2021
4-29 | 76 | 120 seg
2024
16-112 | 96 | 100 seg



48-60 | 43 seg
101-136 | 
# propiedades camelot

tables = camelot.read_pdf(
    str(pdf_path),
    flavor='lattice',
    copy_text=['h', 'v'],  # Para texto en bordes
    split_text=True,       # Para dividir texto entre celdas  
    flag_size=True,        # Para detectar estructura
    strip_text='\n',       # Para limpiar datos
    line_scale=40,         # Más sensible a líneas
    layout_kwargs={'detect_vertical': False}  # A veces ayuda
)



package de un principio

Package            Version
---
cffi               2.0.0
charset-normalizer 3.4.4
cryptography       46.0.2
pdfminer.six       20250506
pdfplumber         0.11.7
pillow             11.3.0
pip                24.0
pycparser          2.23
PyPDF2             3.0.1
pypdfium2          4.30.0


5247476
3496704

