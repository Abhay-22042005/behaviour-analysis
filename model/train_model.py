import os
import joblib
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier


def train(X, y):

    print("[+] Splitting dataset")

    # VERY IMPORTANT: stratify keeps both classes in train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    print("[+] Scaling features")
    scaler = StandardScaler()

    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    print("[+] Training RandomForest")
    rf = RandomForestClassifier(
        n_estimators=200,
        max_depth=12,
        class_weight="balanced",
        random_state=42
    )

    rf.fit(X_train, y_train)

    print("[+] Training GradientBoost")
    gb = GradientBoostingClassifier(
        n_estimators=150,
        learning_rate=0.08,
        max_depth=3
    )

    gb.fit(X_train, y_train)

    print("[+] Evaluating models")

    rf_pred = rf.predict(X_test)
    gb_pred = gb.predict(X_test)

    print("\n===== RANDOM FOREST RESULTS =====")
    print("Accuracy:", accuracy_score(y_test, rf_pred))
    print(classification_report(y_test, rf_pred))

    print("\n===== GRADIENT BOOST RESULTS =====")
    print("Accuracy:", accuracy_score(y_test, gb_pred))
    print(classification_report(y_test, gb_pred))

    # Choose best model automatically
    rf_acc = accuracy_score(y_test, rf_pred)
    gb_acc = accuracy_score(y_test, gb_pred)

    if rf_acc >= gb_acc:
        best_model = rf
        print("\n✔ Selected Model: RandomForest")
        model_name = "random_forest.pkl"
    else:
        best_model = gb
        print("\n✔ Selected Model: GradientBoost")
        model_name = "gradient_boost.pkl"

    # Save model
    os.makedirs("model", exist_ok=True)
    joblib.dump(best_model, f"model/{model_name}")
    joblib.dump(scaler, "model/scaler.pkl")

    print(f"\nModel saved: model/{model_name}")
    print("Scaler saved: model/scaler.pkl")

    return best_model
