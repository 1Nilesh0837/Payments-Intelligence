# 🔧 Power BI Setup Guide — UPI Pulse Dashboard

## Prerequisites
- Power BI Desktop (free) → https://powerbi.microsoft.com/desktop/
- Python 3.8+ (to generate dataset)

---

## Step 1: Generate the Dataset

```bash
cd data/
pip install pandas numpy
python generate_data.py
```

This creates `upi_transactions.csv` (50,000 rows, 28 columns).

---

## Step 2: Load Data into Power BI

1. Open **Power BI Desktop**
2. Click **Get Data** → **Text/CSV**
3. Select `data/upi_transactions.csv`
4. In the preview, click **Transform Data**
5. In Power Query Editor:
   - Set `timestamp` column → Data Type: **Date/Time**
   - Set `date` column → Data Type: **Date**
   - Set `amount_inr` → Data Type: **Decimal Number**
   - Set `cashback_inr` → Data Type: **Decimal Number**
   - Set `hour`, `month`, `year` → Data Type: **Whole Number**
6. Click **Close & Apply**

---

## Step 3: Create a Date Table (Required for Time Intelligence)

In Power BI, go to **Modeling** → **New Table**, paste:

```dax
DateTable = 
ADDCOLUMNS(
    CALENDAR(DATE(2024,1,1), DATE(2024,12,31)),
    "Year", YEAR([Date]),
    "Month", MONTH([Date]),
    "Month Name", FORMAT([Date], "MMMM"),
    "Month Short", FORMAT([Date], "MMM"),
    "Quarter", "Q" & ROUNDUP(MONTH([Date])/3, 0),
    "Day of Week", FORMAT([Date], "dddd"),
    "Day Number", WEEKDAY([Date], 2),
    "Is Weekend", IF(WEEKDAY([Date], 2) >= 6, 1, 0),
    "Week Number", WEEKNUM([Date])
)
```

Then go to **Model View** → drag `DateTable[Date]` to `upi_transactions[date]` to create a relationship.

---

## Step 4: Add All DAX Measures

1. In **Report View**, right-click `upi_transactions` table → **New Measure**
2. Copy-paste each measure from `dax_measures/all_measures.dax`
3. Organize measures into a **Measure Table**:
   - Create empty table: **Enter Data** → name it `_Measures`
   - Move all measures to this table by changing Home Table in measure properties

---

## Step 5: Build the 5 Report Pages

### Page 1: 📊 Executive Overview
**Visuals to add:**
| Visual | Fields | Notes |
|--------|--------|-------|
| Card | Total Transactions | Format: #,##0 |
| Card | Total Volume (₹) | Format: ₹#,##0 |
| Card | Success Rate % | Format: 0.0% |
| Card | Average Ticket Size | Format: ₹#,##0 |
| Card | Fraud Transactions | Red color |
| Line Chart | date → Volume MoM % Change | Title: Monthly Volume Trend |
| Donut Chart | payment_app → Total Transactions | Title: App Market Share |
| Bar Chart | merchant_category → Total Volume (₹) | Sort descending |
| KPI Visual | Total Volume (₹) vs Rolling 30-Day Volume | |

**Slicers:** payment_app, quarter, city_tier

---

### Page 2: ⏰ Time Intelligence
**Visuals to add:**
| Visual | Fields | Notes |
|--------|--------|-------|
| Area Chart | date → Total Volume (₹) | Monthly trend |
| Clustered Bar | hour → Total Transactions | Peak hours |
| Matrix | month_name × day_of_week → Total Transactions | Heatmap style |
| Column Chart | month_name → Transactions MoM % Change | Conditional format |
| Card | Rolling 7-Day Transactions | |
| Card | Festival Day Volume | |
| Stacked Bar | month_name → Total Volume by payment_app | |

**Tip:** Use conditional formatting on the Matrix → Background Color → based on value to create a heatmap effect.

---

### Page 3: 🗺️ Geo Analysis
**Visuals to add:**
| Visual | Fields | Notes |
|--------|--------|-------|
| Filled Map | state → Total Volume (₹) | Color saturation |
| Bar Chart | state → Total Transactions (top 10) | |
| Donut | city_tier → Total Volume (₹) | Tier 1 vs Tier 2 |
| Table | state, transactions, volume, success_rate | Top 13 states |
| Column Chart | state → Success Rate % | Sort ascending to show problem states |
| Card | Tier 1 vs Tier 2 Ratio | |

