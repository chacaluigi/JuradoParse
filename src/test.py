
""" 
I-6445002
C.I.     12620864
R-3019-071080A
C.I. 5575289 - 1V
"""

import re


pruebas = ["I-6445002", "C.I.     12620864", "R-3019-071080A", "C.I. 5575289 - 1V", "P-9345302"]
separators = r"\s+|-"
for doc_text in pruebas:
    divisions = re.split(separators, str(doc_text).strip())
    parts = [item for item in divisions if item]
    print(parts)
