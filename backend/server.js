const express = require("express");
const cors = require("cors");
const bodyParser = require("body-parser");
const fs = require("fs");
const path = require("path");

const app = express();
app.use(cors());
app.use(bodyParser.json());

let users = [];
let logs = [];

// File paths
const USERS_FILE = path.join(__dirname, "login.json");
const LOGS_FILE = path.join(__dirname, "logs.json");

// Load existing data
if (fs.existsSync(USERS_FILE)) {
    users = JSON.parse(fs.readFileSync(USERS_FILE));
}
if (fs.existsSync(LOGS_FILE)) {
    logs = JSON.parse(fs.readFileSync(LOGS_FILE));
}

// Save data periodically
function saveData() {
    fs.writeFileSync(USERS_FILE, JSON.stringify(users, null, 2));
    fs.writeFileSync(LOGS_FILE, JSON.stringify(logs, null, 2));
}

// REGISTER
app.post("/api/register", (req, res) => {
    const { username, password } = req.body;
    if (users.find(u => u.username === username)) {
        return res.status(400).send({ message: "User already exists" });
    }
    users.push({ username, password });
    saveData();
    res.send({ message: "User registered successfully" });
});

// LOGIN
app.post("/api/login", (req, res) => {
    const { username, password } = req.body;
    let user = users.find(u => u.username === username);
    
    if (!user && username === "demo_user") {
        users.push({ username, password });
        saveData();
        return res.send({ message: "Demo user created & logged in" });
    }
    
    if (!user || user.password !== password) {
        return res.status(401).send({ message: "Invalid credentials" });
    }
    
    res.send({ message: "Login success" });
});

// LOG USER ACTIONS (from frontend AND MITM)
app.post("/api/log-event", (req, res) => {
    const logEntry = {
        ...req.body,
        timestamp_received: Date.now()
    };
    logs.push(logEntry);
    
    // Keep only last 10000 logs
    if (logs.length > 10000) logs.shift();
    saveData();
    
    console.log(`[LOG] ${logEntry.source || 'frontend'} - ${logEntry.is_anomaly ? 'ANOMALY' : 'Normal'}`);
    res.send({ message: "Event logged" });
});

// GET ALL LOGS
app.get("/api/logs", (req, res) => {
    res.send(logs);
});

// GET LOGS WITH FILTERS
app.get("/api/logs-with-anomaly", (req, res) => {
    const anomalyLogs = logs.filter(log => log.is_anomaly === true);
    res.send({
        total: logs.length,
        anomalies: anomalyLogs.length,
        logs: logs.slice(-100)  // Last 100 logs
    });
});

// PREDICT endpoint (forwards to Python ML)
app.post("/api/predict", async (req, res) => {
    try {
        const { spawn } = require('child_process');
        const { login_hour, files_accessed, cpu_usage, network_packets } = req.body;
        
        const pythonProcess = spawn('python', [
            path.join(__dirname, '..', 'model', 'predict.py'),
            login_hour, files_accessed, cpu_usage, network_packets
        ]);
        
        let result = '';
        pythonProcess.stdout.on('data', (data) => {
            result += data.toString();
        });
        
        pythonProcess.on('close', () => {
            const isAnomaly = result.trim() === '1';
            res.json({ anomaly: isAnomaly });
        });
    } catch (error) {
        res.json({ anomaly: false, error: error.message });
    }
});

app.listen(5000, () => {
    console.log("✅ Backend running on http://localhost:5000");
    console.log("📡 MITM proxy should send logs to this endpoint");
});