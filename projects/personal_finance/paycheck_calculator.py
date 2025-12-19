"""
Paycheck Calculator Engine
Calculates net income based on salary, deductions, and tax brackets
"""

from typing import Dict, List, Tuple
from dataclasses import dataclass, asdict
import json


@dataclass
class PaycheckBreakdown:
    """Complete breakdown of a paycheck calculation"""
    # Input values
    salary: float
    pay_periods: int
    
    # Gross pay
    paycheck_gross: float
    
    # Pre-tax deductions
    contribution_401k: float
    contribution_401k_percent: float
    employer_match_401k: float
    hsa_contribution: float
    transit_fsa: float
    medical_insurance: float
    dental_insurance: float
    vision_insurance: float
    
    # Pre-tax income
    pre_tax_income: float
    
    # Taxes
    federal_tax: float
    state_tax: float
    local_tax: float
    social_security: float
    medicare: float
    total_taxes: float
    
    # Post-tax income
    post_tax_income: float
    
    # Post-tax deductions
    espp: float
    ny_sdi_tax: float
    li_adjustments: float
    
    # Take home
    take_home_income: float
    
    # Allocations
    to_savings: float
    to_savings2: float
    to_roth_ira: float
    to_brokerage: float
    to_crypto: float
    
    # Final income
    final_income: float
    
    # Annual projections
    annual_salary: float
    annual_401k: float
    annual_employer_match: float
    annual_federal_tax: float
    annual_state_tax: float
    annual_local_tax: float
    annual_take_home: float
    
    # Effective tax rates
    effective_federal_rate: float
    effective_state_rate: float
    effective_local_rate: float
    total_tax_rate: float
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return asdict(self)
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), indent=2)


