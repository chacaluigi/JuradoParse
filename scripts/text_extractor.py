import pdfplumber
pdf = "data/raw/2025-10-19-Elecciones-Generales-2V-Cochabamba.pdf"
#pdf = "data/raw/2021-03-07-Elecciones-Subnacionales-Cochabamba.pdf"
def extract_dimensions_page(pdf_file, page_number):
    with pdfplumber.open(pdf_file) as pdf:
        page = pdf.pages[page_number]
    return page.width, page.height

def extract_pdf_pdfplumber(pdf_file, page_number, area_number):
    with pdfplumber.open(pdf_file) as pdf:
        page=pdf.pages[page_number-1]

        if area_number == 1:
            area=page.crop((0, 0, 1/3*float(page.width), page.height))
        elif area_number == 2:
            area=page.crop((1/3*float(page.width), 0, 2*1/3*float(page.width), page.height))
        elif area_number == 3:        
            area=page.crop((2/3*float(page.width), 0, page.width, page.height))
        elif area_number == 4:
            x1 = float(page.width) * 0
            y1 = float(page.height) * 0.18
            x2 = float(page.width) * 1
            y2 = float(page.height) * 0.95
            area=page.crop((x1,y1,x2,y2))
        elif area_number == 5:
            page_width = page.width
            page_height = page.height
            coord_multiplier = [0, 0.18, 1, 0.95]
            #coord_multiplier = [0.01, 0, 0.99, 1]
            mx1, my1, mx2, my2 = coord_multiplier
            x1, y1, x2, y2 = mx1*float(page_width), my1*float(page_height), mx2*float(page_width), my2*float(page_height)
            page_width = x2-x1
            page_height = y2-y1
            table_areas_list = [
                [x1, y1, 1/3*float(page_width)+x1, y2],
                [1/3*float(page_width) + x1, y1, 2/3*float(page_width) + x1, y2],
                [2/3*float(page_width) + x1, y1, page_width + x1, y2],
            ]
            area = page.crop(table_areas_list[2])
        else:
            a = 0
            b = 415.67
            area=page.crop((a, 0, b, 900))

        print(f'ancho: {area.width}, alto: {area.height}')
        im=area.to_image(resolution=150)
        im.save(f"area{page_number}_{area_number}.png", format="PNG")
    return area
columns = [
        ['88.10,117.30,165.70,242.95'],
        ['337.5,365.7,414.67,491.90'],
        ['585.90,614.3,662.92,738.95']
    ]
a = extract_pdf_pdfplumber(pdf, 50, 5)

#paginas: 87, 
#0.968
#w, h = extract_dimensions_page("data/raw/2020-10-18-Elecciones-Generales-Cochabamba.pdf", 96)
#print(f'ancho: {w}, alto: {h}')