from flask import Flask, render_template_string
import pandas as pd
import os

app = Flask(__name__)

TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ad-Click Fraud Detection Dashboard</title>
    <style>
        :root {
            --primary-color: #2193b0;
            --secondary-color: #6dd5ed;
            --text-color: #2c3e50;
            --bg-color: #f5f6fa;
            --card-bg: #ffffff;
            --border-color: #e1e8ed;
            --shadow-light: rgba(0, 0, 0, 0.1);
        }
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        header {
            background: var(--card-bg);
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px var(--shadow-light);
            margin-bottom: 30px;
            text-align: center;
        }
        h1 {
            font-size: 2.5em;
            background: linear-gradient(45deg, var(--primary-color), var(--secondary-color));
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
            font-weight: bold;
        }
        .subtitle {
            color: var(--text-color);
            font-size: 1.1em;
            margin-bottom: 20px;
        }
        .metrics {
            display: flex;
            gap: 20px;
            justify-content: center;
            flex-wrap: wrap;
            margin-top: 20px;
        }
        .metric-card {
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
            color: white;
            padding: 20px 30px;
            border-radius: 10px;
            box-shadow: 0 5px 15px var(--shadow-light);
            min-width: 200px;
            text-align: center;
            transition: transform 0.3s ease;
        }
        .metric-card:hover {
            transform: translateY(-5px);
        }
        .metric-value {
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 5px;
        }
        .metric-label {
            font-size: 0.9em;
            opacity: 0.9;
        }
        .section {
            background: var(--card-bg);
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px var(--shadow-light);
            margin-bottom: 30px;
        }
        h2 {
            color: var(--primary-color);
            font-size: 1.8em;
            margin-bottom: 20px;
            border-bottom: 3px solid var(--primary-color);
            padding-bottom: 10px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }
        th {
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }
        td {
            padding: 12px 15px;
            border-bottom: 1px solid var(--border-color);
            color: var(--text-color);
        }
        tr:hover {
            background: var(--bg-color);
        }
        .status-fraud {
            color: #e74c3c;
            font-weight: bold;
        }
        .status-normal {
            color: #27ae60;
            font-weight: bold;
        }
        .footer {
            text-align: center;
            color: white;
            padding: 20px;
            font-size: 0.9em;
            opacity: 0.95;
            text-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }
        .no-data {
            text-align: center;
            padding: 40px;
            color: #999;
            font-style: italic;
        }
        .alert-high {
            background: #ffe5e5;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🛡️ Ad-Click Fraud Detection Dashboard</h1>
            <p class="subtitle">Real-time monitoring of fraudulent click patterns using ML-based anomaly detection</p>
            <div class="metrics">
                <div class="metric-card">
                    <div class="metric-value">{{ precision }}</div>
                    <div class="metric-label">Precision</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{{ recall }}</div>
                    <div class="metric-label">Recall</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{{ total_alerts }}</div>
                    <div class="metric-label">Total Alerts</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{{ total_clicks }}</div>
                    <div class="metric-label">Total Clicks</div>
                </div>
            </div>
        </header>

        <div class="section">
            <h2>📊 Daily Trends</h2>
            {% if trends_html %}
                {{ trends_html|safe }}
            {% else %}
                <div class="no-data">No trend data available. Run the pipeline first.</div>
            {% endif %}
        </div>

        <div class="section">
            <h2>🚨 Top 20 Fraud Alerts</h2>
            {% if alerts_html %}
                {{ alerts_html|safe }}
            {% else %}
                <div class="no-data">No alerts available. Run the pipeline first.</div>
            {% endif %}
        </div>

        <div class="footer">
            Made with ❤️ by Soha | Powered by Flask, Scikit-learn & Isolation Forest
        </div>
    </div>
</body>
</html>
"""


@app.route('/')
def index():
    precision = "N/A"
    recall = "N/A"
    total_alerts = 0
    total_clicks = 0
    trends_html = None
    alerts_html = None
    
    # Load trends
    if os.path.exists('reports/daily_trends.csv'):
        try:
            df_trends = pd.read_csv('reports/daily_trends.csv')
            total_clicks = df_trends['total_clicks'].sum()
            total_alerts = df_trends['anomalies'].sum()
            trends_html = df_trends.to_html(index=False, classes='', border=0)
        except Exception as e:
            trends_html = f'<div class="no-data">Error loading trends: {e}</div>'
    
    # Load alerts
    if os.path.exists('reports/alerts.csv'):
        try:
            df_alerts = pd.read_csv('reports/alerts.csv')
            # Select key columns for display
            display_cols = ['ip', 'timestamp', 'device', 'country', 'clicks', 'click_rate', 'clicks_per_ip_hour']
            available_cols = [col for col in display_cols if col in df_alerts.columns]
            df_display = df_alerts[available_cols].head(20)
            alerts_html = df_display.to_html(index=False, classes='', border=0)
            
            # Calculate precision/recall from labels if available
            if 'label' in df_alerts.columns and 'anomaly' in df_alerts.columns:
                from sklearn.metrics import precision_score, recall_score
                y_true = df_alerts['label'].values
                y_pred = df_alerts['anomaly'].values
                precision = f"{precision_score(y_true, y_pred):.1%}"
                recall = f"{recall_score(y_true, y_pred):.1%}"
        except Exception as e:
            alerts_html = f'<div class="no-data">Error loading alerts: {e}</div>'
    
    return render_template_string(
        TEMPLATE,
        precision=precision,
        recall=recall,
        total_alerts=total_alerts,
        total_clicks=total_clicks,
        trends_html=trends_html,
        alerts_html=alerts_html
    )


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Ad-Click Fraud Detection Dashboard")
    print("="*60)
    print("📊 Dashboard running at: http://127.0.0.1:5000")
    print("💡 Press Ctrl+C to stop the server")
    print("="*60 + "\n")
    app.run(host='0.0.0.0', port=5000, debug=True)
