from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd
import os
import json

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Load the trained model
model_path = os.path.join(os.path.dirname(__file__), '..', 'model', 'intrusion_model.pkl')

try:
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    print("✅ Model loaded successfully")
except:
    print("⚠️ Model not found, training new one...")
    from sklearn.ensemble import IsolationForest
    import numpy as np
    
    # Create synthetic training data
    normal_data = pd.DataFrame({
        'login_hour': np.random.normal(9, 2, 400),
        'files_accessed': np.random.normal(15, 5, 400),
        'cpu_usage': np.random.normal(30, 10, 400),
        'network_packets': np.random.normal(500, 100, 400)
    })
    anomaly_data = pd.DataFrame({
        'login_hour': np.random.uniform(0, 23, 100),
        'files_accessed': np.random.uniform(50, 200, 100),
        'cpu_usage': np.random.uniform(80, 100, 100),
        'network_packets': np.random.uniform(1000, 5000, 100)
    })
    
    X_train = pd.concat([normal_data, anomaly_data])
    model = IsolationForest(contamination=0.2, random_state=42)
    model.fit(X_train)
    print("✅ New model trained")

@app.route('/predict', methods=['POST'])
def predict():
    """Predict if behavior is anomalous"""
    try:
        data = request.json
        features = pd.DataFrame([[
            data['login_hour'],
            data['files_accessed'],
            data['cpu_usage'],
            data['network_packets']
        ]], columns=['login_hour', 'files_accessed', 'cpu_usage', 'network_packets'])
        
        prediction = model.predict(features)
        is_anomaly = bool(prediction[0] == -1)
        
        return jsonify({'anomaly': is_anomaly})
    except Exception as e:
        return jsonify({'anomaly': False, 'error': str(e)})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'running', 'model_loaded': True})

if __name__ == '__main__':
    app.run(port=5001, debug=True)