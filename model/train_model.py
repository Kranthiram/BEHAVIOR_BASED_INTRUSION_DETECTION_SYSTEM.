import pandas as pd
import matplotlib.pyplot as plt
import pickle

# Load dataset
data = pd.read_excel(r"C:\Users\KRANTHI\Downloads\login_anomaly_data_500_records (1).xlsx")

# Features
X = data[['login_hour', 'files_accessed', 'cpu_usage', 'network_packets']]

# ✅ Load trained model
with open("intrusion_model.pkl", "rb") as f:
    model = pickle.load(f)

# Predict
data['anomaly'] = model.predict(X)

# Convert labels
# 1 → Normal, -1 → Intrusion
data['anomaly'] = data['anomaly'].map({1: 0, -1: 1})

# Plot graph
plt.figure()
plt.scatter(data['login_hour'], data['cpu_usage'], c=data['anomaly'])
plt.xlabel("Login Hour")
plt.ylabel("CPU Usage")
plt.title("Anomaly Detection Graph")
plt.show()