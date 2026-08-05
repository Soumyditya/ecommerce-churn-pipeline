import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

def run_modeling():
    processed_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed')
    
    # Load processed customers
    print("Loading processed customer data...")
    df = pd.read_csv(os.path.join(processed_dir, 'customers_processed.csv'))
    
    # Define Churn: 1 if recency > 180 days, else 0
    print("Defining churn (Target Variable)...")
    df['is_churn'] = (df['recency'] > 180).astype(int)
    
    # Features for ML Model
    features = ['age', 'recency', 'frequency', 'monetary']
    X = df[features]
    y = df['is_churn']
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train Model
    print("Training Random Forest Classifier...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate
    predictions = model.predict(X_test)
    print("\nModel Evaluation:")
    print(f"Accuracy: {accuracy_score(y_test, predictions):.2f}")
    print(classification_report(y_test, predictions))
    
    # Predict probabilities for the entire dataset
    df['churn_probability'] = np.round(model.predict_proba(X)[:, 1], 2)
    
    # Save predictions
    df.to_csv(os.path.join(processed_dir, 'customers_with_predictions.csv'), index=False)
    print("Predictions saved to data/processed/customers_with_predictions.csv")

if __name__ == "__main__":
    run_modeling()
