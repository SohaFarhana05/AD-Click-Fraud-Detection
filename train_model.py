import os
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from features import load_clicks, engineer_features

MODELS_DIR = 'models'
os.makedirs(MODELS_DIR, exist_ok=True)


def train_and_save(out_model_path=None, contamination=0.05, random_state=42):
    df = load_clicks()
    df_feat, feature_cols = engineer_features(df)
    X = df_feat[feature_cols].values
    scaler = StandardScaler()
    Xs = scaler.fit_transform(X)

    # Train Isolation Forest
    clf = IsolationForest(contamination=contamination, random_state=random_state)
    clf.fit(Xs)

    out_model_path = out_model_path or os.path.join(MODELS_DIR, 'iso_forest.joblib')
    joblib.dump({'model': clf, 'scaler': scaler, 'feature_cols': feature_cols}, out_model_path)
    print(f"Saved model to {out_model_path}")
    return clf, scaler, feature_cols


if __name__ == '__main__':
    train_and_save()
