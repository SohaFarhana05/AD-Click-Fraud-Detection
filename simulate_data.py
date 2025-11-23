import random
import csv
from datetime import datetime, timedelta
import ipaddress
import math
import os
import numpy as np
import pandas as pd

random.seed(42)
np.random.seed(42)

OUT_DIR = "data"
os.makedirs(OUT_DIR, exist_ok=True)

COUNTRIES = ["US","IN","CN","GB","DE","BR","NG","RU","CA","AU"]
DEVICES = ["mobile","desktop","tablet"]
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)",
    "Mozilla/5.0 (Linux; Android 10)"
]


def random_ip():
    return str(ipaddress.IPv4Address(random.getrandbits(32)))


def random_subnet(ip):
    parts = ip.split('.')
    return '.'.join(parts[:3]) + '.0/24'


def simulate(n=10000, fraud_ratio=0.05, out_csv=None):
    rows = []
    start = datetime.utcnow() - timedelta(days=1)
    fraud_count = int(n * fraud_ratio)
    legit_count = n - fraud_count

    # Generate legit traffic
    for i in range(legit_count):
        ip = random_ip()
        ts = start + timedelta(seconds=random.randint(0, 86400))
        device = random.choices(DEVICES, weights=[0.6,0.3,0.1])[0]
        ua = random.choice(USER_AGENTS)
        country = random.choices(COUNTRIES, weights=[0.3,0.1,0.15,0.1,0.1,0.05,0.03,0.04,0.07,0.06])[0]
        impressions = random.randint(1,10)
        clicks = 1 if random.random() < 0.3 else 0
        # legit mostly single clicks
        rows.append({
            'ip': ip,
            'timestamp': ts.isoformat(),
            'device': device,
            'user_agent': ua,
            'country': country,
            'impressions': impressions,
            'clicks': clicks,
            'label': 0
        })

    # Generate fraud clusters: click farms and bots
    for i in range(fraud_count):
        # Create clusters with repeated IPs, short intervals, impossible geo travel, high clicks
        cluster = random.choice(['farm','bot','vpn'])
        if cluster == 'farm':
            base_ip = random_ip()
            # many clicks from same subnet
            for k in range(random.randint(3,10)):
                ip = base_ip
                ts = start + timedelta(seconds=random.randint(0, 86400))
                device = random.choice(['mobile','desktop'])
                ua = random.choice(USER_AGENTS)
                country = random.choice(COUNTRIES)
                impressions = random.randint(1,3)
                clicks = random.randint(1,5)
                rows.append({
                    'ip': ip,
                    'timestamp': ts.isoformat(),
                    'device': device,
                    'user_agent': ua,
                    'country': country,
                    'impressions': impressions,
                    'clicks': clicks,
                    'label': 1
                })
        elif cluster == 'bot':
            ip = random_ip()
            for k in range(random.randint(1,5)):
                ts = start + timedelta(seconds=random.randint(0, 86400))
                device = 'desktop'
                ua = 'bot-crawler/1.0'
                country = random.choice(COUNTRIES)
                impressions = random.randint(1,2)
                clicks = random.randint(1,10)
                rows.append({
                    'ip': ip,
                    'timestamp': ts.isoformat(),
                    'device': device,
                    'user_agent': ua,
                    'country': country,
                    'impressions': impressions,
                    'clicks': clicks,
                    'label': 1
                })
        else:  # vpn/geo mismatch
            ip = random_ip()
            ts = start + timedelta(seconds=random.randint(0, 86400))
            device = random.choice(DEVICES)
            ua = random.choice(USER_AGENTS)
            country = random.choice(COUNTRIES)
            # simulate impossible travel by pairing close timestamps with far countries later in stream
            impressions = random.randint(1,3)
            clicks = random.randint(1,4)
            rows.append({
                'ip': ip,
                'timestamp': ts.isoformat(),
                'device': device,
                'user_agent': ua,
                'country': country,
                'impressions': impressions,
                'clicks': clicks,
                'label': 1
            })

    df = pd.DataFrame(rows)
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    out_csv = out_csv or os.path.join(OUT_DIR, 'clicks.csv')
    df.to_csv(out_csv, index=False)
    print(f"Wrote {len(df)} rows to {out_csv}")
    return df


if __name__ == '__main__':
    simulate(n=10000, fraud_ratio=0.06)
