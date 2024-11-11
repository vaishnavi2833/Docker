import pandas as pd

df = pd.read_csv('bayesdata.csv')

def calculate_class_probabilities(data):
    class_counts = data['NObeyesdad'].value_counts().to_dict()
    total_count = len(data)
    priors = {cls: count / total_count for cls, count in class_counts.items()}
    return priors

def calculate_likelihood(data, feature, value, target_class):
    class_data = data[data['NObeyesdad'] == target_class]
    if len(class_data) == 0:
        return 0
    likelihood = len(class_data[class_data[feature] == value]) / len(class_data)
    return likelihood

def get_feature_probabilities(data):
    classes = data['NObeyesdad'].unique()
    features = ['Gender', 'MTRANS']
    
    probabilities = []
    for cls in classes:
        cls_probs = {'Class': cls}
        for feature in features:
            feature_values = data[feature].unique()
            for value in feature_values:
                likelihood = calculate_likelihood(data, feature, value, cls)
                cls_probs[f'{feature}_{value}'] = likelihood
        probabilities.append(cls_probs)
    
    return pd.DataFrame(probabilities)

def classify(data, gender, transport):
    priors = calculate_class_probabilities(data)
    classes = data['NObeyesdad'].unique()
    scores = {}

    feature_probs = get_feature_probabilities(data)
    print("Feature Probabilities Table:")
    print(feature_probs)

    print("\nCalculations:")
    for cls in classes:
        prior = priors[cls]
        gender_prob = calculate_likelihood(data, 'Gender', gender, cls)
        transport_prob = calculate_likelihood(data, 'MTRANS', transport, cls)

        print(f"\nClass: {cls}")
        print(f"Prior (P({cls})): {prior}")
        print(f"P(Gender={gender} | Class={cls}): {gender_prob}")
        print(f"P(MTRANS={transport} | Class={cls}): {transport_prob}")
        
        # Calculate the final score (posterior probability) for each class
        score = prior * gender_prob * transport_prob
        scores[cls] = score
        print(f"Score (P({cls} | Gender={gender}, MTRANS={transport})): {score}")

    best_class = max(scores, key=scores.get)
    return best_class, scores

gender_input = 'Male'
mtrans_input = 'walking'

predicted_class, scores = classify(df, gender_input, mtrans_input)

print(f"\nPredicted Class: {predicted_class}")
print(f"Scores: {scores}")
