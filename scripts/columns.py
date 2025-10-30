from pathlib import Path
import camelot

pdf_path = 'data/raw/2021-03-07-Elecciones-Subnacionales-Cochabamba.pdf'
pages = '57'
flavor='stream'
table_areas_list = [
    ['0,0,250.39,992.13'],
    ['250.39,0,500.79,992.13'],
    ['500.79,0,751.18,992.13']
]
""" columns = [
    ['88.10,117.30,165.70,242.95'],
    ['338.5,366.7,415.67,492.93'],
    ['587.14,615.14,663.92,740.95']
] """
columns = [
        ['88.10,117.30,165.70,242.95'],
        ['337.5,365.7,415,491.90'],
        ['585.90,614.3,662.92,738.95']
    ]

area = 1

tables = camelot.read_pdf(
    pdf_path, 
    pages=pages, 
    flavor=flavor, 
    split_text=False,
    flag_size=True, 
    table_areas=table_areas_list[area],
    columns=columns[area]
)

table = tables[0]

print(table.df)
print("Posiciones de columnas detectadas:", table.cols)

table.to_csv("./ejemplo.csv", index=False, header=False)