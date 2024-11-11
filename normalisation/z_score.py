import csv
import math

def z_score_normalize(data, col):
    col_values = [float(row[col]) for row in data]
    mean = sum(col_values) / len(col_values)
    variance = sum((x - mean) ** 2 for x in col_values) / len(col_values)
    std_dev = math.sqrt(variance)
    
    for row in data:
        row[col] = (float(row[col]) - mean) / std_dev
    
    return data

file_path = "./data.csv" 

with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
    reader = csv.reader(file)
    headers = next(reader) 
    data = [row for row in reader]  

col = 1
normalized_data = z_score_normalize(data, col)

print(headers)
for row in normalized_data:
    print(row)

with open("z_score_normalized_data.csv", 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    writer.writerows(normalized_data)  
