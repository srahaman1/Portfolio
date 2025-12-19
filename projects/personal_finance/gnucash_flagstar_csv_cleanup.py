import pandas as pd

def transform_csv_for_gnucash(input_file, output_file):
    """
    Transform CSV file for GnuCash import by adding an accounts column
    based on transaction descriptions.
    """
    # Read the CSV file
    df = pd.read_csv(input_file)
    
    # Select the required columns
    final = df[['Date', 'Description', 'Debit', 'Credit']].copy()
    
    # Merge Credit and Debit columns using coalesce logic
    # Fill NaN values with 0 first, then combine
    final['Amount'] = final['Debit'].fillna(0) + final['Credit'].fillna(0)
    
    # Alternative method that preserves the original values better:
    # final['Amount'] = final['Debit'].combine_first(final['Credit'])
    
    # Drop the original Credit and Debit columns
    final = final.drop(['Debit', 'Credit'], axis=1)
    
    # Function to determine account based on description
    def get_account(description):
        # Convert to string and make case-insensitive
        desc = str(description).upper()
        
        # Check conditions in order (most specific first)
        
        if "WITHDRAWAL" in desc and "CHASE" in desc:
            return "Liabilities:Credit Card"
        elif "WITHDRAWAL" in desc and "VERIZON" in desc:
            return "Expenses:Cable"
        elif "WITHDRAWAL" in desc and "GOLDMAN SACHS" in desc:
            return "Assets:Current Assets:Goldman Sachs"
        elif "WITHDRAWAL" in desc and "TRANSFER TO" in desc and "9432 SAV" in desc:
            return "Assets:Current Assets:Savings Account"
        elif "WITHDRAWAL" in desc and "TRANSFER TO" in desc and "7153 CK" in desc:
            return "Assets:Current Assets:Checking Account"
        elif "WITHDRAWAL" in desc and "FID" in desc:
            return "Assets:Investment:Fidelity ROTH"
        elif "WITHDRAWAL" in desc and "1ST BANKCARD" in desc:
            return "Liabilities:Credit Card"
        elif "WITHDRAWAL" in desc and "CUNY" in desc:
            return "Expenses:Education"
        elif "WITHDRAWAL" in desc and "COINBASE" in desc:
            return "Assets:Investment:Cryptocurrency"
        
        # Specific deposit patterns (most specific first)
        elif "DEPOSIT" in desc and "RAPID7" in desc:
            return "Income:Salary"
        elif "DEPOSIT" in desc and "ANCIL" in desc:
            return "Income:Rental Income"
        elif "DEPOSIT" in desc and "TRANSFER FROM" in desc and "9432 SAV" in desc:
            return "Assets:Current Assets:Checking Account"
        elif "DEPOSIT" in desc and "NYSTAXRFD" in desc:
            return "Expenses:Taxes:State/Province"
        elif "DEPOSIT" in desc and "IRS" in desc and "TAX REFUND" in desc:
            return "Expenses:Taxes:Federal"
        elif desc == "WITHDRAWAL":
            return "Assets:Current Assets:Checking Account"
        elif desc == "DEPOSIT":
            return "Assets:Current Assets:Cash in Wallet"
        # Savings
        elif "INTEREST" in desc:
            return "Income:Interest Income:Savings Interest"
        elif "DEPOSIT" in desc and "TRANSFER FROM" in desc and "7153 CK" in desc:
            return "Assets:Current Assets:Savings Account"
        else:
            return "Imbalance-USD"  # Default category for unmatched descriptions
    
    # Apply the transformation to create the accounts column
    final['Accounts'] = final['Description'].apply(get_account)
    
    # Reorder columns to put Accounts at the end
    final = final[['Date', 'Description', 'Amount', 'Accounts']]
    
    # Save to new CSV file
    final.to_csv(output_file, index=False)
    
    return final

# Usage example
if __name__ == "__main__":
    # Transform the file
    input_file = "C:/Users/Graduate/Downloads/export (2).csv"
    output_file = "C:/Users/Graduate/Downloads/export_transformed.csv"
    
    result_df = transform_csv_for_gnucash(input_file, output_file)
    
    # Display summary
    print(f"Transformation complete! File saved to: {output_file}")
    print(f"Total transactions: {len(result_df)}")
    print("\nAccount distribution:")
    print(result_df['Accounts'].value_counts())
    
    # Show first few rows
    print("\nFirst 10 rows of transformed data:")
    print(result_df.head(25))