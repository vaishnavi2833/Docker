import csv

def min_max_normalize(data, col):
    min_max_values = {}
    colval = [float(row[col]) for row in data]
    mini = min(colval)
    maxi= max(colval)
    
    for row in data:
        row[col] = (float(row[col]) - mini) / (maxi - mini)
    
    return data

file_path = "./data.csv"

with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
    reader = csv.reader(file)
    headers = next(reader)
    data = [row for row in reader]

col = 1 

normalized_data = min_max_normalize(data, col)

with open("normalized_data.csv", 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(headers) 
    writer.writerows(normalized_data)  
