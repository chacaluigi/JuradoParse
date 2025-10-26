import pandas as pd
from io import StringIO

data = """
APELLIDOS Y NOMBRES,DOCUMENTO,MUNICIPIO,RECINTO ELECTORAL,MESA
I-9451431,VILLACA TERRAZAS ROXANA ROCIO,Cochabamba,Colegio La Salle,15
VIDOVIC SANCHEZ PABLO ROBERTO,I-3783435,Cochabamba,Colegio San Rafael19
"""

df = pd.read_csv(StringIO(data))

print(df.columns['DOCUMENTO'])
