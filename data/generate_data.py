"""
UPI Pulse - Transaction Data Generator
Generates 50,000 realistic synthetic UPI transactions
Run: python generate_data.py
Output: upi_transactions.csv
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

# ─── Seed for reproducibility ───────────────────────────────────────────────
np.random.seed(42)
random.seed(42)

# ─── Configuration ────────────────────────────────────────────────────────────
N = 50000
START_DATE = datetime(2024, 1, 1)
END_DATE   = datetime(2024, 12, 31)

# ─── Reference Data ───────────────────────────────────────────────────────────
STATES = {
    "Maharashtra":    {"tier1": ["Mumbai", "Pune"],           "tier2": ["Nagpur", "Nashik", "Aurangabad"],    "weight": 0.18},
    "Karnataka":      {"tier1": ["Bengaluru"],                "tier2": ["Mysuru", "Hubli", "Mangaluru"],      "weight": 0.12},
    "Delhi":          {"tier1": ["New Delhi", "Gurugram"],    "tier2": ["Noida", "Faridabad"],                "weight": 0.11},
    "Tamil Nadu":     {"tier1": ["Chennai"],                  "tier2": ["Coimbatore", "Madurai", "Salem"],    "weight": 0.09},
    "Telangana":      {"tier1": ["Hyderabad"],                "tier2": ["Warangal", "Karimnagar"],            "weight": 0.08},
    "Gujarat":        {"tier1": ["Ahmedabad", "Surat"],       "tier2": ["Vadodara", "Rajkot", "Gandhinagar"], "weight": 0.07},
    "Rajasthan":      {"tier1": ["Jaipur"],                   "tier2": ["Jodhpur", "Udaipur", "Kota"],        "weight": 0.06},
    "West Bengal":    {"tier1": ["Kolkata"],                  "tier2": ["Siliguri", "Howrah", "Durgapur"],    "weight": 0.06},
    "Uttar Pradesh":  {"tier1": ["Lucknow", "Kanpur"],        "tier2": ["Agra", "Varanasi", "Prayagraj"],     "weight": 0.07},
    "Punjab":         {"tier1": ["Chandigarh"],               "tier2": ["Ludhiana", "Amritsar", "Jalandhar"], "weight": 0.04},
    "Madhya Pradesh": {"tier1": ["Indore", "Bhopal"],         "tier2": ["Gwalior", "Jabalpur"],               "weight": 0.04},
    "Kerala":         {"tier1": ["Kochi", "Thiruvananthapuram"], "tier2": ["Kozhikode", "Thrissur"],          "weight": 0.04},
    "Haryana":        {"tier1": ["Faridabad", "Gurugram"],    "tier2": ["Ambala", "Hisar", "Karnal"],         "weight": 0.04},
}

PAYMENT_APPS = {
    "PhonePe":   0.48,
    "Google Pay": 0.35,
    "Paytm":     0.09,
    "CRED":      0.04,
    "Amazon Pay": 0.02,
    "WhatsApp Pay": 0.02,
}

MERCHANT_CATEGORIES = {
    "Food & Dining":       {"weight": 0.22, "avg_amt": 350,  "std": 200},
    "Groceries":           {"weight": 0.18, "avg_amt": 800,  "std": 500},
    "Shopping & Fashion":  {"weight": 0.12, "avg_amt": 1200, "std": 800},
    "Utility Bills":       {"weight": 0.10, "avg_amt": 1500, "std": 600},
    "Entertainment":       {"weight": 0.08, "avg_amt": 500,  "std": 300},
    "Travel & Transport":  {"weight": 0.08, "avg_amt": 2000, "std": 1500},
    "Healthcare":          {"weight": 0.06, "avg_amt": 1800, "std": 1200},
    "Education":           {"weight": 0.05, "avg_amt": 5000, "std": 3000},
    "Fuel":                {"weight": 0.05, "avg_amt": 2200, "std": 500},
    "P2P Transfer":        {"weight": 0.04, "avg_amt": 3000, "std": 2000},
    "Investments & EMI":   {"weight": 0.02, "avg_amt": 8000, "std": 5000},
}

DEVICE_TYPES = {"Android": 0.72, "iOS": 0.24, "Feature Phone": 0.04}

TRANSACTION_TYPES = {"Merchant Payment": 0.65, "P2P Transfer": 0.25, "Bill Payment": 0.10}

# Indian festivals (2024) — spike days
FESTIVAL_DAYS = [
    "2024-01-14",  # Makar Sankranti
    "2024-01-22",  # Ram Mandir
    "2024-03-25",  # Holi
    "2024-04-14",  # Baisakhi
    "2024-08-15",  # Independence Day
    "2024-10-02",  # Gandhi Jayanti
    "2024-10-12",  # Navratri start
    "2024-11-01",  # Diwali
    "2024-11-02",  # Diwali +1
    "2024-11-15",  # Children's Day
    "2024-12-25",  # Christmas
    "2024-12-31",  # New Year's Eve
]
festival_set = set(FESTIVAL_DAYS)

# ─── Helper Functions ─────────────────────────────────────────────────────────

def weighted_choice(d):
    keys = list(d.keys())
    weights = list(d.values())
    return random.choices(keys, weights=weights, k=1)[0]

def generate_upi_id(app):
    domains = {
        "PhonePe": "ybl",
        "Google Pay": "okaxis",
        "Paytm": "paytm",
        "CRED": "axisbank",
        "Amazon Pay": "apl",
        "WhatsApp Pay": "waaxis",
    }
    name = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=6))
    digits = ''.join(random.choices('0123456789', k=4))
    return f"{name}{digits}@{domains[app]}"

def generate_timestamp(start, end):
    delta = end - start
    random_seconds = random.randint(0, int(delta.total_seconds()))
    ts = start + timedelta(seconds=random_seconds)
    
    # Weight towards peak hours (9am-11am, 12pm-2pm, 7pm-10pm)
    hour = ts.hour
    if hour in range(9, 12) or hour in range(12, 14) or hour in range(19, 23):
        # 2x more transactions in peak hours — resample with 50% chance
        if random.random() < 0.5:
            ts = start + timedelta(seconds=random.randint(0, int(delta.total_seconds())))
    return ts

def get_status(category, app, amount):
    base_fail_rate = 0.05  # 5% base failure
    if amount > 50000:
        base_fail_rate += 0.08
    if app == "Feature Phone":
        base_fail_rate += 0.05
    if category == "Utility Bills":
        base_fail_rate += 0.03
    
    r = random.random()
    if r < base_fail_rate:
        return "Failed"
    elif r < base_fail_rate + 0.02:
        return "Pending"
    else:
        return "Success"

def get_amount(category):
    info = MERCHANT_CATEGORIES[category]
    amt = np.random.normal(info["avg_amt"], info["std"])
    amt = max(1, round(amt, 2))
    # Round to realistic UPI amounts
    if amt < 100:
        amt = round(amt / 5) * 5
    elif amt < 1000:
        amt = round(amt / 10) * 10
    else:
        amt = round(amt / 100) * 100
    return max(1, amt)

def is_festival(ts):
    return ts.strftime("%Y-%m-%d") in festival_set

def get_cashback(app, amount, category):
    if app == "CRED" and amount > 500:
        return round(amount * random.uniform(0.01, 0.05), 2)
    if app == "Google Pay" and random.random() < 0.15:
        return round(random.uniform(1, 50), 2)
    if app == "PhonePe" and category == "Groceries" and random.random() < 0.1:
        return round(random.uniform(5, 100), 2)
    return 0.0

# ─── Main Generation ──────────────────────────────────────────────────────────

print("🚀 Generating 50,000 UPI transactions...")

records = []
user_pool = [generate_upi_id(random.choice(list(PAYMENT_APPS.keys()))) for _ in range(8000)]
merchant_pool = {
    cat: [f"merchant_{cat[:4].lower()}_{i:04d}@upi" for i in range(200)]
    for cat in MERCHANT_CATEGORIES
}

for i in range(N):
    # Timestamp
    ts = generate_timestamp(START_DATE, END_DATE)
    
    # Location
    state = weighted_choice({s: v["weight"] for s, v in STATES.items()})
    state_info = STATES[state]
    city_tier = random.choices(["Tier 1", "Tier 2"], weights=[0.6, 0.4])[0]
    city_pool = state_info["tier1"] if city_tier == "Tier 1" else state_info["tier2"]
    city = random.choice(city_pool)
    
    # Payment
    app = weighted_choice(PAYMENT_APPS)
    category = weighted_choice({c: v["weight"] for c, v in MERCHANT_CATEGORIES.items()})
    txn_type = weighted_choice(TRANSACTION_TYPES)
    amount = get_amount(category)
    device = weighted_choice(DEVICE_TYPES)
    status = get_status(category, device, amount)
    
    # Users
    sender = random.choice(user_pool)
    if txn_type == "P2P Transfer":
        receiver = random.choice(user_pool)
    else:
        receiver = random.choice(merchant_pool[category])
    
    # Enrichment
    is_repeat = random.random() < 0.45
    is_new_user = random.random() < 0.08
    festival = is_festival(ts)
    cashback = get_cashback(app, amount, category) if status == "Success" else 0.0
    bank = random.choice(["SBI", "HDFC", "ICICI", "Axis", "Kotak", "PNB", "BOB", "Canara"])
    
    # Fraud signal (synthetic rule-based)
    fraud_flag = 0
    if amount > 90000 and status == "Failed" and ts.hour in [1, 2, 3, 4]:
        fraud_flag = 1
    if is_new_user and amount > 50000:
        fraud_flag = 1
    
    records.append({
        "transaction_id":    f"TXN{i+1:07d}",
        "timestamp":         ts.strftime("%Y-%m-%d %H:%M:%S"),
        "date":              ts.strftime("%Y-%m-%d"),
        "year":              ts.year,
        "month":             ts.month,
        "month_name":        ts.strftime("%B"),
        "day_of_week":       ts.strftime("%A"),
        "hour":              ts.hour,
        "is_weekend":        1 if ts.weekday() >= 5 else 0,
        "is_festival_day":   1 if festival else 0,
        "quarter":           f"Q{((ts.month - 1) // 3) + 1}",
        "sender_upi":        sender,
        "receiver_upi":      receiver,
        "payment_app":       app,
        "transaction_type":  txn_type,
        "merchant_category": category,
        "amount_inr":        amount,
        "status":            status,
        "state":             state,
        "city":              city,
        "city_tier":         city_tier,
        "device_type":       device,
        "bank":              bank,
        "is_repeat_user":    int(is_repeat),
        "is_new_user":       int(is_new_user),
        "cashback_inr":      cashback,
        "fraud_flag":        fraud_flag,
        "failure_reason":    random.choice(["Insufficient Balance", "Bank Server Down", "Wrong PIN", "Timeout"]) if status == "Failed" else "",
    })

df = pd.DataFrame(records)
df = df.sort_values("timestamp").reset_index(drop=True)

# ─── Save ─────────────────────────────────────────────────────────────────────
output_path = os.path.join(os.path.dirname(__file__), "upi_transactions.csv")
df.to_csv(output_path, index=False)

# ─── Summary Stats ────────────────────────────────────────────────────────────
print(f"\n✅ Dataset generated: {len(df):,} rows × {len(df.columns)} columns")
print(f"📁 Saved to: {output_path}")
print(f"\n📊 Quick Stats:")
print(f"   Total Volume:     ₹{df['amount_inr'].sum():,.0f}")
print(f"   Avg Ticket Size:  ₹{df['amount_inr'].mean():,.0f}")
print(f"   Success Rate:     {(df['status']=='Success').mean()*100:.1f}%")
print(f"   Fraud Flags:      {df['fraud_flag'].sum():,}")
print(f"   Date Range:       {df['date'].min()} → {df['date'].max()}")
print(f"\n   Top Apps:")
print(df['payment_app'].value_counts().to_string())
print(f"\n   Top States:")
print(df['state'].value_counts().head(5).to_string())
