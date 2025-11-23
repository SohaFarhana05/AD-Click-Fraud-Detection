import os
import joblib
import pandas as pd
import numpy as np
from sklearn.metrics import precision_score, recall_score
from features import load_clicks, engineer_features

MODELS_DIR = 'models'
REPORTS_DIR = 'reports'
os.makedirs(REPORTS_DIR, exist_ok=True)


def evaluate(model_path=None, threshold=None):
    model_path = model_path or os.path.join(MODELS_DIR, 'iso_forest.joblib')
    m = joblib.load(model_path)
    clf = m['model']
    scaler = m['scaler']
    feature_cols = m['feature_cols']

    df = load_clicks()
    df_feat, feature_cols = engineer_features(df)
    X = df_feat[feature_cols].values
    Xs = scaler.transform(X)
    preds = clf.predict(Xs)  # -1 for anomaly, 1 for normal
    df_feat['anomaly'] = (preds == -1).astype(int)

    # compute precision on labeled rows
    if 'label' in df_feat.columns:
        y = df_feat['label'].values
        y_pred = df_feat['anomaly'].values
        prec = precision_score(y, y_pred)
        rec = recall_score(y, y_pred)
    else:
        prec = None
        rec = None

    # generate simple daily trends
    summary = df_feat.groupby(df_feat['timestamp'].dt.date).agg(
        total_clicks=('clicks','sum'),
        anomalies=('anomaly','sum'),
        fraud_labels=('label','sum') if 'label' in df_feat.columns else ('ip','count')
    ).reset_index()

    trends_path = os.path.join(REPORTS_DIR, 'daily_trends.csv')
    alerts_path = os.path.join(REPORTS_DIR, 'alerts.csv')
    summary.to_csv(trends_path, index=False)
    df_feat[df_feat['anomaly'] == 1].to_csv(alerts_path, index=False)
    print(f"Precision: {prec:.3f} Recall: {rec:.3f}")
    print(f"Wrote trends to {trends_path} and alerts to {alerts_path}")
    return prec, rec


if __name__ == '__main__':
    evaluate()
