"""
UPI Pulse - Exploratory Data Analysis
Run this after generate_data.py to get key insights
Output: Multiple summary CSV files for Power BI reference + printed insights
"""

import pandas as pd
import numpy as np
import os

print("=" * 60)
print("   UPI PULSE — EDA ANALYSIS REPORT")
print("=" * 60)

df = pd.read_csv("upi_transactions.csv", parse_dates=["timestamp", "date"])

# ── 1. EXECUTIVE OVERVIEW ────────────────────────────────────────────────────
print("\n📊 EXECUTIVE OVERVIEW")
print("-" * 40)
total_txns     = len(df)
total_volume   = df['amount_inr'].sum()
avg_ticket     = df['amount_inr'].mean()
success_rate   = (df['status'] == 'Success').mean() * 100
failed_rate    = (df['status'] == 'Failed').mean() * 100
total_cashback = df['cashback_inr'].sum()
fraud_count    = df['fraud_flag'].sum()

print(f"  Total Transactions : {total_txns:,}")
print(f"  Total Volume       : ₹{total_volume:,.0f} (~₹{total_volume/1e7:.1f} Cr)")
print(f"  Avg Ticket Size    : ₹{avg_ticket:,.0f}")
print(f"  Success Rate       : {success_rate:.1f}%")
print(f"  Failed Rate        : {failed_rate:.1f}%")
print(f"  Total Cashback     : ₹{total_cashback:,.0f}")
print(f"  Fraud Flags        : {int(fraud_count)}")

# ── 2. PAYMENT APP ANALYSIS ──────────────────────────────────────────────────
print("\n📱 PAYMENT APP BREAKDOWN")
print("-" * 40)
app_stats = df.groupby('payment_app').agg(
    transactions=('transaction_id', 'count'),
    total_volume=('amount_inr', 'sum'),
    avg_ticket=('amount_inr', 'mean'),
    success_rate=('status', lambda x: (x == 'Success').mean() * 100),
    cashback_given=('cashback_inr', 'sum')
).round(2).sort_values('transactions', ascending=False)
app_stats['market_share_%'] = (app_stats['transactions'] / total_txns * 100).round(1)
print(app_stats[['transactions', 'market_share_%', 'avg_ticket', 'success_rate']].to_string())

# ── 3. MERCHANT CATEGORY ANALYSIS ────────────────────────────────────────────
print("\n🛍️  MERCHANT CATEGORY INSIGHTS")
print("-" * 40)
cat_stats = df.groupby('merchant_category').agg(
    transactions=('transaction_id', 'count'),
    total_volume=('amount_inr', 'sum'),
    avg_ticket=('amount_inr', 'mean'),
    success_rate=('status', lambda x: (x == 'Success').mean() * 100)
).round(2).sort_values('total_volume', ascending=False)
print(cat_stats.to_string())

# ── 4. TIME INTELLIGENCE ──────────────────────────────────────────────────────
print("\n⏰  PEAK HOURS (Top 5)")
print("-" * 40)
hourly = df.groupby('hour')['transaction_id'].count().sort_values(ascending=False)
print(hourly.head(5).to_string())

print("\n📅  DAY OF WEEK PATTERNS")
day_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
daily = df.groupby('day_of_week').agg(
    transactions=('transaction_id','count'),
    avg_amount=('amount_inr','mean')
).reindex(day_order).round(2)
print(daily.to_string())

print("\n📆  MONTHLY TRENDS")
monthly = df.groupby(['year','month','month_name']).agg(
    transactions=('transaction_id','count'),
    volume=('amount_inr','sum'),
    avg_ticket=('amount_inr','mean')
).round(2)
print(monthly.to_string())

# ── 5. GEO ANALYSIS ──────────────────────────────────────────────────────────
print("\n🗺️  TOP STATES BY VOLUME")
print("-" * 40)
state_stats = df.groupby('state').agg(
    transactions=('transaction_id','count'),
    volume=('amount_inr','sum'),
    avg_ticket=('amount_inr','mean')
).sort_values('volume', ascending=False)
print(state_stats.head(8).to_string())

print("\n🏙️  TIER 1 vs TIER 2 CITIES")
tier_stats = df.groupby('city_tier').agg(
    transactions=('transaction_id','count'),
    volume=('amount_inr','sum'),
    avg_ticket=('amount_inr','mean'),
    success_rate=('status', lambda x: (x=='Success').mean()*100)
).round(2)
print(tier_stats.to_string())

# ── 6. FESTIVAL ANALYSIS ──────────────────────────────────────────────────────
print("\n🎉  FESTIVAL vs NORMAL DAY COMPARISON")
print("-" * 40)
fest = df.groupby('is_festival_day').agg(
    transactions=('transaction_id','count'),
    avg_amount=('amount_inr','mean'),
    total_volume=('amount_inr','sum')
).round(2)
fest.index = ['Normal Day', 'Festival Day']
print(fest.to_string())

# ── 7. FAILURE ANALYSIS ───────────────────────────────────────────────────────
print("\n⚠️  FAILURE REASON BREAKDOWN")
print("-" * 40)
failed_df = df[df['status'] == 'Failed']
print(failed_df['failure_reason'].value_counts().to_string())

# ── 8. DEVICE ANALYSIS ───────────────────────────────────────────────────────
print("\n📱 DEVICE TYPE ANALYSIS")
print("-" * 40)
device_stats = df.groupby('device_type').agg(
    transactions=('transaction_id','count'),
    avg_ticket=('amount_inr','mean'),
    success_rate=('status', lambda x: (x=='Success').mean()*100)
).round(2)
print(device_stats.to_string())

# ── SAVE SUMMARY FILES ────────────────────────────────────────────────────────
app_stats.reset_index().to_csv("summary_by_app.csv", index=False)
cat_stats.reset_index().to_csv("summary_by_category.csv", index=False)
state_stats.reset_index().to_csv("summary_by_state.csv", index=False)
monthly.reset_index().to_csv("summary_monthly.csv", index=False)

print("\n\n✅ Summary CSVs saved:")
print("   → summary_by_app.csv")
print("   → summary_by_category.csv")
print("   → summary_by_state.csv")
print("   → summary_monthly.csv")
print("\n💡 Load upi_transactions.csv into Power BI to get started!")
