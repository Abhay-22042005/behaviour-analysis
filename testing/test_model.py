import joblib
import pandas as pd

MODEL_FEATURES = [
    "file_activity",
    "registry_activity",
    "process_thread_ratio",
    "dll_per_process",
    "path_suspicion",
    "activity_score"
]


def extract_features_from_log(file_path):

    file_create = file_read = file_write = 0
    reg_create = reg_set = 0
    process_create = thread_create = 0
    dll_load = 0
    paths = set()

    with open(file_path, "r", errors="ignore") as f:
        for line in f:
            l = line.lower()

            if "[file]" in l and "create" in l:
                file_create += 1
            if "[file]" in l and "read" in l:
                file_read += 1
            if "[file]" in l and "write" in l:
                file_write += 1

            if "[registry]" in l and "create" in l:
                reg_create += 1
            if "[registry]" in l and ("set" in l or "modify" in l):
                reg_set += 1

            if "[process]" in l:
                process_create += 1
            if "[thread]" in l:
                thread_create += 1

            if "[dll]" in l:
                dll_load += 1

            if ":" in l and "\\" in l:
                paths.add(l.strip())

    # ---- NORMALIZED BEHAVIOR FEATURES ----
    file_activity = (file_create + file_read + file_write) * 5
    registry_activity = (reg_create + reg_set) * 8

    process_thread_ratio = (thread_create + 1) / (process_create + 1)
    dll_per_process = (dll_load + 1) / (process_create + 1)

    path_suspicion = len(paths) * 6

    activity_score = (
        file_activity
        + registry_activity
        + dll_load * 10
        + thread_create * 8
    )

    features = pd.DataFrame([{
        "file_activity": file_activity,
        "registry_activity": registry_activity,
        "process_thread_ratio": process_thread_ratio,
        "dll_per_process": dll_per_process,
        "path_suspicion": path_suspicion,
        "activity_score": activity_score
    }])

    return features


def predict(log_file):

    print(f"\nAnalyzing: {log_file}")

    model = joblib.load("model/random_forest.pkl")
    scaler = joblib.load("model/scaler.pkl")

    features = extract_features_from_log(log_file)

    scaled = scaler.transform(features[MODEL_FEATURES])
    pred = model.predict(scaled)[0]

    if pred == 1:
        print("⚠ MALWARE DETECTED")
    else:
        print("✓ BENIGN FILE")


if __name__ == "__main__":
    predict("sandbox_logs/sample_malware_log.txt")
