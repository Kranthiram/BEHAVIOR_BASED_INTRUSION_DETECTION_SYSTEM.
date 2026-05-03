# 🔐 Behavior-Based Intrusion Detection System (BBIDS)

A Machine Learning-based Intrusion Detection System that analyzes user behavior to detect anomalies and potential cyber threats in real-time.

---

##  Overview

With the increasing number of cyber threats, traditional intrusion detection systems fail to detect unknown attacks. This project implements a **Behavior-Based Intrusion Detection System (BBIDS)** using Machine Learning techniques to identify abnormal user behavior.

The system monitors:
- Login patterns
- CPU usage
- File access
- Network activity

It uses the **Isolation Forest algorithm** to classify behavior as normal or anomalous.

---

##  Features

- 🔍 Real-time anomaly detection  
- 🤖 Machine Learning-based analysis  
- 🌐 Network traffic monitoring (MITM detection)  
- 📊 Graphical visualization of results  
- 📁 Behavior logs storage and display  
- 🔐 Secure login system  

---

## Technologies Used

### Frontend
- HTML
- CSS
- JavaScript

### Backend
- Node.js
- Express.js

### Machine Learning
- Python
- Scikit-learn (Isolation Forest)

### Tools
- VS Code
- Postman
- mitmproxy

---

## 🏗️ System Architecture

The system consists of four main components:

1. **Frontend (UI)** – Captures user behavior  
2. **Backend (Node.js)** – Processes data and APIs  
3. **Machine Learning Module (Python)** – Detects anomalies  
4. **Traffic Monitoring Module** – Detects MITM attacks  

---

## ⚙️ Working

1. User logs into system  
2. Behavior data is captured (login time, CPU, etc.)  
3. Data sent to backend via REST APIs  
4. ML model analyzes behavior  
5. Output:
   - Normal Behavior
   - Anomaly Detected 🚨  

---

## 📊 Results

- Accuracy: ~95%  
- Low false positive rate  
- Detection latency: ~200 ms  
- Real-time monitoring supported  

---

## ⚠️ Limitations

- Depends on quality of input data  
- May generate false positives  
- Limited behavioral features in current version  

---

## 🔮 Future Scope

- Deep Learning integration  
- Cloud deployment  
- Email/SMS alerts  
- Advanced behavior tracking  
- Enterprise-level scalability  

---
