import pandas as pd

data = pd.read_csv('transactions.csv', header=None)  

item_sets = [set(row.astype(str)) for _, row in data.iterrows()] 

items = sorted(set(item for sublist in item_sets for item in sublist))  
binary_matrix = []

for items_in_set in item_sets:
    binary_vector = [1 if item in items_in_set else 0 for item in items]
    binary_matrix.append(binary_vector)

df = pd.DataFrame(binary_matrix, columns=items)
print(f"Shape of the binary matrix: {df.shape}")  
print(df)

def correlation(x, y):
    n = len(x)
    sum_x = sum(x)
    sum_y = sum(y)
    sum_x_squared = sum(xi ** 2 for xi in x)
    sum_y_squared = sum(yi ** 2 for yi in y)
    sum_xy = sum(xi * yi for xi, yi in zip(x, y))

    numerator = n * sum_xy - sum_x * sum_y
    denominator = ((n * sum_x_squared - sum_x ** 2) * (n * sum_y_squared - sum_y ** 2)) ** 0.5

    if denominator == 0:
        return None  

    return numerator / denominator

correlation_results = {}

for i in range(len(items)):
    for j in range(i + 1, len(items)):
        item1 = items[i]
        item2 = items[j]
        correlation = correlation(df[item1], df[item2])
        correlation_results[(item1, item2)] = correlation

print("Pearson Correlation Coefficients:")
for (item1, item2), correlation in correlation_results.items():
    print(f"{item1} and {item2}: {correlation:.4f}" if correlation is not None else f"{item1} and {item2}: Undefined")