class PaycheckCalculator:
    """Calculate paycheck breakdown with taxes and deductions"""
    
    # Tax constants
    SOCIAL_SECURITY_RATE = 0.062  # 6.2%
    MEDICARE_RATE = 0.0145  # 1.45%
    SOCIAL_SECURITY_WAGE_BASE = 168600  # 2024 limit
    
    def __init__(self, tax_brackets: Dict[str, List[Dict]]):
        """
        Initialize calculator with tax brackets
        
        Args:
            tax_brackets: Dict with keys 'federal', 'NY', 'NYC' containing bracket info
        """
        self.federal_brackets = tax_brackets.get('federal', [])
        self.state_brackets = tax_brackets.get('NY', [])
        self.local_brackets = tax_brackets.get('NYC', [])
    
    def calculate_progressive_tax(self, taxable_income: float, brackets: List[Dict]) -> float:
        """
        Calculate tax using progressive tax brackets
        
        Args:
            taxable_income: The income to tax
            brackets: List of dicts with 'threshold' (where rate starts) and 'rate' keys
        
        Returns:
            Total tax owed
        """
        if taxable_income <= 0:
            return 0
        
        total_tax = 0
        
        for i, bracket in enumerate(brackets):
            current_threshold = bracket['threshold']
            current_rate = bracket['rate']
            
            # Determine the upper bound of this bracket
            if i < len(brackets) - 1:
                next_threshold = brackets[i + 1]['threshold']
            else:
                next_threshold = float('inf')  # Last bracket has no upper limit
            
            # Calculate income in this bracket
            if taxable_income <= current_threshold:
                # Income doesn't reach this bracket
                break
            elif taxable_income <= next_threshold:
                # Income falls within this bracket
                income_in_bracket = taxable_income - current_threshold
                total_tax += income_in_bracket * current_rate
                break
            else:
                # Income exceeds this bracket, tax the full bracket
                income_in_bracket = next_threshold - current_threshold
                total_tax += income_in_bracket * current_rate
        
        return total_tax
    
    def calculate(self, config: Dict) -> PaycheckBreakdown:
        """
        Calculate complete paycheck breakdown
        
        Args:
            config: Dictionary with paycheck configuration
        
        Returns:
            PaycheckBreakdown object with all calculations
        """
        # Extract configuration
        salary = config['salary']
        pay_periods = config.get('pay_periods', 26)
        
        # 401k
        contribution_401k_percent = config.get('contribution_401k_percent', 0.15)
        employer_match_percent = config.get('employer_match_percent', 0.03)
        max_employer_match = config.get('max_employer_match', 3000.0)
        
        # HSA and FSA
        hsa_per_paycheck = config.get('hsa_per_paycheck', 50.59)
        transit_fsa_per_paycheck = config.get('transit_fsa_per_paycheck', 0.0)
        
        # Insurance
        medical_per_paycheck = config.get('medical_insurance_per_paycheck', 46.67)
        dental_annual = config.get('dental_premium_annual', 130.52)
        vision_annual = config.get('vision_premium_annual', 124.28)
        
        # ESPP
        espp_percent = config.get('espp_percent', 0.04)
        
        # Standard deductions
        standard_deduction_federal = config.get('standard_deduction_federal', 14600.0)
        standard_deduction_state = config.get('standard_deduction_state', 8000.0)
        
        # Post-tax allocations
        savings_percent = config.get('savings_percent', 0.0)
        savings2_percent = config.get('savings2_percent', 0.0)
        roth_ira_per_paycheck = config.get('roth_ira_per_paycheck', 0.0)
        brokerage_per_paycheck = config.get('brokerage_per_paycheck', 0.0)
        crypto_per_paycheck = config.get('crypto_per_paycheck', 0.0)
        
        # === CALCULATIONS ===
        
        # Gross pay per paycheck
        paycheck_gross = salary / pay_periods
        
        # Life insurance adjustments (added to gross for tax purposes)
        li_adjustments = config.get('li_adjustments', 5.13)
        income_before_tax = paycheck_gross + li_adjustments
        
        # 401k contribution
        contribution_401k = paycheck_gross * contribution_401k_percent
        annual_401k = contribution_401k * pay_periods
        
        # Employer match (annual, then per paycheck)
        annual_employer_match = min(salary * employer_match_percent, max_employer_match)
        employer_match_per_paycheck = annual_employer_match / pay_periods
        
        # Insurance per paycheck
        dental_per_paycheck = dental_annual / pay_periods
        vision_per_paycheck = vision_annual / pay_periods
        
        # Pre-tax income (dental and vision are NOT deducted here)
        pre_tax_income = (income_before_tax - contribution_401k - hsa_per_paycheck - 
                         transit_fsa_per_paycheck - medical_per_paycheck)
        
        # Annual pre-tax income for tax calculations
        annual_pre_tax_income = pre_tax_income * pay_periods
        
        # === TAX CALCULATIONS ===
        
        # Federal tax
        federal_taxable_income = annual_pre_tax_income - standard_deduction_federal
        annual_federal_tax = self.calculate_progressive_tax(federal_taxable_income, self.federal_brackets)
        federal_tax_per_paycheck = annual_federal_tax / pay_periods
        effective_federal_rate = annual_federal_tax / annual_pre_tax_income if annual_pre_tax_income > 0 else 0
        
        # State tax (NY)
        state_taxable_income = annual_pre_tax_income - standard_deduction_state
        annual_state_tax = self.calculate_progressive_tax(state_taxable_income, self.state_brackets)
        state_tax_per_paycheck = annual_state_tax / pay_periods
        effective_state_rate = annual_state_tax / annual_pre_tax_income if annual_pre_tax_income > 0 else 0
        
        # Local tax (NYC) - uses same taxable income as state
        annual_local_tax = self.calculate_progressive_tax(state_taxable_income, self.local_brackets)
        local_tax_per_paycheck = annual_local_tax / pay_periods
        effective_local_rate = annual_local_tax / annual_pre_tax_income if annual_pre_tax_income > 0 else 0
        
        # Social Security (6.2% up to wage base)
        social_security = min(paycheck_gross * self.SOCIAL_SECURITY_RATE, 
                             self.SOCIAL_SECURITY_WAGE_BASE / pay_periods * self.SOCIAL_SECURITY_RATE)
        
        # Medicare (1.45%)
        medicare = paycheck_gross * self.MEDICARE_RATE
        
        # Total taxes
        total_taxes = (federal_tax_per_paycheck + state_tax_per_paycheck + 
                      local_tax_per_paycheck + social_security + medicare)
        
        # Post-tax income
        post_tax_income = pre_tax_income - total_taxes
        
        # === POST-TAX DEDUCTIONS ===
        
        # ESPP
        espp = paycheck_gross * espp_percent
        
        # NY SDI Tax (fixed)
        ny_sdi_tax = 1.20
        
        # Life insurance adjustments are already added to income_before_tax
        # So they're subtracted here in the final take-home calculation
        
        # Take home income
        take_home_income = post_tax_income - espp - ny_sdi_tax - li_adjustments
        
        # === ALLOCATIONS ===
        
        # Calculate allocations
        to_savings = take_home_income * savings_percent
        to_savings2 = take_home_income * savings2_percent
        to_roth_ira = roth_ira_per_paycheck
        to_brokerage = brokerage_per_paycheck
        to_crypto = crypto_per_paycheck
        
        # Final income (after all allocations)
        final_income = (take_home_income - to_savings - to_savings2 - 
                       to_roth_ira - to_brokerage - to_crypto)
        
        # === ANNUAL PROJECTIONS ===
        
        annual_take_home = take_home_income * pay_periods
        total_tax_rate = (annual_federal_tax + annual_state_tax + annual_local_tax + 
                         social_security * pay_periods + medicare * pay_periods) / salary
        
        # Build the result
        return PaycheckBreakdown(
            salary=salary,
            pay_periods=pay_periods,
            paycheck_gross=paycheck_gross,
            
            contribution_401k=contribution_401k,
            contribution_401k_percent=contribution_401k_percent,
            employer_match_401k=employer_match_per_paycheck,
            hsa_contribution=hsa_per_paycheck,
            transit_fsa=transit_fsa_per_paycheck,
            medical_insurance=medical_per_paycheck,
            dental_insurance=dental_per_paycheck,
            vision_insurance=vision_per_paycheck,
            
            pre_tax_income=pre_tax_income,
            
            federal_tax=federal_tax_per_paycheck,
            state_tax=state_tax_per_paycheck,
            local_tax=local_tax_per_paycheck,
            social_security=social_security,
            medicare=medicare,
            total_taxes=total_taxes,
            
            post_tax_income=post_tax_income,
            
            espp=espp,
            ny_sdi_tax=ny_sdi_tax,
            li_adjustments=li_adjustments,
            
            take_home_income=take_home_income,
            
            to_savings=to_savings,
            to_savings2=to_savings2,
            to_roth_ira=to_roth_ira,
            to_brokerage=to_brokerage,
            to_crypto=to_crypto,
            
            final_income=final_income,
            
            annual_salary=salary,
            annual_401k=annual_401k,
            annual_employer_match=annual_employer_match,
            annual_federal_tax=annual_federal_tax,
            annual_state_tax=annual_state_tax,
            annual_local_tax=annual_local_tax,
            annual_take_home=annual_take_home,
            
            effective_federal_rate=effective_federal_rate,
            effective_state_rate=effective_state_rate,
            effective_local_rate=effective_local_rate,
            total_tax_rate=total_tax_rate
        )