**Tip:** For the map, go to Format → Map styles → enable "Show labels"

---

### Page 4: 🛍️ Merchant Analytics
**Visuals to add:**
| Visual | Fields | Notes |
|--------|--------|-------|
| Treemap | merchant_category → Total Volume (₹) | |
| Bar Chart | merchant_category → Average Ticket Size | |
| Line & Clustered | merchant_category → Transactions + Success Rate % | Dual axis |
| Table | category, transactions, volume, avg_ticket, success_rate | |
| Donut | transaction_type → Total Transactions | |
| Waterfall | merchant_category → Total Volume (₹) | |
| Card | Repeat User Rate % | |
| Scatter | avg_ticket (X) vs Total Volume (Y), size = Transactions | By category |

---

### Page 5: ⚠️ Fraud & Anomaly Signals
**Visuals to add:**
| Visual | Fields | Notes |
|--------|--------|-------|
| Card | Fraud Transactions | Red background |
| Card | Fraud Rate % | |
| Card | Night Hour Failures | |
| Line Chart | date → Total Transactions with Anomaly Detection | Enable Analytics pane → Anomaly Detection |
| Bar Chart | failure_reason → count | Failed txns only |
| Bar Chart | hour → Night Hour Failures | Filter hour 0–5 |
| Table | Fraud transactions detail | Filter fraud_flag = 1 |
| Donut | device_type → Failed transactions | |
| Column | bank → Failed Rate % | |

**Tip:** On the Line Chart, go to **Analytics pane** → turn on **Anomaly detection** → Power BI will auto-highlight anomalous spikes!

---

## Step 6: Design & Theming

### Recommended Color Theme (JSON — paste in View → Themes → Customize)
```json
{
  "name": "UPI Pulse Dark",
  "dataColors": ["#6C63FF", "#00D4AA", "#FF6B6B", "#FFD93D", "#4ECDC4", "#45B7D1"],
  "background": "#1E1E2E",
  "foreground": "#FFFFFF",
  "tableAccent": "#6C63FF"
}
```

### Formatting Tips:
- Background: Dark (#1A1A2E) or White — both look professional
- Font: Segoe UI throughout
- Add company logo placeholder in top-left
- Use **Bookmarks** for toggle between views
- Add **page navigation buttons** at the bottom

---

## Step 7: What-If Parameter (Revenue Impact Simulator)

1. Go to **Modeling** → **New Parameter**
2. Name: `Success Rate Improvement`
3. Type: Whole Number, Min: 0, Max: 20, Increment: 1, Default: 5
4. This auto-creates a slicer — place it on Page 1 or Page 5
5. Add a Card visual with `Projected Volume Gain` measure
6. Label it: *"If we improve success rate by X%, we recover ₹Y"*

---

## Step 8: Row Level Security (Optional but Impressive)

1. Go to **Modeling** → **Manage Roles**
2. Create role: `PhonePe_Analyst`
3. Add table filter: `[payment_app] = "PhonePe"`
4. Create roles for each app
5. In GitHub README, mention: *"Implements RLS for app-wise access control"*

---

## Step 9: Publish & Share

**Option A (Free):** Export as PDF → `File → Export → PDF`
**Option B (Free):** Publish to Power BI Service (free account) → Share link
**Option C (GitHub):** 
- Save `.pbix` file to `/powerbi/UPI_Pulse.pbix`
- Add screenshots of all 5 pages to `/screenshots/`
- Both `.pbix` and screenshots go in your repo

---

## Drillthrough Setup

1. Go to Page 3 (Geo Analysis)
2. In **Visualizations pane** → **Drillthrough** section
3. Drag `state` to the drillthrough field
4. Now right-clicking any state in other pages → Drillthrough → Geo Analysis

---

## Quick Checklist Before GitHub Upload

- [ ] `data/upi_transactions.csv` exists (50,000 rows)
- [ ] `powerbi/UPI_Pulse.pbix` saved
- [ ] Screenshots of all 5 pages in `screenshots/`
- [ ] `README.md` has project description + screenshots
- [ ] `insights/key_findings.md` has 10+ business insights
- [ ] `requirements.txt` lists Python packages
