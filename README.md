PROYECTO DE EXTRACCIÓN DE PDFS
- pylint, flakeo ruff?
- Un colegio puede tener filiales en varios municipios.
- Un municipio puede tener varios colegios.
## desinstalar java y Tabula-py junto a todo sus archivos residuales y cache en WSL. Después instalar camelot-py
## Subir proyecto en venv Ubuntu a git hub.
## quitar los enumeramientos de las columnas en la extracción de la tabla.
## modificar la función de extract_pdf_tables: unir las tablas encontradas de un pdf, en un solo archivo csv, ya que, las tablas de un pdf tienen el mismo encabezado y formato en todas sus páginas. Además que los pdfs tienen cientos de páginas con tablas.
- Tipos de documentos
- Extraer el 2do pdf

# extraer tablas del pdf
python -m src.extract_tables data/raw/2019-10-20-Elecciones-Generales-Cochabamba.pdf 1-3 lattice
python -m src.extract_tables data/raw/2020-10-18-Elecciones-Generales-Cochabamba.pdf 5-6 stream areas

# limpiar una tabla extraída
python -m src.clean_data data/extracted/2019-10-20-Elecciones-Generales-Cochabamba_combined.csv data/raw/2019-10-20-Elecciones-Generales-Cochabamba.pdf
python -m src.clean_data data/extracted/82___2020-10-18-Elecciones-Generales-Cochabamba.csv

# ejecutar cli.py
python -m src.cli normal ./data/raw/2019-10-20-Elecciones-Generales-Cochabamba.pdf 36-39 lattice

python -m src.cli areas ./data/raw/2020-10-18-Elecciones-Generales-Cochabamba.pdf 51-55 stream

python -m src.cli special ./data/raw/2020-10-18-Elecciones-Generales-Cochabamba.pdf 4 stream 0.180

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