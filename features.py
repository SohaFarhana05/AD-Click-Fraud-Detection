import pandas as pd
import numpy as np
import os
from datetime import datetime
import ipaddress
from geopy.distance import geodesic

OUT_DIR = "data"


def load_clicks(path=None):
    path = path or os.path.join(OUT_DIR, 'clicks.csv')
    return pd.read_csv(path, parse_dates=['timestamp'])


def ip_to_subnet(ip):
    try:
        parts = ip.split('.')
        return '.'.join(parts[:3])
    except Exception:
        return '0.0.0'


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # basic counts
    df['subnet'] = df['ip'].astype(str).apply(ip_to_subnet)
    df['hour'] = df['timestamp'].dt.hour

    # 1. click_rate = clicks / impressions
    df['click_rate'] = df['clicks'] / (df['impressions'].replace(0, 1))

    # 2. clicks_per_hour by ip
    df['clicks_per_ip_hour'] = df.groupby(['ip','hour'])['clicks'].transform('sum')

    # 3. clicks_per_subnet
    df['clicks_per_subnet'] = df.groupby('subnet')['clicks'].transform('sum')

    # 4. repeat_clicks_from_same_ip (count per ip)
    df['clicks_from_ip_count'] = df.groupby('ip')['clicks'].transform('count')

    # 5. distinct_user_agents_per_ip
    df['distinct_ua_per_ip'] = df.groupby('ip')['user_agent'].transform('nunique')

    # 6. device_mismatch_flag: if user_agent implies mobile but device == desktop etc.
    df['ua_mobile'] = df['user_agent'].str.contains('iPhone|Android', case=False, na=False)
    df['device_mismatch'] = ((df['ua_mobile']) & (df['device'] == 'desktop')) | ((~df['ua_mobile']) & (df['device'] == 'mobile'))
    df['device_mismatch'] = df['device_mismatch'].astype(int)

    # 7. short_interclick_interval: simulate by grouping timestamps per ip and computing min interval
    df = df.sort_values(['ip','timestamp'])
    df['prev_ts'] = df.groupby('ip')['timestamp'].shift(1)
    df['inter_click_seconds'] = (df['timestamp'] - df['prev_ts']).dt.total_seconds().fillna(999999)
    df['short_interclick'] = (df['inter_click_seconds'] < 10).astype(int)

    # 8. burst_rate: clicks in short window per ip
    df['clicks_in_1min'] = df.groupby(['ip', pd.Grouper(key='timestamp', freq='1min')])['clicks'].transform('sum')
    df['burst_rate'] = df['clicks_in_1min'] / (1 + df['impressions'])

    # 9. impossible_geo_travel: naive - same ip with different countries (VPN) OR rapid country change for same ip
    df['countries_per_ip'] = df.groupby('ip')['country'].transform('nunique')
    df['impossible_geo_travel'] = (df['countries_per_ip'] > 1).astype(int)

    # 10. subnet_repeat_count
    df['subnet_repeat_count'] = df.groupby('subnet')['ip'].transform('count')

    # 11. user_agent_entropy per ip
    def entropy(x):
        p = x.value_counts(normalize=True)
        return -(p * np.log2(p + 1e-9)).sum()

    df['ua_entropy_ip'] = df.groupby('ip')['user_agent'].transform(entropy)

    # 12. hour_of_day (cyclic features)
    df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
    df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)

    # 13. avg_clicks_per_impression per ip
    df['avg_clicks_per_impression_ip'] = df.groupby('ip')['click_rate'].transform('mean')

    # 14. duplicate_user_agent_flag if ua repeats many times in ip
    df['ua_mode_count'] = df.groupby(['ip','user_agent'])['user_agent'].transform('count')
    df['duplicate_ua_flag'] = (df['ua_mode_count'] > 2).astype(int)

    # 15. high_click_variance_in_ip
    df['clicks_std_ip'] = df.groupby('ip')['clicks'].transform('std').fillna(0)
    df['high_click_variance'] = (df['clicks_std_ip'] > 2).astype(int)

    # 16. night_activity_flag
    df['night_activity'] = df['hour'].isin([0,1,2,3,4]).astype(int)

    # 17. ip_numeric for distance calc
    def ip_to_int(ip):
        try:
            return int(ipaddress.IPv4Address(ip))
        except Exception:
            return 0
    df['ip_int'] = df['ip'].astype(str).apply(ip_to_int)

    # 18. clicks_per_minute (rolling by ip)
    df['timestamp_round_min'] = df['timestamp'].dt.floor('min')
    df['clicks_per_min'] = df.groupby(['ip','timestamp_round_min'])['clicks'].transform('sum')

    # Keep a selection of features
    feature_cols = [
        'click_rate','clicks_per_ip_hour','clicks_per_subnet','clicks_from_ip_count',
        'distinct_ua_per_ip','device_mismatch','inter_click_seconds','short_interclick','burst_rate',
        'impossible_geo_travel','subnet_repeat_count','ua_entropy_ip','hour_sin','hour_cos',
        'avg_clicks_per_impression_ip','duplicate_ua_flag','high_click_variance','night_activity',
        'ip_int','clicks_per_min'
    ]

    # fillna, infinities
    for c in feature_cols:
        if c in df.columns:
            df[c] = df[c].replace([np.inf, -np.inf], np.nan).fillna(0)

    return df, feature_cols


if __name__ == '__main__':
    df = load_clicks()
    df_feat, cols = engineer_features(df)
    os.makedirs('data', exist_ok=True)
    df_feat.to_csv('data/features.csv', index=False)
    print('Wrote features to data/features.csv')
