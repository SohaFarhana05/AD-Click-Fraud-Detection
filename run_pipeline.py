import os
from simulate_data import simulate
from features import engineer_features, load_clicks
from train_model import train_and_save
from evaluate import evaluate

os.makedirs('data', exist_ok=True)
os.makedirs('models', exist_ok=True)
os.makedirs('reports', exist_ok=True)


def run_all():
    print('Simulating data...')
    simulate(n=10000, fraud_ratio=0.06)
    print('Engineering features...')
    df = load_clicks()
    df_feat, cols = engineer_features(df)
    df_feat.to_csv('data/features.csv', index=False)
    print('Training model...')
    train_and_save(contamination=0.19)
    print('Evaluating...')
    prec, rec = evaluate()
    print(f'Done. Precision: {prec:.1%} Recall: {rec:.1%}')


if __name__ == '__main__':
    run_all()
