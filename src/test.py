
""" 
I-6445002
C.I.     12620864
R-3019-071080A
C.I. 5575289 - 1V
"""

import re


pruebas = ["I-6445002", "C.I.     12620864", "R-3019-071080A", "C.I. 5575289 - 1V", "P-9345302"]
separadores = r"\s+|-"
for item in pruebas:
    divisiones = re.split(separadores, item.strip())
    item_filtrado = [subitem for subitem in divisiones if subitem]
    print(item_filtrado)
