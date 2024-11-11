import csv

def support(itemset, transactions):
    count = sum(1 for transaction in transactions if itemset.issubset(transaction))
    return count / len(transactions)

def generate_new_itemsets(prev_itemsets, length):
    new_itemsets = set()
    prev_itemsets = list(prev_itemsets)
    for i in range(len(prev_itemsets)):
        for j in range(i + 1, len(prev_itemsets)):
            combined = prev_itemsets[i].union(prev_itemsets[j])
            if len(combined) == length:
                new_itemsets.add(combined)
    return new_itemsets

def apriori(transactions, min_support):
    transactions = [set(transaction) for transaction in transactions]
    one_itemsets = {frozenset([item]) for transaction in transactions for item in transaction}
    
    current_itemsets = {itemset for itemset in one_itemsets if support(itemset, transactions) >= min_support}
    
    frequent_itemsets = []
    length = 2
    
    while current_itemsets:
        frequent_itemsets.extend(current_itemsets)
        new_itemsets = generate_new_itemsets(current_itemsets, length)
        current_itemsets = {itemset for itemset in new_itemsets if support(itemset, transactions) >= min_support}
        length += 1
    
    return frequent_itemsets

file_path = 'transactions.csv'
transactions = []
with open(file_path, 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        transactions.append(set(row))  

min_support = 0.4
frequent_itemsets = apriori(transactions, min_support)

print("Frequent itemsets:")
for itemset in frequent_itemsets:
    print(itemset)

with open("frequent_itemsets.csv", 'w', newline='') as file:
    writer = csv.writer(file)
    for itemset in frequent_itemsets:
        writer.writerow(list(itemset))