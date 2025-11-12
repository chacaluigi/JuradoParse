import pdfplumber
pdf = "data/raw/2025-10-19-Elecciones-Generales-2V-Cochabamba.pdf"
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
            top_cut = 0.8        
            area=page.crop((0, 0, page.width), top_cut*float(page.height))
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
a = extract_pdf_pdfplumber(pdf, 1, 4)

#paginas: 87, 
#0.968
#w, h = extract_dimensions_page("data/raw/2020-10-18-Elecciones-Generales-Cochabamba.pdf", 96)
#print(f'ancho: {w}, alto: {h}')