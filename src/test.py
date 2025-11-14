from reportlab.pdfgen import canvas

c = canvas.Canvas("linea_vertical.pdf")

# (x1, y1, x2, y2)
# Dibuja una línea vertical en la posición X=100, desde Y=50 (abajo) hasta Y=700 (arriba)
c.line(100, 50, 100, 700) 

c.showPage()
c.save()