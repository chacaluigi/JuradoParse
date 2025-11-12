def generate_groped_ranges(text: str, first_special_page: str, reason: int):
    start_str, end_str = text.split('-')
    start = int(start_str)
    end = int(end_str)
    
    if start > end:
        print("Error: El número de inicio es mayor que el número final.")
        return []
    
    ranges = []
    if first_special_page:
        ranges.append(str(start))
        start += 1
        
    current_start = start
    while current_start <= end:
        range_end = current_start + reason - 1
        
        # formateamos en caso que esté en el límite
        if range_end > end:
            range_end = end
        
        range_str = f"{current_start}-{range_end}"
        ranges.append(range_str)
        
        current_start = range_end + 1
        
    return ranges

text = '23-50'
first = '1.58'
reason = 4
if '-' in text:
    page_groups = generate_groped_ranges(text, first, reason)
else:
    print('luigii')

for group in page_groups:
    print(group, type(group))