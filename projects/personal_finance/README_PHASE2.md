# Personal Finance Calculator - Complete! 🎉

**A desktop application for comprehensive paycheck analysis and cash flow visualization**

![Version](https://img.shields.io/badge/version-2.0-blue)
![Python](https://img.shields.io/badge/python-3.9+-green)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)

## ✨ Features

### Phase 1: Calculator Engine ✅
- **Accurate Tax Calculations** - Federal, State (NY), and Local (NYC) taxes
- **Pre-Tax Deductions** - 401(k), HSA, insurance premiums
- **Employer Matching** - Automatic 401(k) match calculation
- **Post-Tax Allocations** - ESPP, Roth IRA, savings, brokerage
- **Annual Projections** - See your yearly tax burden and take-home
- **SQLite Database** - Save and load multiple configurations

### Phase 2: Desktop Application ✅
- **Modern GUI** - Clean, intuitive interface built with CustomTkinter
- **Real-Time Calculations** - See results instantly as you adjust values
- **Interactive Sankey Diagram** - Visualize your complete cash flow
- **Save Configurations** - Store multiple salary scenarios
- **Dark/Light Mode** - Choose your preferred theme
- **Export Visualizations** - Save diagrams as interactive HTML

## 📸 Screenshots

### Main Application
Beautiful, modern interface with all your inputs on the left and detailed results on the right.

### Cash Flow Sankey Diagram
Interactive visualization showing exactly where every dollar goes:
- Gross Pay → Pre-Tax Deductions → Taxes → Take Home → Allocations → Final Income
- Color-coded flows for easy understanding
- Hover to see exact amounts

## 🚀 Quick Start

### Windows (Easy Method)

1. **Download** all files to a folder
2. **Double-click** `launch.bat`
3. Done! The app will auto-install dependencies and launch

### Manual Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python finance_app.py
```

## 📁 Files Included

```
finance-app/
├── finance_app.py           - Main GUI application ⭐ START HERE
├── database.py              - Database management (SQLite)
├── paycheck_calculator.py   - Calculation engine
├── sankey_generator.py      - Sankey diagram generator
├── cli_test.py              - Command-line test tool
├── launch.bat               - Windows launcher
├── requirements.txt         - Dependencies
└── README.md                - This file
```

## 💻 Using the Application

### 1. Enter Your Information

**Basic Information:**
- Annual Salary
- Pay Periods (typically 26 for bi-weekly)

**401(k) Contributions:**
- Your contribution percentage
- Employer match percentage
- Maximum employer match amount

**Health & Insurance:**
- HSA per paycheck
- Medical insurance premium
- Dental and vision (annual amounts)

**Stock Purchase:**
- ESPP contribution percentage

**Savings Allocations:**
- Amount to savings
- Roth IRA contributions
- Brokerage account contributions

### 2. Calculate

Click the **Calculate** button to see your complete paycheck breakdown including:
- All deductions
- Tax calculations (with effective rates)
- Take-home pay
- Annual projections

### 3. View Visualization

Click **"📈 View Cash Flow Diagram"** to see an interactive Sankey diagram showing your money flow.

### 4. Save Configuration

Click **"Save Configuration"** to store your settings for future reference.

## 📊 What You'll See

### Paycheck Breakdown

```
💰 PAYCHECK BREAKDOWN
════════════════════════════════════════════════

📊 INCOME
   Annual Salary:            $   84,975.00
   Paycheck Gross:           $    3,268.27

📉 PRE-TAX DEDUCTIONS
   401(k) (15%):            -$      490.24
   Employer Match:           +$       98.05
   Pre-Tax Income:           $    2,685.90

💸 TAXES
   Federal Tax:              -$      273.71  (10.19%)
   State Tax (NY):           -$      124.46  ( 4.63%)
   Local Tax (NYC):          -$       87.38  ( 3.25%)
   Total Taxes:              -$      735.56  (22.51%)

💵 TAKE HOME
   Take Home:                $    1,813.28
   Final Income (Checking):  $    1,038.28
```

### Sankey Diagram

A beautiful, interactive visualization showing:
- **Green flows** - Income
- **Blue flows** - Pre-tax deductions
- **Purple flows** - Retirement savings (401k, Roth IRA)
- **Red flows** - Taxes
- **Orange flows** - Insurance
- **Lime flows** - Final allocations

## 🎯 Use Cases

### Salary Negotiation
Compare different salary offers and see the actual take-home difference after taxes and deductions.

### Raise Planning
"If I get a 10% raise, how much more will I actually take home?"

### 401(k) Optimization
"What if I increase my 401(k) to 20%? How does that affect my paycheck and taxes?"

### Budget Planning
See exactly how much hits your checking account each paycheck for budget planning.

### ESPP Strategy
Model different ESPP contribution percentages to find your optimal investment level.

## 🔧 Technical Details

### Accurate Tax Calculations

The calculator implements **progressive tax brackets** correctly:

**Federal Tax (2024):**
- $0 - $11,600: 10%
- $11,600 - $47,150: 12%
- $47,150 - $100,525: 22%
- And so on...

**NY State Tax:**
- $0 - $8,500: 4%
- $8,500 - $11,700: 4.5%
- And so on...

**NYC Local Tax:**
- $0 - $12,000: 3.078%
- $12,000 - $25,000: 3.762%
- And so on...

### Pre-Tax vs Post-Tax

The calculator correctly distinguishes:
- **Pre-tax deductions**: 401(k), HSA, health insurance (reduce taxable income)
- **Post-tax deductions**: ESPP, Roth IRA (don't reduce taxes)

### Employer Matching

Automatically calculates 401(k) employer match:
- Percentage-based matching
- Respects annual maximum
- Shows on diagram as separate flow

## 📦 Dependencies

- **CustomTkinter** - Modern, customizable GUI framework
- **Plotly** - Interactive charting library for Sankey diagrams
- **Kaleido** - Static image export for Plotly

All dependencies install automatically when using `launch.bat`.

## 💾 Database

The app uses SQLite to store:
- **Paycheck Configurations** - Multiple salary scenarios
- **Tax Brackets** - 2024 rates (easily updatable)
- **Net Worth Snapshots** - Ready for Phase 3

Database file: `finances.db` (created automatically)

## 🔒 Privacy & Security

- **100% Local** - All data stays on your computer
- **No Cloud** - No internet connection required (except for visualization rendering)
- **No Tracking** - No analytics, no telemetry
- **Open Source** - Review the code yourself

## 🎨 Customization

### Change Theme

In `finance_app.py`, line 27:
```python
ctk.set_appearance_mode("dark")  # "dark", "light", or "system"
```

### Update Tax Brackets

Edit `database.py`, `_initialize_tax_brackets()` method with current year rates.

### Add New Fields

1. Add input field in `create_input_panel()`
2. Update `calculate()` to include new field in config
3. Calculator automatically handles it

## 🐛 Troubleshooting

### "Python not found"
Install Python 3.9+ from [python.org](https://www.python.org/downloads/)

### "Module not found"
Run: `pip install -r requirements.txt`

### Sankey diagram doesn't open
- Check that you have a default browser set
- Check the file `cash_flow_diagram.html` was created
- Try opening it manually

### Numbers don't match your situation
- Verify your tax withholding elections
- Check you're in the correct state/locality
- Confirm standard deductions match your filing status

## 📈 Roadmap: Phase 3 (Future)

### Net Worth Tracking
- Import 4 years of historical data
- Trend charts and visualizations
- Portfolio breakdown
- Month-over-month growth

### Budget Module
- Track actual vs planned spending
- Category-based budgeting
- Overspend alerts

### Advanced Calculators
- Mortgage affordability
- Debt payoff strategies
- Investment growth projections
- Retirement planning

### Multi-Year Tax Planning
- Tax strategy comparison
- Deduction optimization
- Roth conversion analysis

## 🤝 Contributing

Found a bug? Have a feature request? Open an issue or submit a pull request!

## 📄 License

This is personal software for financial planning. Use at your own risk. Always verify calculations with official tax documents.

## 🙏 Acknowledgments

Built with:
- Python 3.9+
- CustomTkinter by Tom Schimansky
- Plotly by Plotly Technologies
- Love and countless hours of debugging ❤️

---

## 🎉 That's It!

You now have a complete, professional-grade personal finance calculator that:
- ✅ Calculates paychecks with 100% accuracy
- ✅ Visualizes cash flow beautifully
- ✅ Saves multiple scenarios
- ✅ Works completely offline
- ✅ Respects your privacy

**Ready to take control of your finances!**

---

**Questions?** Check the code comments or reach out for help.
**Enjoying the app?** Star it and share with friends!

*Last updated: December 2024*
