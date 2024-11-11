import pandas as pd

df = pd.read_csv('data.csv')

num_bins = 3

df['Weight_Bin'], bin_edges = pd.cut(df['Weight'], bins=num_bins, retbins=True)

print(df.groupby('Weight_Bin')['Weight'])

df['Mean_Binning'] = df.groupby('Weight_Bin')['Weight'].transform('mean')

df['Median_Binning'] = df.groupby('Weight_Bin')['Weight'].transform('median')

boundary_bins = []
for weight in df['Weight']:
    for i in range(len(bin_edges) - 1):
        if bin_edges[i] <= weight < bin_edges[i + 1]:
            lb = bin_edges[i]
            ub = bin_edges[i + 1]
            if abs(weight - lb) < abs(weight - ub):
                boundary_bins.append(lb)
            else:
                boundary_bins.append(ub)
            break
    else:
        boundary_bins.append(bin_edges[-1]) 

df['Boundary_Binning'] = boundary_bins

print(df[['Gender', 'Weight', 'Mean_Binning', 'Median_Binning', 'Boundary_Binning']])
