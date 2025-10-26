from pathlib import Path
import camelot

pdf_path = 'data/raw/2020-10-18-Elecciones-Generales-Cochabamba.pdf'
pages = '22'
flavor='stream'
table_areas_list = [
    ['0,0,250.39,992.13'],
    ['250.39,0,500.79,992.13'],
    ['500.79,0,751.18,992.13']
]
columns = [
    ['78.10,113.30,154.7,244.17'],
    ['338.5,366.7,415.67,492.93'],
    ['587.14,615.14,663.92,740.95']
]

tables = camelot.read_pdf(
    pdf_path, 
    pages=pages, 
    flavor=flavor, 
    split_text=False,
    flag_size=True, 
    table_areas=table_areas_list[2],
    columns=columns[2]
)

table = tables[0]

print(table.df)
print("Posiciones de columnas detectadas:", table.cols)

table.to_csv("./ejemplo.csv", index=False, header=False)