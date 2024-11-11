import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

data=pd.read_csv ('regdata.csv')

X = data['Weight'].values
y = data['Age'].values

N = len(X) 
sum_x = np.sum(X)
print(sum_x)
sum_y = np.sum(y)
print(sum_y)
sum_xy = np.sum(X * y)
print(sum_xy)
sum_x_squared = np.sum(X**2)
print(sum_x_squared)


m = (N * sum_xy - sum_x * sum_y) / (N * sum_x_squared - sum_x**2)
c = (sum_y * sum_x_squared - sum_x*sum_xy)/(N * sum_x_squared - sum_x**2)

print(f"Slope (m): {m}")
print(f"Intercept (b): {c}")

y_pred = m * X + c

plt.scatter(X, y, color='blue', label='Data points')
plt.plot(X, y_pred, color='red', label='Regression line')
plt.xlabel('Weight')
plt.ylabel('Age')
plt.title('Linear Regression')
plt.legend()
plt.show()

