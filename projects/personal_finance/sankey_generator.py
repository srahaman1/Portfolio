"""
Sankey Diagram Generator for Cash Flow Visualization
Creates interactive Plotly Sankey diagrams showing money flow
"""

import plotly.graph_objects as go
from paycheck_calculator import PaycheckBreakdown
from typing import Optional
import webbrowser
import os


class SankeyGenerator:
    """Generate Sankey diagrams for paycheck cash flow"""
    
    # Color scheme
    COLORS = {
        'income': '#4CAF50',        # Green
        'pre_tax': '#2196F3',       # Blue
        '401k': '#9C27B0',          # Purple
        'insurance': '#FF9800',     # Orange
        'taxes': '#F44336',         # Red
        'federal_tax': '#D32F2F',   # Dark red
        'state_tax': '#E57373',     # Light red
        'local_tax': '#FFCDD2',     # Very light red
        'post_tax': '#00BCD4',      # Cyan
        'allocations': '#8BC34A',   # Light green
        'final': '#CDDC39',         # Lime
    }
    
    def generate(self, breakdown: PaycheckBreakdown, title: str = "Paycheck Cash Flow") -> go.Figure:
        """
        Generate a Sankey diagram from paycheck breakdown
        
        Args:
            breakdown: PaycheckBreakdown object with calculation results
            title: Title for the diagram
            
        Returns:
            Plotly figure object
        """
        # Node labels
        labels = [
            "Gross Pay",                    # 0
            "Pre-Tax Deductions",          # 1
            "401(k)",                      # 2
            "Employer Match",              # 3
            "HSA",                         # 4
            "Insurance",                   # 5
            "Pre-Tax Income",              # 6
            "Taxes",                       # 7
            "Federal Tax",                 # 8
            "State Tax",                   # 9
            "Local Tax",                   # 10
            "Payroll Taxes",               # 11
            "Post-Tax Income",             # 12
            "Post-Tax Deductions",         # 13
            "ESPP",                        # 14
            "Take Home",                   # 15
            "Allocations",                 # 16
            "Savings",                     # 17
            "Roth IRA",                    # 18
            "Brokerage",                   # 19
            "Final Income",                # 20
        ]
        
        # Build the flows (source, target, value)
        sources = []
        targets = []
        values = []
        colors = []
        
        # Flow 1: Gross Pay → Pre-Tax Deductions (total pre-tax)
        total_pre_tax_deductions = (breakdown.contribution_401k + 
                                    breakdown.hsa_contribution + 
                                    breakdown.medical_insurance)
        if total_pre_tax_deductions > 0:
            sources.append(0)  # Gross Pay
            targets.append(1)  # Pre-Tax Deductions
            values.append(total_pre_tax_deductions)
            colors.append('rgba(33, 150, 243, 0.4)')  # Blue
        
        # Flow 2: Pre-Tax Deductions → 401(k)
        if breakdown.contribution_401k > 0:
            sources.append(1)  # Pre-Tax Deductions
            targets.append(2)  # 401(k)
            values.append(breakdown.contribution_401k)
            colors.append('rgba(156, 39, 176, 0.6)')  # Purple
        
        # Flow 3: Employer Match (separate source)
        if breakdown.employer_match_401k > 0:
            sources.append(3)  # Employer Match
            targets.append(2)  # 401(k)
            values.append(breakdown.employer_match_401k)
            colors.append('rgba(156, 39, 176, 0.3)')  # Light purple
        
        # Flow 4: Pre-Tax Deductions → HSA
        if breakdown.hsa_contribution > 0:
            sources.append(1)  # Pre-Tax Deductions
            targets.append(4)  # HSA
            values.append(breakdown.hsa_contribution)
            colors.append('rgba(255, 152, 0, 0.6)')  # Orange
        
        # Flow 5: Pre-Tax Deductions → Insurance
        total_insurance = breakdown.medical_insurance
        if total_insurance > 0:
            sources.append(1)  # Pre-Tax Deductions
            targets.append(5)  # Insurance
            values.append(total_insurance)
            colors.append('rgba(255, 152, 0, 0.6)')  # Orange
        
        # Flow 6: Gross Pay → Pre-Tax Income
        sources.append(0)  # Gross Pay
        targets.append(6)  # Pre-Tax Income
        values.append(breakdown.pre_tax_income)
        colors.append('rgba(76, 175, 80, 0.4)')  # Green
        
        # Flow 7: Pre-Tax Income → Taxes (total)
        sources.append(6)  # Pre-Tax Income
        targets.append(7)  # Taxes
        values.append(breakdown.total_taxes)
        colors.append('rgba(244, 67, 54, 0.4)')  # Red
        
        # Flow 8: Taxes → Federal Tax
        sources.append(7)  # Taxes
        targets.append(8)  # Federal Tax
        values.append(breakdown.federal_tax)
        colors.append('rgba(211, 47, 47, 0.8)')  # Dark red
        
        # Flow 9: Taxes → State Tax
        sources.append(7)  # Taxes
        targets.append(9)  # State Tax
        values.append(breakdown.state_tax)
        colors.append('rgba(229, 115, 115, 0.8)')  # Light red
        
        # Flow 10: Taxes → Local Tax
        sources.append(7)  # Taxes
        targets.append(10)  # Local Tax
        values.append(breakdown.local_tax)
        colors.append('rgba(255, 205, 210, 0.8)')  # Very light red
        
        # Flow 11: Taxes → Payroll Taxes (SS + Medicare)
        payroll_taxes = breakdown.social_security + breakdown.medicare
        sources.append(7)  # Taxes
        targets.append(11)  # Payroll Taxes
        values.append(payroll_taxes)
        colors.append('rgba(229, 115, 115, 0.6)')
        
        # Flow 12: Pre-Tax Income → Post-Tax Income
        sources.append(6)  # Pre-Tax Income
        targets.append(12)  # Post-Tax Income
        values.append(breakdown.post_tax_income)
        colors.append('rgba(0, 188, 212, 0.4)')  # Cyan
        
        # Flow 13: Post-Tax Income → Post-Tax Deductions
        total_post_tax = breakdown.espp + breakdown.ny_sdi_tax + breakdown.li_adjustments
        if total_post_tax > 0:
            sources.append(12)  # Post-Tax Income
            targets.append(13)  # Post-Tax Deductions
            values.append(total_post_tax)
            colors.append('rgba(255, 152, 0, 0.4)')
        
        # Flow 14: Post-Tax Deductions → ESPP
        if breakdown.espp > 0:
            sources.append(13)  # Post-Tax Deductions
            targets.append(14)  # ESPP
            values.append(breakdown.espp)
            colors.append('rgba(156, 39, 176, 0.6)')
        
        # Flow 15: Post-Tax Income → Take Home
        sources.append(12)  # Post-Tax Income
        targets.append(15)  # Take Home
        values.append(breakdown.take_home_income)
        colors.append('rgba(139, 195, 74, 0.4)')  # Light green
        
        # Flow 16: Take Home → Allocations
        total_allocations = (breakdown.to_savings + breakdown.to_savings2 + 
                           breakdown.to_roth_ira + breakdown.to_brokerage + 
                           breakdown.to_crypto)
        if total_allocations > 0:
            sources.append(15)  # Take Home
            targets.append(16)  # Allocations
            values.append(total_allocations)
            colors.append('rgba(139, 195, 74, 0.6)')
        
        # Flow 17-20: Allocations to specific accounts
        if breakdown.to_savings + breakdown.to_savings2 > 0:
            sources.append(16)  # Allocations
            targets.append(17)  # Savings
            values.append(breakdown.to_savings + breakdown.to_savings2)
            colors.append('rgba(205, 220, 57, 0.8)')
        
        if breakdown.to_roth_ira > 0:
            sources.append(16)  # Allocations
            targets.append(18)  # Roth IRA
            values.append(breakdown.to_roth_ira)
            colors.append('rgba(156, 39, 176, 0.6)')
        
        if breakdown.to_brokerage > 0:
            sources.append(16)  # Allocations
            targets.append(19)  # Brokerage
            values.append(breakdown.to_brokerage)
            colors.append('rgba(33, 150, 243, 0.6)')
        
        # Flow 21: Take Home → Final Income
        sources.append(15)  # Take Home
        targets.append(20)  # Final Income
        values.append(breakdown.final_income)
        colors.append('rgba(205, 220, 57, 0.6)')  # Lime
        
        # Create the Sankey diagram
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=labels,
                color=[
                    self.COLORS['income'],      # 0: Gross Pay
                    self.COLORS['pre_tax'],     # 1: Pre-Tax Deductions
                    self.COLORS['401k'],        # 2: 401(k)
                    self.COLORS['401k'],        # 3: Employer Match
                    self.COLORS['insurance'],   # 4: HSA
                    self.COLORS['insurance'],   # 5: Insurance
                    self.COLORS['income'],      # 6: Pre-Tax Income
                    self.COLORS['taxes'],       # 7: Taxes
                    self.COLORS['federal_tax'], # 8: Federal Tax
                    self.COLORS['state_tax'],   # 9: State Tax
                    self.COLORS['local_tax'],   # 10: Local Tax
                    self.COLORS['state_tax'],   # 11: Payroll Taxes
                    self.COLORS['post_tax'],    # 12: Post-Tax Income
                    self.COLORS['insurance'],   # 13: Post-Tax Deductions
                    self.COLORS['401k'],        # 14: ESPP
                    self.COLORS['allocations'], # 15: Take Home
                    self.COLORS['allocations'], # 16: Allocations
                    self.COLORS['final'],       # 17: Savings
                    self.COLORS['401k'],        # 18: Roth IRA
                    self.COLORS['pre_tax'],     # 19: Brokerage
                    self.COLORS['final'],       # 20: Final Income
                ]
            ),
            link=dict(
                source=sources,
                target=targets,
                value=values,
                color=colors
            )
        )])
        
        fig.update_layout(
            title={
                'text': title,
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24, 'family': 'Arial, sans-serif'}
            },
            font=dict(size=12, family='Arial, sans-serif'),
            height=800,
            width=1400,
            paper_bgcolor='white',
            plot_bgcolor='white'
        )
        
        return fig
    
    def save_html(self, fig: go.Figure, filename: str = "cash_flow.html") -> str:
        """
        Save Sankey diagram as interactive HTML file
        
        Args:
            fig: Plotly figure
            filename: Output filename
            
        Returns:
            Path to saved file
        """
        fig.write_html(filename)
        return os.path.abspath(filename)
    
    def show(self, fig: go.Figure):
        """Display Sankey diagram in default browser"""
        temp_file = "temp_sankey.html"
        filepath = self.save_html(fig, temp_file)
        webbrowser.open(f'file://{filepath}')


