import csv

def decimal_scaling_normalize(data, col):
    colval = [float(row[col]) for row in data]
    maxi= max(abs(value) for value in colval)
    scale_factor = 10 ** len(str(int(maxi)))
    
    for row in data:
        row[col] = float(row[col]) / scale_factor 
    
    return data

file_path = "./data.csv"

with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
    reader = csv.reader(file)
    headers = next(reader)
    data = [row for row in reader]

col = 1 
normalized_data = decimal_scaling_normalize(data, col)

with open("decimal_normalized_data.csv", 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(headers) 
    writer.writerows(normalized_data)  
