# 💳 UPI Pulse — Payments Intelligence Dashboard

<div align="center">

![Power BI](https://img.shields.io/badge/Power%20BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![DAX](https://img.shields.io/badge/DAX-FF6B00?style=for-the-badge&logo=microsoft&logoColor=white)

**An executive-grade Power BI analytics dashboard analyzing 50,000+ UPI transactions across India — uncovering payment patterns, fraud signals, and ₹7.5 Cr in transaction intelligence.**

[📊 View Dashboard](#dashboard-preview) · [📖 Read Insights](insights/key_findings.md) · [🔧 Setup Guide](powerbi/POWERBI_SETUP_GUIDE.md)

</div>

---

## 🎯 Project Overview

This project replicates the kind of payments analytics work done at **Razorpay, PhonePe, CRED, and Paytm** — taking raw UPI transaction data and transforming it into executive-ready intelligence that drives product decisions.

> *"Analyzed 50,000 synthetic UPI transactions to surface peak payment windows, merchant revenue patterns, city-tier spending gaps, and fraud anomalies — built a 5-page Power BI dashboard with 30+ DAX measures and What-If revenue simulation."*

---

## 📊 Dashboard Preview

> **All 5 pages shown below — open `powerbi/UPI_Pulse.pbix` to interact live**

### 01. Executive Overview
![Executive Overview](screenshots/01_Executive_Overview.png)
*High-level KPIs, app market share, and monthly volume trends.*

### 02. Time Intelligence
![Time Intelligence](screenshots/02_Time_Intelligence.png)
*Deep dive into peak payment hours (8-11 PM), transaction heatmaps, and MoM growth patterns.*

### 03. Geo Analysis
![Geo Analysis](screenshots/03_Geo_Analysis.png)
*State-wise transaction volume via filled maps and Tier 1 vs Tier 2 city intelligence.*

### 04. Merchant Analytics
![Merchant Analytics](screenshots/04_Merchant_Analytics.png)
*Category-wise spending patterns (Food, Grocery, Travel), success rates, and merchant bank distribution.*

### 05. Fraud & Anomaly Signals
![Fraud & Anomaly](screenshots/05_Fraud_Anomaly.png)
*AI-driven anomaly detection, failure reason analysis (Insufficient Balance vs. Bank Down), and fraud risk monitoring.*


---

## 📦 Dataset

| Attribute | Value |
|-----------|-------|
| Rows | 50,000 transactions |
| Columns | 28 features |
| Date Range | Jan 2024 – Dec 2024 |
| States | 13 Indian states |
| Payment Apps | PhonePe, Google Pay, Paytm, CRED, Amazon Pay, WhatsApp Pay |
| Total Volume | ₹7.46 Cr (~₹74.6 million) |

### Key Columns

```
transaction_id    Unique ID per transaction
timestamp         Full datetime (YYYY-MM-DD HH:MM:SS)
payment_app       PhonePe / Google Pay / Paytm / CRED / etc.
merchant_category Food & Dining / Groceries / Travel / etc.
amount_inr        Transaction amount in Indian Rupees
status            Success / Failed / Pending
state             Indian state name
city_tier         Tier 1 / Tier 2
is_repeat_user    1 if returning user, 0 if new
fraud_flag        1 if suspicious pattern detected
failure_reason    Reason for failure (if status = Failed)
```

> 📁 Dataset is **synthetically generated** using realistic distributions matching NPCI's published UPI statistics.

---

## 🏗️ Project Structure

```
UPI-Pulse-Dashboard/
│
├── 📁 data/
│   ├── generate_data.py        ← Python script to generate dataset
│   ├── eda_analysis.py         ← EDA + summary statistics
│   ├── upi_transactions.csv    ← Main dataset (50,000 rows)
│   ├── summary_by_app.csv      ← App-level aggregates
│   ├── summary_by_category.csv ← Category-level aggregates
│   ├── summary_by_state.csv    ← State-level aggregates
│   └── summary_monthly.csv     ← Monthly trend data
│
├── 📁 powerbi/
│   ├── UPI_Pulse.pbix          ← Power BI dashboard file
│   └── POWERBI_SETUP_GUIDE.md  ← Step-by-step build instructions
│
├── 📁 dax_measures/
│   └── all_measures.dax        ← All 30+ DAX measures (copy-paste ready)
│
├── 📁 insights/
│   └── key_findings.md         ← 10 business insights with recommendations
│
├── 📁 screenshots/
│   └── *.png                   ← Dashboard page screenshots
│
├── requirements.txt
└── README.md
```

---

## 🚀 Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/UPI-Pulse-Dashboard.git
cd UPI-Pulse-Dashboard
```

### 2. Generate the dataset
```bash
pip install -r requirements.txt
cd data
python generate_data.py
```

### 3. Open in Power BI
- Open `powerbi/UPI_Pulse.pbix` in Power BI Desktop
- Or follow the [full setup guide](powerbi/POWERBI_SETUP_GUIDE.md) to build it from scratch

---

## 📐 DAX Highlights

30+ custom DAX measures built from scratch:

```dax
-- Month-over-Month Volume Change
Volume MoM % Change = 
    VAR CurrentMonth = [Total Volume (₹)]
    VAR PrevMonth = CALCULATE(SUM(upi_transactions[amount_inr]), DATEADD(upi_transactions[date], -1, MONTH))
    RETURN DIVIDE(CurrentMonth - PrevMonth, PrevMonth, 0) * 100

-- What-If: Revenue Recovery Simulation
Projected Volume Gain = 
    VAR CurrentFailedVolume = CALCULATE(SUM(upi_transactions[amount_inr]), upi_transactions[status] = "Failed")
    VAR ImprovementFactor = 'Success Rate Improvement'[Success Rate Improvement Value] / 100
    RETURN CurrentFailedVolume * ImprovementFactor
```

📄 *See all measures in [`dax_measures/all_measures.dax`](dax_measures/all_measures.dax)*

---

## 🔍 Key Findings

| # | Insight | Impact |
|---|---------|--------|
| 1 | PhonePe holds **48% market share** but success rates are equal across all apps | Acquisition > reliability differentiates apps |
| 2 | **Utility Bills** has worst success rate (89.6%) — 3pp below average | High-priority reliability fix |
| 3 | **Feature Phone** users fail 5% more often than smartphone users | 150M+ users underserved |
| 4 | **Tier 2 cities** have *higher* avg ticket (₹1,498) than Tier 1 (₹1,488) | Tier 2 expansion is underrated |
| 5 | Education & EMI: 2,454 txns but ₹1.23 Cr volume (avg ₹5,022) | Highest-value category per transaction |

📄 *Full analysis in [`insights/key_findings.md`](insights/key_findings.md)*

---

## ⚙️ Advanced Power BI Features Used

| Feature | Where Used |
|---------|------------|
| **Time Intelligence DAX** | MoM%, YoY%, Rolling 7-day, DATESYTD |
| **What-If Parameter** | Revenue recovery simulator (Page 1 + 5) |
| **Anomaly Detection** | Built-in anomaly detection on time series (Page 5) |
| **Row Level Security** | App-wise access control (PhonePe_Analyst role) |
| **Drillthrough Pages** | State → City level drillthrough |
| **Dynamic Titles** | DAX-driven titles that change with slicer selection |
| **Conditional Formatting** | Heatmap matrix, red/green KPI cards |
| **Bookmarks** | Toggle between table/chart views |

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| **Python 3.11** | Dataset generation, EDA |
| **Pandas + NumPy** | Data manipulation |
| **Power BI Desktop** | Dashboard building |
| **DAX** | Calculated measures & time intelligence |
| **Power Query (M)** | Data transformation |
| **Power BI Service** | Publishing & sharing |

---

## 💼 Business Context

This dashboard is designed to answer the questions a **Data Analyst at Razorpay / CRED / PhonePe** would answer daily:

- Which payment app is losing ground this month?
- Which merchant categories are driving high-value transactions?
- Where are we losing revenue to failed transactions?
- Which states should we double down on for expansion?
- Are there fraud patterns we're missing?

---

## 📬 Contact

**Nilesh Sahoo** — Data Analyst | AI/ML Engineer  
📧 nileshsahoo837@gmail.com  


---

<div align="center">
⭐ Star this repo if you found it useful!
</div>
