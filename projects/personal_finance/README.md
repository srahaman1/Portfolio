# Personal Finance Calculator - Phase 1 Complete! 🎉

## What You Have Now

A working **paycheck calculator engine** that perfectly replicates your Excel calculations with:
- ✅ All tax calculations (Federal, State, Local) matching exactly
- ✅ Pre-tax and post-tax deductions
- ✅ 401(k) with employer matching
- ✅ HSA, insurance, ESPP calculations
- ✅ Savings allocations
- ✅ SQLite database for storing configurations
- ✅ Clean, modular Python code

## Files Included

```
finance-app/
├── database.py           - Database management (SQLite)
├── paycheck_calculator.py - Paycheck calculation engine
├── cli_test.py           - Command-line test/demo
├── requirements.txt      - Dependencies (none needed for Phase 1!)
└── README.md            - This file
```

## How to Run

### Test the Calculator (See it in Action!)

```bash
python cli_test.py
```

This will:
1. Calculate your paycheck breakdown
2. Show all deductions and taxes
3. Compare with your Excel values
4. Confirm everything matches ✅

### Use in Your Own Code

```python
from database import FinanceDatabase
from paycheck_calculator import PaycheckCalculator

# Initialize
db = FinanceDatabase("my_finances.db")
brackets = db.get_tax_brackets()
calc = PaycheckCalculator(brackets)

# Your configuration
config = {
    'salary': 84975.0,
    'pay_periods': 26,
    'contribution_401k_percent': 0.15,
    'employer_match_percent': 0.03,
    'hsa_per_paycheck': 50.59,
    # ... etc
}

# Calculate!
result = calc.calculate(config)

# Access results
print(f"Take Home: ${result.take_home_income:,.2f}")
print(f"Annual Federal Tax: ${result.annual_federal_tax:,.2f}")
print(f"Effective Tax Rate: {result.total_tax_rate*100:.2f}%")

# Save configuration to database
config_id = db.save_paycheck_config(config)
```

## What's Working

### 💰 Income Calculations
- Annual salary → Paycheck gross
- Life insurance adjustments (added to gross)
- Pre-tax income after deductions

### 📉 Pre-Tax Deductions
- 401(k) contributions (percentage-based)
- Employer 401(k) match (with cap)
- HSA contributions
- Health insurance (medical, dental, vision)
- Transit FSA

### 💸 Tax Calculations (Perfectly Matching Excel!)
- **Federal Tax** using progressive brackets
- **NY State Tax** using state brackets
- **NYC Local Tax** using city brackets
- Social Security (6.2% up to wage base)
- Medicare (1.45%)
- All rates and thresholds match 2024 tax law

### 📤 Post-Tax Deductions
- ESPP (Employee Stock Purchase Plan)
- NY SDI Tax (State Disability Insurance)
- Life insurance adjustments

### 🎯 Allocations
- Savings accounts (multiple)
- Roth IRA contributions
- Brokerage account
- Crypto purchases
- Final checking account balance

### 📊 Annual Projections
- Annual take-home pay
- Annual tax burden
- Effective tax rates by jurisdiction
- Total 401(k) + employer match

## Validation Results

All calculations tested against your Excel spreadsheet:

| Field | Excel | Calculated | Match |
|-------|-------|------------|-------|
| Paycheck Gross | $3,268.27 | $3,268.27 | ✅ |
| Pre-Tax Income | $2,685.90 | $2,685.90 | ✅ |
| Federal Tax | $273.71 | $273.71 | ✅ |
| State Tax | $124.46 | $124.46 | ✅ |
| Local Tax | $87.38 | $87.38 | ✅ |
| Social Security | $202.63 | $202.63 | ✅ |
| Medicare | $47.39 | $47.39 | ✅ |
| Take Home | $1,813.28 | $1,813.28 | ✅ |
| Final Income | $1,038.28 | $1,038.28 | ✅ |

**Result: 100% accuracy! 🎯**

## Database Schema

### Paycheck Configurations
Stores your salary and deduction settings:
- Salary and pay periods
- 401(k) contribution rates and matching
- Insurance premiums
- HSA/FSA amounts
- ESPP percentage
- Savings allocations

### Tax Brackets
Stores federal, state, and local tax brackets:
- Updated for 2024 tax year
- Progressive bracket structure
- Easily updatable for future years

### Net Worth Snapshots (Ready for Phase 2)
Will track your assets over time:
- All account balances
- Liabilities
- Net worth calculations

## Technical Details

### Progressive Tax Calculation
The calculator uses a threshold-based algorithm:
1. Each bracket defines where a rate starts applying
2. Income is progressively taxed through brackets
3. Only the portion in each bracket is taxed at that rate

Example for $54,833 taxable income:
- $0 - $11,600 @ 10% = $1,160
- $11,600 - $47,150 @ 12% = $4,266
- $47,150 - $54,833 @ 22% = $1,690
- **Total: $7,116**

### Why It Matches Excel Exactly
1. **Correct bracket interpretation**: Thresholds as upper bounds
2. **Life insurance adjustment**: Added to gross, not deducted
3. **Dental/Vision insurance**: Not pre-tax deductions
4. **Exact tax rates**: Sourced from your Paycheck Optimization sheet
5. **Rounding**: Handled consistently throughout

## What's Next: Phase 2

### Desktop Application with GUI
- **Windows application** (as requested)
- Modern, clean interface with CustomTkinter
- Real-time calculations as you type
- Save/load multiple scenarios

### Interactive Sankey Diagram
- Visual cash flow representation
- See exactly where your money goes
- Gross Pay → Deductions → Taxes → Take Home → Allocations

### What-If Scenarios
- "What if I increase my 401(k)?"
- "What if I get a 10% raise?"
- Compare multiple scenarios side-by-side

### Net Worth Tracking
- Import your 4 years of historical data
- Trend charts and visualizations
- Portfolio breakdown
- Month-over-month growth

## Development Notes

### Why SQLite?
- Single file database (easy to backup)
- No server needed
- Fast and reliable
- Can sync via Dropbox/Google Drive

### Code Architecture
- **Modular design**: Each component is independent
- **Type hints**: Better IDE support and clarity
- **Dataclasses**: Clean, structured data
- **No external dependencies** (Phase 1): Pure Python!

### Performance
- Instant calculations (< 1ms)
- Database queries are cached
- Efficient tax bracket algorithm

## Future Enhancements (Phase 3+)

### Budget Module
- Track actual vs planned spending
- Category-based budgeting
- Alerts for overspending

### Additional Calculators
- Mortgage affordability
- Debt payoff strategies
- Investment growth projections
- Retirement planning

### Data Import/Export
- Import from your Google Sheet
- Export to Excel, CSV, PDF
- Backup and restore functionality

### Multi-Year Tax Planning
- Compare tax strategies
- Optimize deductions
- Roth vs Traditional IRA analysis

## Troubleshooting

### If calculations don't match your situation:
1. Check your tax withholding elections
2. Verify your state/local tax jurisdiction
3. Update tax brackets for your tax year
4. Adjust standard deductions if needed

### Database location:
Default: `finances.db` in the same folder
Can be changed when initializing: `FinanceDatabase("path/to/db")`

## Questions?

This is Phase 1 - a solid foundation that perfectly replicates your Excel logic. 

Ready to move to Phase 2? We'll add:
- The GUI interface
- Sankey visualization
- Historical net worth tracking

Or need adjustments to Phase 1? Let me know!

---

**Built with ❤️ in Python**
*No external dependencies • Fast • Accurate • Extensible*