if __name__ == "__main__":
    # Test with sample data
    from database import FinanceDatabase
    from paycheck_calculator import PaycheckCalculator
    
    # Get tax brackets
    db = FinanceDatabase("test_finances.db")
    brackets = db.get_tax_brackets()
    db.close()
    
    # Create calculator
    calc = PaycheckCalculator(brackets)
    
    # Test configuration
    config = {
        'salary': 84975.0,
        'pay_periods': 26,
        'contribution_401k_percent': 0.15,
        'employer_match_percent': 0.03,
        'max_employer_match': 3000.0,
        'hsa_per_paycheck': 50.59,
        'medical_insurance_per_paycheck': 46.67,
        'dental_premium_annual': 130.52,
        'vision_premium_annual': 124.28,
        'espp_percent': 0.04,
        'standard_deduction_federal': 15000.0,
        'standard_deduction_state': 8000.0,
        'savings_percent': 480.0 / 1813.28,
        'savings2_percent': 175.0 / 1813.28,
        'roth_ira_per_paycheck': 45.0,
        'brokerage_per_paycheck': 75.0,
        'crypto_per_paycheck': 0.0
    }
    
    result = calc.calculate(config)
    
    # Generate Sankey diagram
    sankey = SankeyGenerator()
    fig = sankey.generate(result, title="Paycheck Cash Flow - $84,975 Annual Salary")
    
    # Save and display
    filepath = sankey.save_html(fig, "/mnt/user-data/outputs/finance-app/sample_sankey.html")
    print(f"✅ Sankey diagram saved to: {filepath}")
    print("\n💡 Opening in browser...")
    
    # Clean up test database
    import os
    if os.path.exists("test_finances.db"):
        os.remove("test_finances.db")
