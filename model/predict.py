import sys
import pickle
import pandas as pd
import os

# Load model
model_path = os.path.join(os.path.dirname(__file__), 'intrusion_model.pkl')

with open(model_path, 'rb') as f:
    model = pickle.load(f)

# Get input from command line
login_hour = float(sys.argv[1])
files_accessed = float(sys.argv[2])
cpu_usage = float(sys.argv[3])
network_packets = float(sys.argv[4])

# Predict
features = pd.DataFrame([[login_hour, files_accessed, cpu_usage, network_packets]], 
                        columns=['login_hour', 'files_accessed', 'cpu_usage', 'network_packets'])
prediction = model.predict(features)

# Output 1 for anomaly (-1), 0 for normal (1)
print(1 if prediction[0] == -1 else 0)