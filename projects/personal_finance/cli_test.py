"""
Simple CLI to test paycheck calculations
"""

from database import FinanceDatabase
from paycheck_calculator import PaycheckCalculator
import os


def test_against_excel():
    """Test calculator against known Excel values"""
    
    # Create database and get tax brackets
    db_path = "test_finances.db"
    db = FinanceDatabase(db_path)
    brackets = db.get_tax_brackets()
    
    # Create calculator
    calc = PaycheckCalculator(brackets)
    
    # Your exact configuration from Excel
    # Key insight: Annual pre-tax income is $69,833.37
    # This means total annual pre-tax deductions are: $84,975 - $69,833.37 = $15,141.63
    
    config = {
        'salary': 84975.0,
        'pay_periods': 26,
        'contribution_401k_percent': 0.15,  # $490.24 per paycheck
        'employer_match_percent': 0.03,
        'max_employer_match': 3000.0,
        'hsa_per_paycheck': 50.59,
        'medical_insurance_per_paycheck': 46.67,
        'dental_premium_annual': 130.52,
        'vision_premium_annual': 124.28,
        'espp_percent': 0.04,
        'standard_deduction_federal': 15000.0,  # From Excel row 32
        'standard_deduction_state': 8000.0,  # From Excel row 35
        'savings_percent': 480.0 / 1813.28,  # Fixed $480 per paycheck to savings
        'savings2_percent': 175.0 / 1813.28,  # Fixed $175 per paycheck to savings 2
        'roth_ira_per_paycheck': 45.0,
        'brokerage_per_paycheck': 75.0,
        'crypto_per_paycheck': 0.0
    }
    
    result = calc.calculate(config)
    
    print("\n" + "="*80)
    print("💰 PAYCHECK CALCULATOR - PHASE 1 DELIVERABLE")
    print("="*80)
    
    print(f"\n📊 INCOME BREAKDOWN:")
    print(f"   Annual Salary:           ${result.annual_salary:>12,.2f}")
    print(f"   Pay Periods:             {result.pay_periods:>12}")
    print(f"   Paycheck Gross:          ${result.paycheck_gross:>12,.2f}")
    
    print(f"\n📉 PRE-TAX DEDUCTIONS:")
    print(f"   401(k) ({result.contribution_401k_percent*100:.0f}%):           -${result.contribution_401k:>12,.2f}")
    print(f"   Employer Match:          +${result.employer_match_401k:>12,.2f}")
    print(f"   HSA:                     -${result.hsa_contribution:>12,.2f}")
    print(f"   Medical Insurance:       -${result.medical_insurance:>12,.2f}")
    print(f"   Dental Insurance:        -${result.dental_insurance:>12,.2f}")
    print(f"   Vision Insurance:        -${result.vision_insurance:>12,.2f}")
    print(f"   ---")
    print(f"   Pre-Tax Income:          ${result.pre_tax_income:>12,.2f}")
    
    print(f"\n💸 TAXES:")
    print(f"   Federal Tax:             -${result.federal_tax:>12,.2f}  ({result.effective_federal_rate*100:>5.2f}%)")
    print(f"   State Tax (NY):          -${result.state_tax:>12,.2f}  ({result.effective_state_rate*100:>5.2f}%)")
    print(f"   Local Tax (NYC):         -${result.local_tax:>12,.2f}  ({result.effective_local_rate*100:>5.2f}%)")
    print(f"   Social Security:         -${result.social_security:>12,.2f}")
    print(f"   Medicare:                -${result.medicare:>12,.2f}")
    print(f"   ---")
    print(f"   Total Taxes:             -${result.total_taxes:>12,.2f}  ({result.total_tax_rate*100:>5.2f}%)")
    
    print(f"\n💵 POST-TAX INCOME:")
    print(f"   After Taxes:             ${result.post_tax_income:>12,.2f}")
    
    print(f"\n📤 POST-TAX DEDUCTIONS:")
    print(f"   ESPP ({result.espp/result.paycheck_gross*100:.0f}%):              -${result.espp:>12,.2f}")
    print(f"   NY SDI Tax:              -${result.ny_sdi_tax:>12,.2f}")
    print(f"   Life Insurance Adj:      -${result.li_adjustments:>12,.2f}")
    print(f"   ---")
    print(f"   Take Home:               ${result.take_home_income:>12,.2f}")
    
    print(f"\n🎯 ALLOCATIONS:")
    if result.to_savings > 0:
        print(f"   To Savings:              -${result.to_savings:>12,.2f}")
    if result.to_roth_ira > 0:
        print(f"   To Roth IRA:             -${result.to_roth_ira:>12,.2f}")
    if result.to_brokerage > 0:
        print(f"   To Brokerage:            -${result.to_brokerage:>12,.2f}")
    if result.to_crypto > 0:
        print(f"   To Crypto:               -${result.to_crypto:>12,.2f}")
    print(f"   ---")
    print(f"   Final Income (Checking): ${result.final_income:>12,.2f}")
    
    print(f"\n📅 ANNUAL SUMMARY:")
    print(f"   Annual 401(k):           ${result.annual_401k:>12,.2f}")
    print(f"   Annual Employer Match:   ${result.annual_employer_match:>12,.2f}")
    print(f"   Annual Federal Tax:      ${result.annual_federal_tax:>12,.2f}")
    print(f"   Annual State Tax:        ${result.annual_state_tax:>12,.2f}")
    print(f"   Annual Local Tax:        ${result.annual_local_tax:>12,.2f}")
    print(f"   Annual Take Home:        ${result.annual_take_home:>12,.2f}")
    
    print("\n" + "="*80)
    print("📋 COMPARISON WITH YOUR EXCEL:")
    print("="*80)
    
    excel_values = {
        'Paycheck Gross': 3268.27,
        'Pre-Tax Income': 2685.90,
        'Federal Tax': 273.71,
        'State Tax': 124.46,
        'Local Tax': 87.38,
        'Social Security': 202.63,
        'Medicare': 47.39,
        'Take Home': 1813.28,
        'Final Income': 1038.28
    }
    
    calculated_values = {
        'Paycheck Gross': result.paycheck_gross,
        'Pre-Tax Income': result.pre_tax_income,
        'Federal Tax': result.federal_tax,
        'State Tax': result.state_tax,
        'Local Tax': result.local_tax,
        'Social Security': result.social_security,
        'Medicare': result.medicare,
        'Take Home': result.take_home_income,
        'Final Income': result.final_income
    }
    
    print(f"\n{'Field':<20} {'Excel':>15} {'Calculated':>15} {'Match':>10}")
    print("-"*63)
    
    all_match = True
    for field in excel_values:
        excel_val = excel_values[field]
        calc_val = calculated_values[field]
        diff = abs(calc_val - excel_val)
        match = "✅" if diff < 5.0 else "❌"  # Within $5 tolerance
        
        if diff >= 5.0:
            all_match = False
        
        print(f"{field:<20} ${excel_val:>13,.2f} ${calc_val:>13,.2f}  {match:>8}")
    
    print("\n" + "="*80)
    if all_match:
        print("✅ ALL CALCULATIONS MATCH! Phase 1 Complete!")
    else:
        print("⚠️  Some calculations need adjustment...")
        print("   (This is normal - we'll fine-tune in Phase 2)")
    print("="*80)
    
    # Clean up
    db.close()
    if os.path.exists(db_path):
        os.remove(db_path)
    
    return result


if __name__ == "__main__":
    test_against_excel()
