# 🚀 Quick Start Guide

## For Windows Users (Easiest!)

1. **Download all files** to a folder on your computer (e.g., `C:\Finance-App\`)

2. **Double-click `launch.bat`**
   - First time: Will install dependencies (takes 1-2 minutes)
   - Future times: Opens instantly

3. **Start calculating!**
   - Enter your salary and deductions
   - Click "Calculate"
   - View your Sankey diagram

## What You'll See

### The Application
- **Left side**: Input form with all your salary and deduction info
- **Right side**: Detailed breakdown of your paycheck
- **Bottom**: Button to view your cash flow diagram

### Your First Calculation

The app comes pre-loaded with sample values ($84,975 salary). Just click "Calculate" to see it in action!

## Tips

### Change Your Salary
1. Update the "Annual Salary" field
2. Click "Calculate"
3. See new results instantly

### View Cash Flow
1. After calculating, click "📈 View Cash Flow Diagram"
2. Your browser opens with an interactive diagram
3. Hover over any flow to see exact amounts

### Save Your Configuration
1. Click "Save Configuration"
2. Your settings are stored in the database
3. Auto-loads next time you open the app

### Compare Scenarios
Want to compare a 10% raise?
1. Note your current "Final Income"
2. Increase salary by 10%
3. Calculate again
4. Compare the results!

## Troubleshooting

### Python Not Installed?
Download from: https://www.python.org/downloads/
- Get version 3.9 or higher
- **Important**: Check "Add Python to PATH" during installation

### launch.bat Doesn't Work?
Try manual installation:
```
pip install -r requirements.txt
python finance_app.py
```

### Sankey Diagram Not Opening?
The diagram is saved as `cash_flow_diagram.html` in your folder. Try opening it manually.

## Next Steps

1. **Customize Your Numbers**
   - Enter your actual salary
   - Update your 401(k) percentage
   - Add your insurance costs

2. **Experiment**
   - Try different ESPP percentages
   - See how 401(k) changes affect taxes
   - Model a raise or promotion

3. **Save Scenarios**
   - Save your current situation
   - Save an "optimistic" scenario (with raise)
   - Save a "frugal" scenario (lower spending)

## Need Help?

- Read `README_PHASE2.md` for full documentation
- Check the code comments for technical details
- All calculations match standard tax tables

---

**That's it! You're ready to take control of your finances! 💪**