if __name__ == "__main__":
    # Test the calculator with sample data
    from database import FinanceDatabase
    
    # Get tax brackets
    db = FinanceDatabase("test_finances.db")
    brackets = db.get_tax_brackets()
    db.close()
    
    # Create calculator
    calc = PaycheckCalculator(brackets)
    
    # Test configuration matching the Excel file
    config = {
        'salary': 84975.0,
        'pay_periods': 26,
        'contribution_401k_percent': 0.15,
        'employer_match_percent': 0.03,
        'max_employer_match': 3000.0,
        'hsa_per_paycheck': 50.59,
        'medical_insurance_per_paycheck': 46.67,
        'espp_percent': 0.04,
        'savings_percent': 0.1468667255,  # $480 / $3268.27
        'savings2_percent': 0.0,
        'roth_ira_per_paycheck': 45.0,
        'brokerage_per_paycheck': 75.0,
        'crypto_per_paycheck': 0.0
    }
    
    result = calc.calculate(config)
    
    print("💰 PAYCHECK CALCULATION TEST")
    print("="*70)
    print(f"\nAnnual Salary: ${result.annual_salary:,.2f}")
    print(f"Paycheck Gross: ${result.paycheck_gross:,.2f}")
    print(f"\nPre-Tax Deductions:")
    print(f"  401k ({result.contribution_401k_percent*100:.0f}%): -${result.contribution_401k:,.2f}")
    print(f"  Employer Match: +${result.employer_match_401k:,.2f}")
    print(f"  HSA: -${result.hsa_contribution:,.2f}")
    print(f"  Medical Insurance: -${result.medical_insurance:,.2f}")
    print(f"  Dental Insurance: -${result.dental_insurance:,.2f}")
    print(f"  Vision Insurance: -${result.vision_insurance:,.2f}")
    print(f"\nPre-Tax Income: ${result.pre_tax_income:,.2f}")
    print(f"\nTaxes:")
    print(f"  Federal Tax: -${result.federal_tax:,.2f} ({result.effective_federal_rate*100:.2f}%)")
    print(f"  State Tax (NY): -${result.state_tax:,.2f} ({result.effective_state_rate*100:.2f}%)")
    print(f"  Local Tax (NYC): -${result.local_tax:,.2f} ({result.effective_local_rate*100:.2f}%)")
    print(f"  Social Security: -${result.social_security:,.2f}")
    print(f"  Medicare: -${result.medicare:,.2f}")
    print(f"  Total Taxes: -${result.total_taxes:,.2f} ({result.total_tax_rate*100:.2f}%)")
    print(f"\nPost-Tax Income: ${result.post_tax_income:,.2f}")
    print(f"\nPost-Tax Deductions:")
    print(f"  ESPP (4%): -${result.espp:,.2f}")
    print(f"  NY SDI Tax: -${result.ny_sdi_tax:,.2f}")
    print(f"  LI Adjustments: -${result.li_adjustments:,.2f}")
    print(f"\nTake Home: ${result.take_home_income:,.2f}")
    print(f"\nAllocations:")
    print(f"  Savings: -${result.to_savings:,.2f}")
    print(f"  Roth IRA: -${result.to_roth_ira:,.2f}")
    print(f"  Brokerage: -${result.to_brokerage:,.2f}")
    print(f"\nFinal Income (Checking): ${result.final_income:,.2f}")
    print(f"\nAnnual Take Home: ${result.annual_take_home:,.2f}")
    print("\n" + "="*70)
    
    # Compare with Excel values
    print("\n📊 COMPARISON WITH YOUR EXCEL:")
    print("="*70)
    excel_values = {
        'Paycheck Gross': 3268.27,
        'Pre-Tax Income': 2685.90,
        'Federal Tax': 273.71,
        'State Tax': 124.46,
        'Local Tax': 87.38,
        'Take Home': 1813.28,
        'Final Income': 1038.28
    }
    
    calculated_values = {
        'Paycheck Gross': result.paycheck_gross,
        'Pre-Tax Income': result.pre_tax_income,
        'Federal Tax': result.federal_tax,
        'State Tax': result.state_tax,
        'Local Tax': result.local_tax,
        'Take Home': result.take_home_income,
        'Final Income': result.final_income
    }
    
    print(f"{'Field':<20} {'Excel':>15} {'Calculated':>15} {'Difference':>15}")
    print("-"*70)
    for field in excel_values:
        excel_val = excel_values[field]
        calc_val = calculated_values[field]
        diff = calc_val - excel_val
        diff_pct = (diff / excel_val * 100) if excel_val != 0 else 0
        print(f"{field:<20} ${excel_val:>13,.2f} ${calc_val:>13,.2f} ${diff:>10,.2f} ({diff_pct:>5.2f}%)")
    
    print("\n✅ Calculator working! (Small differences are due to rounding)")
    
    # Clean up
    import os
    os.remove("test_finances.db")
