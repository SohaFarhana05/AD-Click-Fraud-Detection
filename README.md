# 🛡️ Ad-Click Fraud Detection System

**An ML-powered system to detect fraudulent ad-click patterns using anomaly detection**

Built by **Soha** | Powered by Python, Scikit-learn & Flask

---

## 🎯 Overview

This project detects click-farm and bot abuse patterns in ad-click logs using machine learning. It simulates real-world ad-click data, engineers 18+ fraud signals, and trains an Isolation Forest model to identify suspicious behavior with **91.6% precision** and **97.7% recall**.

### ✨ Key Features

- 📊 **10,000+ simulated ad-click logs** with realistic fraud patterns
- 🔍 **18+ engineered fraud signals** (click-burst rate, device mismatch, geo-travel, subnet analysis, etc.)
- 🤖 **ML-based anomaly detection** using Isolation Forest algorithm
- 📈 **Automated daily reports** and fraud alert generation
- 🌐 **Beautiful Flask dashboard** for real-time monitoring
- 🎯 **High accuracy**: 91.6% precision, 97.7% recall

---

## 🚀 Quick Start

### 1️⃣ Setup Environment

```bash
# Clone or navigate to project directory
cd Project

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # On macOS/Linux
# .venv\Scripts\activate   # On Windows

# Install dependencies
pip install -r requirements.txt
```

### 2️⃣ Run the Pipeline

```bash
# Run complete fraud detection pipeline
python run_pipeline.py
```

This will:
- Generate synthetic ad-click data
- Engineer 18+ fraud signals
- Train the ML model
- Evaluate performance
- Generate reports in `reports/` folder

### 3️⃣ Launch Dashboard

```bash
# Start Flask web dashboard
python app.py
```

Then open your browser to: **http://localhost:5000**

---

## 📁 Project Structure

```
Project/
├── simulate_data.py       # Generates synthetic click logs (10K+ records)
├── features.py            # Engineers 18+ fraud detection signals
├── train_model.py         # Trains Isolation Forest ML model
├── evaluate.py            # Evaluates model & generates reports
├── run_pipeline.py        # Orchestrates end-to-end pipeline
├── app.py                 # Flask dashboard for visualization
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── PROJECT_SUMMARY.md     # Detailed project summary
├── data/
│   ├── clicks.csv         # Raw simulated click logs
│   └── features.csv       # Engineered features (18+ signals)
├── models/
│   └── iso_forest.joblib  # Trained model + scaler
└── reports/
    ├── daily_trends.csv   # Daily aggregated statistics
    └── alerts.csv         # Flagged fraudulent clicks
```

---

## 🔍 Fraud Signals Engineered (18+)

The system detects fraud through multiple behavioral signals:

1. **Click-burst rate** - Abnormal click frequency in short time windows
2. **Abnormal CTR** - Click-through rate exceeds normal thresholds
3. **Device mismatch** - User-agent doesn't match device type
4. **Impossible geo-travel** - Same IP from multiple countries
5. **Repeated clicks from subnet** - High activity from IP ranges
6. **Inter-click interval** - Time between clicks too short/regular
7. **Night activity patterns** - Unusual activity during off-hours
8. **User-agent entropy** - Suspicious user-agent patterns per IP
9. **Subnet repeat count** - Multiple IPs from same subnet
10. **High click variance** - Inconsistent click patterns
11. **Duplicate user-agent flags** - Same UA repeated excessively
12. **Clicks per impression ratio** - Unrealistic conversion rates
13. **Hour-of-day patterns** - Temporal anomalies (cyclic features)
14. **Clicks per minute** - Rapid-fire clicking behavior
15. **Distinct UA per IP** - Multiple user-agents from one IP
16. **Clicks from IP count** - Total activity per IP address
17. **Clicks per subnet** - Aggregate subnet-level activity
18. **Short interclick flags** - Sub-10-second click intervals

---

## 📊 Performance Metrics

| Metric | Value |
|--------|-------|
| **Precision** | 91.6% |
| **Recall** | 97.7% |
| **Dataset Size** | 10,000+ clicks |
| **Fraud Signals** | 18+ features |
| **Model** | Isolation Forest |
| **Training Time** | < 5 seconds |

---

## 🛠️ Technologies Used

- **Python 3.13+**
- **Pandas** - Data manipulation
- **NumPy** - Numerical computing
- **Scikit-learn** - Machine learning (Isolation Forest)
- **Flask** - Web dashboard
- **Joblib** - Model serialization
- **Geopy** - Geo-location analysis

---

## 📈 Dashboard Preview

The Flask dashboard displays:
- 📊 Real-time metrics (precision, recall, total alerts)
- 📅 Daily trend analysis
- 🚨 Top 20 fraud alerts with key attributes
- 🎨 Beautiful, responsive UI

---

## 🎓 Resume-Ready Highlights

Perfect for showcasing on your resume/portfolio:

✅ **End-to-end ML pipeline** (data simulation → feature engineering → training → evaluation)  
✅ **Advanced feature engineering** (18+ fraud signals)  
✅ **High-precision anomaly detection** (91.6% precision, 97.7% recall)  
✅ **Production-ready code** with modular structure  
✅ **Automated reporting** and real-time monitoring  
✅ **Web dashboard** for visualization

---

## 📝 How It Works

1. **Data Simulation**: Generate realistic ad-click logs with fraud patterns (click-farms, bots, VPN abuse)
2. **Feature Engineering**: Compute 18+ statistical and behavioral fraud signals
3. **Model Training**: Train Isolation Forest to detect anomalies in feature space
4. **Evaluation**: Measure precision/recall and generate reports
5. **Monitoring**: View results in Flask dashboard

---

## 🔮 Future Enhancements

- [ ] Real-time streaming data ingestion
- [ ] Deep learning models (Autoencoders, LSTMs)
- [ ] Integration with Google Ads API
- [ ] A/B testing framework for model comparison
- [ ] Docker containerization
- [ ] CI/CD pipeline with automated testing

---

## 👤 Author

**Made with ❤️ by Soha**

This project demonstrates expertise in:
- Machine Learning & Anomaly Detection
- Feature Engineering
- Python Development
- Data Analysis & Visualization
- Web Development (Flask)

---

## 📄 License

This project is for educational and portfolio purposes.

---

## 🤝 Contributing

Feel free to fork, modify, and use this project for learning or portfolio purposes!

---

**Status**: ✅ Complete and tested  
**Last Updated**: November 2025  
**Performance**: 91.6% precision, 97.7% recall
