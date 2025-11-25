import os
import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# Path to save/load the trained model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "severity_model.joblib")

def train_mock_model():
    """
    Trains a simple Random Forest model on dummy clinical data to demonstrate
    local ML capabilities. Saves the model to disk.
    """
    print("Training local ML model...")
    # Dummy Data: [HeartRate, Temp, RR, CRT] -> Severity (0:Low, 1:Med, 2:High)
    data = {
        'heart_rate':       [80,  120, 180, 60,  200, 100, 140, 160, 70,  220],
        'temperature':      [38.5,39.2,37.0,36.5,40.0,38.0,39.5,36.0,38.2,41.0],
        'respiratory_rate': [20,  40,  60,  15,  80,  25,  50,  10,  22,  90],
        'capillary_refill': [1.0, 2.0, 3.0, 1.0, 4.0, 1.0, 2.0, 3.0, 1.0, 4.0], 
        'severity_class':   [0,   1,   2,   1,   2,   0,   1,   2,   0,   2] 
    }
    df = pd.DataFrame(data)
    X = df.drop('severity_class', axis=1)
    y = df['severity_class']
    
    model = RandomForestClassifier(n_estimators=20, random_state=42)
    model.fit(X, y)
    
    joblib.dump(model, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")
    return model

def predict_severity(vitals: dict):
    """
    Predicts severity based on vitals using the local ML model.
    Returns a dict with probability and label.
    """
    try:
        if not os.path.exists(MODEL_PATH):
            model = train_mock_model()
        else:
            model = joblib.load(MODEL_PATH)
            
        # Prepare input vector (must match training order)
        # Default values represent a "healthy" average to avoid skewing if missing
        input_data = pd.DataFrame([{
            'heart_rate':       float(vitals.get('heart_rate', 100)),
            'temperature':      float(vitals.get('temperature', 38.5)),
            'respiratory_rate': float(vitals.get('respiratory_rate', 24)),
            'capillary_refill': float(vitals.get('capillary_refill', 1.5))
        }])
        
        # Predict
        prediction_class = model.predict(input_data)[0]
        probs = model.predict_proba(input_data)[0]
        
        # Map class to label
        severity_map = {0: "Low Risk", 1: "Moderate Risk", 2: "High Risk (Critical)"}
        severity_label = severity_map.get(prediction_class, "Unknown")
        
        # Probability of the predicted class
        confidence = round(probs[prediction_class] * 100, 1)
        
        return {
            "ml_prediction": severity_label,
            "confidence": confidence,
            "model_used": "RandomForestClassifier (Local)"
        }
    except Exception as e:
        print(f"ML Prediction Error: {e}")
        return {"error": str(e)}
