def generate_groped_ranges(text: str):
    try:
        start_str, end_str = text.split('-')
        start = int(start_str)
        end = int(end_str)
    except ValueError:
        #En caso de que el formato no sea 'N-N'
        print(f"Error: el formato de '{text}' no es válido (debe ser 'inicio-fin').")
        return []
    
    if start > end:
        print("Error: El número de inicio es mayor que el número final.")
        return []
    
    ranges = []
    
    current_start = start
    while current_start <= end:
        range_end = current_start + 9
        
        # formateamos en caso que esté en el límite
        if range_end > end:
            range_end = end
        
        range_str = f"{current_start}-{range_end}"
        ranges.append(range_str)
        
        current_start = range_end + 1
        
    return ranges

text = '23-23'
if '-' in text:
    page_groups = generate_groped_ranges(text)
else:
    print('luigii')

for group in page_groups:
    print(group, type(group))