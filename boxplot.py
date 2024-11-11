import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('data.csv')
data = df['Weight']

min_value = data.min()
q1 = data.quantile(0.25)

median = data.median()
q3 = data.quantile(0.75)
max_value = data.max()
iqr=q3-q1

five_number_summary = {
    'Minimum': min_value,
    'Q1 (25th percentile)': q1,
    'Median (Q2)': median,
    'Q3 (75th percentile)': q3,
    'Maximum': max_value
}

print("Five-Number Summary:")
for key, value in five_number_summary.items():
    print(f"{key}: {value:.2f}")

plt.figure(figsize=(10, 6))
sns.boxplot(x=data, color='lightblue')
plt.title('Box Plot of Weight')
plt.xlabel('Weight')
plt.xlim(q1-1.5*iqr,q3+1.5*iqr) 

plt.grid(axis='x')
plt.show()
plt.close()