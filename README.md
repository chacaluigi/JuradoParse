# JuradoParse

JuradoParse es un proyecto desarrollado para la extracción, limpieza, procesamiento y almacenamiento de datos de personas juradas electorales, a partir de listas oficiales publicadas en formato PDF por el Órgano Electoral Plurinacional (OEP) en su sitio web.

El sistema extrae información clave como nombres completos, número de credencial, recinto de votación y municipio al que pertenece cada persona. Para la extracción de datos desde los archivos PDF se utiliza la librería Camelot de Python. Debido a que este proceso puede generar ruido o inconsistencias en los datos, se aplica una etapa de limpieza y normalización antes de almacenarlos temporalmente en un archivo CSV.

Posteriormente, el proyecto implementa un algoritmo de procesamiento de nombres, que separa el nombre, apellido paterno y apellido materno, guardando cada uno en columnas independientes.

En los casos en los que una persona haya sido jurado electoral en dos o más procesos electorales, el sistema no crea registros duplicados, sino que asocia correctamente todas las elecciones en las que participó.

Finalmente, la información procesada y depurada se almacena de forma persistente en una base de datos PostgreSQL, permitiendo su posterior consulta y análisis.