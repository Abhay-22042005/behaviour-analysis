from feature_extraction.extract_features import load_dataset, preprocess, get_features_labels
from model.train_model import train

DATASET_PATH = "dataset/behavioral_dataset.csv"

def main():

    print("====== Malware Behavior Analysis ======")

    df = load_dataset(DATASET_PATH)

    df = preprocess(df)

    X, y = get_features_labels(df)

    train(X, y)

    print("\n[✓] Pipeline Completed Successfully")


if __name__ == "__main__":
    main()
