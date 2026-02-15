import pandas as pd

def load_dataset(path):
    df = pd.read_csv(path)
    print("Dataset Loaded Successfully")
    print("Total Samples:", len(df))
    return df


# ---------------- FEATURE ENGINEERING ----------------
def behavioral_features(df):

    # File activity intensity
    df['file_activity'] = df['file_create'] + df['file_read'] + df['file_write']

    # Registry persistence behavior
    df['registry_activity'] = df['reg_create'] + df['reg_set']

    # Process injection suspicion
    df['process_thread_ratio'] = df['thread_create'] / (df['process_create'] + 1)

    # DLL abuse indicator
    df['dll_per_process'] = df['dll_load'] / (df['process_create'] + 1)

    # System spread behaviour
    df['path_suspicion'] = df['unique_paths'] / (df['file_create'] + 1)

    # Overall activity score
    df['activity_score'] = (
        df['file_activity'] +
        df['registry_activity'] +
        df['process_create'] +
        df['thread_create'] +
        df['dll_load']
    )

    return df


def preprocess(df):
    df = behavioral_features(df)

    # Convert label
    df['label'] = df['label'].map({'benign':0, 'malware':1})

    df = df.fillna(0)
    return df


def get_features_labels(df):

    features = [
        'file_activity',
        'registry_activity',
        'process_thread_ratio',
        'dll_per_process',
        'path_suspicion',
        'activity_score'
    ]

    X = df[features]
    y = df['label']

    return X, y
