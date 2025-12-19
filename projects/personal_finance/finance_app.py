"""
Personal Finance Calculator - Desktop Application
Modern GUI with paycheck calculator and Sankey visualization
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog
import webbrowser
import os
from datetime import datetime
from database import FinanceDatabase
from paycheck_calculator import PaycheckCalculator
from sankey_generator import SankeyGenerator


class FinanceApp(ctk.CTk):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("Personal Finance Calculator")
        self.geometry("1200x800")
        
        # Set theme
        ctk.set_appearance_mode("dark")  # "dark", "light", or "system"
        ctk.set_default_color_theme("blue")
        
        # Initialize database and calculator
        self.db = FinanceDatabase("finances.db")
        brackets = self.db.get_tax_brackets()
        self.calculator = PaycheckCalculator(brackets)
        self.sankey = SankeyGenerator()
        
        # Current calculation result
        self.current_result = None
        
        # Create UI
        self.create_widgets()
        
        # Load saved configuration if exists
        self.load_configuration()
    
    def create_widgets(self):
        """Create all UI widgets"""
        
        # Create main container with grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)
        
        # Left panel - Input form
        self.create_input_panel()
        
        # Right panel - Results display
        self.create_results_panel()
    
    def create_input_panel(self):
        """Create the input form panel"""
        
        input_frame = ctk.CTkScrollableFrame(self, corner_radius=10)
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Title
        title = ctk.CTkLabel(
            input_frame, 
            text="💰 Paycheck Calculator",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(pady=10)
        
        # --- BASIC INFO SECTION ---
        self.create_section_header(input_frame, "Basic Information")
        
        self.salary_var = ctk.StringVar(value="84975")
        self.create_input_field(input_frame, "Annual Salary ($):", self.salary_var)
        
        self.pay_periods_var = ctk.StringVar(value="26")
        self.create_input_field(input_frame, "Pay Periods per Year:", self.pay_periods_var)
        
        # --- 401K SECTION ---
        self.create_section_header(input_frame, "401(k) Contributions")
        
        self.k401_percent_var = ctk.StringVar(value="15")
        self.create_input_field(input_frame, "401(k) Contribution (%):", self.k401_percent_var)
        
        self.employer_match_var = ctk.StringVar(value="3")
        self.create_input_field(input_frame, "Employer Match (%):", self.employer_match_var)
        
        self.employer_max_var = ctk.StringVar(value="3000")
        self.create_input_field(input_frame, "Max Employer Match ($):", self.employer_max_var)
        
        # --- HEALTH SAVINGS SECTION ---
        self.create_section_header(input_frame, "Health & Insurance")
        
        self.hsa_var = ctk.StringVar(value="50.59")
        self.create_input_field(input_frame, "HSA per Paycheck ($):", self.hsa_var)
        
        self.medical_var = ctk.StringVar(value="46.67")
        self.create_input_field(input_frame, "Medical Insurance ($):", self.medical_var)
        
        self.dental_var = ctk.StringVar(value="130.52")
        self.create_input_field(input_frame, "Dental (Annual $):", self.dental_var)
        
        self.vision_var = ctk.StringVar(value="124.28")
        self.create_input_field(input_frame, "Vision (Annual $):", self.vision_var)
        
        # --- ESPP SECTION ---
        self.create_section_header(input_frame, "Stock Purchase")
        
        self.espp_var = ctk.StringVar(value="4")
        self.create_input_field(input_frame, "ESPP Contribution (%):", self.espp_var)
        
        # --- ALLOCATIONS SECTION ---
        self.create_section_header(input_frame, "Savings Allocations")
        
        self.savings_var = ctk.StringVar(value="480")
        self.create_input_field(input_frame, "To Savings ($):", self.savings_var)
        
        self.roth_var = ctk.StringVar(value="45")
        self.create_input_field(input_frame, "To Roth IRA ($):", self.roth_var)
        
        self.brokerage_var = ctk.StringVar(value="75")
        self.create_input_field(input_frame, "To Brokerage ($):", self.brokerage_var)
        
        # --- BUTTONS ---
        button_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        button_frame.pack(pady=20, fill="x")
        
        calc_button = ctk.CTkButton(
            button_frame,
            text="Calculate",
            command=self.calculate,
            font=ctk.CTkFont(size=16, weight="bold"),
            height=40
        )
        calc_button.pack(pady=5, fill="x")
        
        save_button = ctk.CTkButton(
            button_frame,
            text="Save Configuration",
            command=self.save_configuration,
            fg_color="green",
            hover_color="darkgreen"
        )
        save_button.pack(pady=5, fill="x")
    
    def create_results_panel(self):
        """Create the results display panel"""
        
        results_frame = ctk.CTkFrame(self, corner_radius=10)
        results_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        # Title
        title = ctk.CTkLabel(
            results_frame,
            text="📊 Paycheck Breakdown",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(pady=10)
        
        # Scrollable results area
        self.results_text = ctk.CTkTextbox(
            results_frame,
            font=ctk.CTkFont(family="Courier New", size=12),
            wrap="none"
        )
        self.results_text.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Initial message
        self.results_text.insert("1.0", "Enter your information and click 'Calculate' to see results...")
        self.results_text.configure(state="disabled")
        
        # Sankey button
        self.sankey_button = ctk.CTkButton(
            results_frame,
            text="📈 View Cash Flow Diagram",
            command=self.show_sankey,
            font=ctk.CTkFont(size=16, weight="bold"),
            height=40,
            state="disabled"
        )
        self.sankey_button.pack(pady=10, padx=10, fill="x")
    
    def create_section_header(self, parent, text):
        """Create a section header"""
        header = ctk.CTkLabel(
            parent,
            text=text,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        header.pack(pady=(15, 5))
        
        separator = ctk.CTkFrame(parent, height=2, fg_color="gray")
        separator.pack(fill="x", padx=20, pady=5)
    
    def create_input_field(self, parent, label_text, variable):
        """Create a labeled input field"""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(pady=5, padx=20, fill="x")
        
        label = ctk.CTkLabel(frame, text=label_text, width=200, anchor="w")
        label.pack(side="left", padx=(0, 10))
        
        entry = ctk.CTkEntry(frame, textvariable=variable, width=150)
        entry.pack(side="right")
    
    def calculate(self):
        """Perform paycheck calculation"""
        try:
            # Get values from form
            config = {
                'salary': float(self.salary_var.get()),
                'pay_periods': int(self.pay_periods_var.get()),
                'contribution_401k_percent': float(self.k401_percent_var.get()) / 100,
                'employer_match_percent': float(self.employer_match_var.get()) / 100,
                'max_employer_match': float(self.employer_max_var.get()),
                'hsa_per_paycheck': float(self.hsa_var.get()),
                'medical_insurance_per_paycheck': float(self.medical_var.get()),
                'dental_premium_annual': float(self.dental_var.get()),
                'vision_premium_annual': float(self.vision_var.get()),
                'espp_percent': float(self.espp_var.get()) / 100,
                'standard_deduction_federal': 15000.0,
                'standard_deduction_state': 8000.0,
                'roth_ira_per_paycheck': float(self.roth_var.get()),
                'brokerage_per_paycheck': float(self.brokerage_var.get()),
                'crypto_per_paycheck': 0.0
            }
            
            # Calculate savings as percentage of take-home
            # We need to do a preliminary calculation first
            temp_result = self.calculator.calculate(config)
            config['savings_percent'] = float(self.savings_var.get()) / temp_result.take_home_income
            config['savings2_percent'] = 0.0
            
            # Calculate with correct savings percentage
            self.current_result = self.calculator.calculate(config)
            
            # Display results
            self.display_results(self.current_result)
            
            # Enable Sankey button
            self.sankey_button.configure(state="normal")
            
        except ValueError as e:
            messagebox.showerror("Input Error", f"Please enter valid numbers in all fields.\n\nError: {str(e)}")
        except Exception as e:
            messagebox.showerror("Calculation Error", f"An error occurred: {str(e)}")
    
    def display_results(self, result):
        """Display calculation results"""
        
        output = []
        output.append("═" * 80)
        output.append("💰 PAYCHECK BREAKDOWN")
        output.append("═" * 80)
        output.append("")
        
        # Income section
        output.append("📊 INCOME")
        output.append(f"   Annual Salary:            ${result.annual_salary:>15,.2f}")
        output.append(f"   Pay Periods:              {result.pay_periods:>15}")
        output.append(f"   Paycheck Gross:           ${result.paycheck_gross:>15,.2f}")
        output.append("")
        
        # Pre-tax deductions
        output.append("📉 PRE-TAX DEDUCTIONS")
        output.append(f"   401(k) ({result.contribution_401k_percent*100:.0f}%):            -${result.contribution_401k:>15,.2f}")
        output.append(f"   Employer Match:           +${result.employer_match_401k:>15,.2f}")
        output.append(f"   HSA:                      -${result.hsa_contribution:>15,.2f}")
        output.append(f"   Medical Insurance:        -${result.medical_insurance:>15,.2f}")
        output.append(f"   Dental Insurance:         -${result.dental_insurance:>15,.2f}")
        output.append(f"   Vision Insurance:         -${result.vision_insurance:>15,.2f}")
        output.append(f"   {'-' * 40}")
        output.append(f"   Pre-Tax Income:           ${result.pre_tax_income:>15,.2f}")
        output.append("")
        
        # Taxes
        output.append("💸 TAXES")
        output.append(f"   Federal Tax:              -${result.federal_tax:>15,.2f}  ({result.effective_federal_rate*100:>5.2f}%)")
        output.append(f"   State Tax (NY):           -${result.state_tax:>15,.2f}  ({result.effective_state_rate*100:>5.2f}%)")
        output.append(f"   Local Tax (NYC):          -${result.local_tax:>15,.2f}  ({result.effective_local_rate*100:>5.2f}%)")
        output.append(f"   Social Security:          -${result.social_security:>15,.2f}")
        output.append(f"   Medicare:                 -${result.medicare:>15,.2f}")
        output.append(f"   {'-' * 40}")
        output.append(f"   Total Taxes:              -${result.total_taxes:>15,.2f}  ({result.total_tax_rate*100:>5.2f}%)")
        output.append("")
        
        # Post-tax income
        output.append("💵 POST-TAX INCOME")
        output.append(f"   After Taxes:              ${result.post_tax_income:>15,.2f}")
        output.append("")
        
        # Post-tax deductions
        output.append("📤 POST-TAX DEDUCTIONS")
        output.append(f"   ESPP:                     -${result.espp:>15,.2f}")
        output.append(f"   NY SDI Tax:               -${result.ny_sdi_tax:>15,.2f}")
        output.append(f"   Life Insurance Adj:       -${result.li_adjustments:>15,.2f}")
        output.append(f"   {'-' * 40}")
        output.append(f"   Take Home:                ${result.take_home_income:>15,.2f}")
        output.append("")
        
        # Allocations
        output.append("🎯 ALLOCATIONS")
        if result.to_savings > 0:
            output.append(f"   To Savings:               -${result.to_savings:>15,.2f}")
        if result.to_roth_ira > 0:
            output.append(f"   To Roth IRA:              -${result.to_roth_ira:>15,.2f}")
        if result.to_brokerage > 0:
            output.append(f"   To Brokerage:             -${result.to_brokerage:>15,.2f}")
        output.append(f"   {'-' * 40}")
        output.append(f"   Final Income (Checking):  ${result.final_income:>15,.2f}")
        output.append("")
        
        # Annual summary
        output.append("📅 ANNUAL SUMMARY")
        output.append(f"   Annual 401(k):            ${result.annual_401k:>15,.2f}")
        output.append(f"   Annual Employer Match:    ${result.annual_employer_match:>15,.2f}")
        output.append(f"   Annual Federal Tax:       ${result.annual_federal_tax:>15,.2f}")
        output.append(f"   Annual State Tax:         ${result.annual_state_tax:>15,.2f}")
        output.append(f"   Annual Local Tax:         ${result.annual_local_tax:>15,.2f}")
        output.append(f"   Annual Take Home:         ${result.annual_take_home:>15,.2f}")
        output.append("")
        output.append("═" * 80)
        
        # Update text widget
        self.results_text.configure(state="normal")
        self.results_text.delete("1.0", "end")
        self.results_text.insert("1.0", "\n".join(output))
        self.results_text.configure(state="disabled")
    
    def show_sankey(self):
        """Generate and show Sankey diagram"""
        if self.current_result is None:
            messagebox.showwarning("No Results", "Please calculate first before viewing the diagram.")
            return
        
        try:
            # Generate Sankey diagram
            fig = self.sankey.generate(
                self.current_result,
                title=f"Cash Flow - ${self.current_result.annual_salary:,.0f} Annual Salary"
            )
            
            # Save to temp file
            filepath = self.sankey.save_html(fig, "cash_flow_diagram.html")
            
            # Open in browser
            webbrowser.open(f'file://{filepath}')
            
        except Exception as e:
            messagebox.showerror("Visualization Error", f"Failed to generate diagram: {str(e)}")
    
    def save_configuration(self):
        """Save current configuration to database"""
        try:
            config_name = f"Config_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            config = {
                'name': config_name,
                'salary': float(self.salary_var.get()),
                'pay_periods': int(self.pay_periods_var.get()),
                'contribution_401k_percent': float(self.k401_percent_var.get()) / 100,
                'employer_match_percent': float(self.employer_match_var.get()) / 100,
                'max_employer_match': float(self.employer_max_var.get()),
                'hsa_per_paycheck': float(self.hsa_var.get()),
                'medical_insurance_per_paycheck': float(self.medical_var.get()),
                'dental_premium_annual': float(self.dental_var.get()),
                'vision_premium_annual': float(self.vision_var.get()),
                'espp_percent': float(self.espp_var.get()) / 100,
                'roth_ira_per_paycheck': float(self.roth_var.get()),
                'brokerage_per_paycheck': float(self.brokerage_var.get()),
            }
            
            config_id = self.db.save_paycheck_config(config)
            messagebox.showinfo("Success", f"Configuration saved as '{config_name}'")
            
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save configuration: {str(e)}")
    
    def load_configuration(self):
        """Load the most recent configuration from database"""
        try:
            config = self.db.get_active_paycheck_config()
            if config:
                self.salary_var.set(str(config['salary']))
                self.pay_periods_var.set(str(config['pay_periods']))
                self.k401_percent_var.set(str(config['contribution_401k_percent'] * 100))
                self.employer_match_var.set(str(config['employer_match_percent'] * 100))
                self.employer_max_var.set(str(config['max_employer_match']))
                self.hsa_var.set(str(config['hsa_per_paycheck']))
                self.medical_var.set(str(config['medical_insurance_per_paycheck']))
                self.dental_var.set(str(config['dental_premium_annual']))
                self.vision_var.set(str(config['vision_premium_annual']))
                self.espp_var.set(str(config['espp_percent'] * 100))
                self.roth_var.set(str(config['roth_ira_per_paycheck']))
                self.brokerage_var.set(str(config['brokerage_per_paycheck']))
        except:
            pass  # No saved config, use defaults
    
    def on_closing(self):
        """Handle window closing"""
        self.db.close()
        self.destroy()


def main():
    """Main entry point"""
    app = FinanceApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()


if __name__ == "__main__":
    main()
