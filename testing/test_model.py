import re
import joblib
import numpy as np
from pathlib import Path


# ---------------------------
# Feature Extraction Engine
# ---------------------------

class SandboxFeatureExtractor:

    def __init__(self):
        self.reset()

    def reset(self):
        self.features = {
            "file_ops": 0,
            "registry_ops": 0,
            "network_ops": 0,
            "process_spawns": 0,
            "dll_loads": 0,
            "thread_events": 0,
            "hidden_files": 0,
            "suspicious_ports": 0,
            "powershell_exec": 0,
            "code_injection": 0
        }

    def parse_line(self, line: str):

        line = line.strip().lower()

        if "[file]" in line:
            self.features["file_ops"] += 1
            if "hidden" in line:
                self.features["hidden_files"] += 1

        elif "[registry]" in line:
            self.features["registry_ops"] += 1

        elif "[network]" in line:
            self.features["network_ops"] += 1
            if re.search(r":(4444|5555|8080|1337)", line):
                self.features["suspicious_ports"] += 1

        elif "[process]" in line:
            self.features["process_spawns"] += 1
            if "powershell" in line:
                self.features["powershell_exec"] += 1

        elif "[dll]" in line:
            self.features["dll_loads"] += 1

        elif "[thread]" in line:
            self.features["thread_events"] += 1
            if "inject" in line or "remote" in line:
                self.features["code_injection"] += 1

    def extract(self, file_path):

        self.reset()

        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                self.parse_line(line)

        return np.array([list(self.features.values())])


# ---------------------------
# Prediction Engine
# ---------------------------

class MalwarePredictor:

    def __init__(self):
        self.model = joblib.load("model/random_forest.pkl")
        self.scaler = joblib.load("model/scaler.pkl")
        self.extractor = SandboxFeatureExtractor()

    def predict(self, log_file):

        features = self.extractor.extract(log_file)
        scaled = self.scaler.transform(features)

        prediction = self.model.predict(scaled)[0]
        probability = self.model.predict_proba(scaled)[0][1]

        print("\n===== ANALYSIS RESULT =====")
        print(f"Log File: {log_file}")
        print(f"Malware Probability: {probability:.2f}")

        if prediction == 1:
            print("⚠ RESULT: MALWARE BEHAVIOR DETECTED")
        else:
            print("✓ RESULT: BENIGN BEHAVIOR")


# ---------------------------
# Runner
# ---------------------------

if __name__ == "__main__":

    log_path = Path("sandbox_logs/sample_malware_log.txt")

    predictor = MalwarePredictor()
    predictor.predict(log_path)
