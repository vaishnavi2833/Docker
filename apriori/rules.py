import csv
from itertools import combinations

file_path='transactions.csv'
transactions = []
with open(file_path, 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        transactions.append(set(row)) 

def support(itemset, transactions):
    count = sum(1 for transaction in transactions if itemset.issubset(transaction))
    return count / len(transactions)

def confidence(prev, after, transactions):
    prev_support = support(prev, transactions)
    if prev_support == 0:
        return 0
    combined_support = support(prev.union(after), transactions)
    return combined_support / prev_support

def generate_rules(itemset, transactions, min_confidence):
    rules = []
    for i in range(1, len(itemset)):
        prev_combinations = combinations(itemset, i)
        for prev in prev_combinations:
            prev = frozenset(prev)
            next = frozenset(itemset - prev)
            conf = confidence(prev, next, transactions)
            if conf >= min_confidence:
                support_value = support(itemset, transactions)
                rules.append({
                    'antecedent': prev,
                    'consequent': next,
                    'confidence': conf,
                    'support': support_value,
                })
    return rules

def apriori_with_rules(transactions, frequent_itemsets, min_confidence):
    rules = []
    for itemset in frequent_itemsets:
        if len(itemset) > 1:  # Generate rules only for itemsets with more than 1 item
            rules.extend(generate_rules(itemset, transactions, min_confidence))
    
    return rules

def print_results(frequent_itemsets, rules):
    print("\nFrequent Itemsets:")
    print("==================")
    for itemset in frequent_itemsets:
        support_value = support(itemset, transactions)
        items = ', '.join(sorted(itemset))
        print(f"Items: {{{items}}} (Support: {support_value:.3f})")
    
    print("\nAssociation Rules:")
    print("=================")
    for rule in rules:
        ant = ', '.join(sorted(rule['antecedent']))
        cons = ', '.join(sorted(rule['consequent']))
        print(f"{{{ant}}} => {{{cons}}}")
        print(f"Confidence: {rule['confidence']:.3f}")
        print(f"Support: {rule['support']:.3f}")
        print("-" * 50)

def main():
    file_path = 'transactions.csv'
    transactions = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            transactions.append(set(row))
    
    
    frequent_itemsets = []
    with open('frequent_itemsets.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            frequent_itemsets.append(frozenset(row))  
    
    min_confidence = 0.7
    
    rules = apriori_with_rules(transactions, frequent_itemsets, min_confidence)
    
    print_results(frequent_itemsets, rules)

if __name__ == "__main__":
    main()
