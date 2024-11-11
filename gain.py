import pandas as pd
import numpy as np
from collections import Counter

def entropy(labels):
    counts = Counter(labels)
    probs = [count / len(labels) for count in counts.values()]
    return -sum(p * np.log2(p) for p in probs)

def information_gain(data, attribute, target='NObeyesdad'):

    parent_entropy = entropy(data[target])
    attribute_values = data[attribute].value_counts()
    
    weighted_entropy = 0
    total_samples = len(data)
    
    for value in attribute_values.index:
        subset = data[data[attribute] == value]
        subset_weight = len(subset) / total_samples
        subset_entropy = entropy(subset[target])
        weighted_entropy += subset_weight * subset_entropy
    
    information_gain = parent_entropy - weighted_entropy
    return information_gain

def main():
    data = pd.read_csv('alldata.csv')
    info_gain = information_gain(data,'Gender')
    print(info_gain)

if __name__ == "__main__":
    main()