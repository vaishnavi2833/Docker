import math
import csv

def read_csv(filename):
    with open(filename, mode='r') as file:
        return [row for row in csv.DictReader(file)]

def entropy(data, target):
    freq = {}
    total = len(data)
    for row in data:
        label = row[target]
        freq[label] = freq.get(label, 0) + 1
    
    return -sum((count / total) * math.log2(count / total) for count in freq.values())



def info_gain(data, attr, target):
    freq = {}
    total = len(data)
    
    for row in data:
        value = row[attr]
        freq[value] = freq.get(value, 0) + 1
    
    gain = entropy(data, target)
    for value, count in freq.items():
        subset = [row for row in data if row[attr] == value]
        prob = count / total
        gain -= prob * entropy(subset, target)
    
    return gain

def gini_index(data, attr, target):
    freq = {}
    total = len(data)
    
    for row in data:
        value = row[attr]
        freq[value] = freq.get(value, 0) + 1

    gini = 0.0
    target_mapping = {label: idx for idx, label in enumerate(set(row[target] for row in data))}
    
    for value, count in freq.items():
        subset = [row for row in data if row[attr] == value]
        prob = count / total
        p = [0] * len(target_mapping)  
        for row in subset:
            p[target_mapping[row[target]]] += 1
        
        gini += prob * sum((count / len(subset)) ** 2 for count in p)  

    return 1 - gini

def info_gain_continuous(data, attr, target):
    thresholds = sorted(set(float(row[attr]) for row in data))
    best_gain, best_threshold = 0, None
    
    for threshold in thresholds:
        low = [row for row in data if float(row[attr]) <= threshold]
        low=[]
        high = [row for row in data if float(row[attr]) > threshold]
        if not low or not high:
            continue
        
        gain = entropy(data, target) - (
            len(low) / len(data) * entropy(low, target) +
            len(high) / len(data) * entropy(high, target)
        )
        
        if gain > best_gain:
            best_gain, best_threshold = gain, threshold
    
    return best_gain, best_threshold

def gini_index_continuous(data, attr, target):
    thresholds = sorted(set(float(row[attr]) for row in data))
    best_gini = float('inf')
    
    for threshold in thresholds:
        low = [row for row in data if float(row[attr]) <= threshold]
        high = [row for row in data if float(row[attr]) > threshold]
        if not low or not high:
            continue
        
        gini = 0.0
        target_mapping = {label: idx for idx, label in enumerate(set(row[target] for row in data))}
        
        for subset in (low, high):
            p = [0] * len(target_mapping)
            for row in subset:
                p[target_mapping[row[target]]] += 1
            gini += (1 - sum((count / len(subset)) ** 2 for count in p)) * (len(subset) / len(data))
        
        best_gini = min(best_gini, gini)
    
    return best_gini

data = read_csv('gini.csv')
target_attr = 'NObeyesdad'

attrs = list(data[0].keys())
attrs.remove(target_attr)

for attr in attrs:
    if attr == 'Weight': 
        gain, threshold = info_gain_continuous(data, attr, target_attr)
        gini = gini_index_continuous(data, attr, target_attr)
        print(f"Attribute: {attr} (Threshold: {threshold})")
        print(f"  Info Gain: {gain:.4f}, Gini: {gini:.4f}\n")
    else:
        gain = info_gain(data, attr, target_attr)
        gini = gini_index(data, attr, target_attr)
        print(f"Attribute: {attr}")
        print(f"  Info Gain: {gain:.4f}, Gini: {gini:.4f}\n")
