import pandas as pd
import os
from pathlib import Path

def aggregate_credit_card_csvs(input_folder, file_list, output_file, credit_card_provider="FirstBank"):
    """
    Aggregate multiple monthly credit card CSV files into a single yearly overview.
    Checks for existing aggregate file and only appends new/unique transactions.
    
    Args:
        input_folder (str): Path to folder containing CSV files
        file_list (list): List of CSV filenames to process
        output_file (str): Path for the output aggregated CSV file
        credit_card_provider (str): Credit card provider ("FirstBank" or "Chase")
    
    Returns:
        pandas.DataFrame: The aggregated data
    """
    
    # Define column configurations for different providers
    provider_config = {
        "FirstBank": {
            "has_headers": False,
            "columns_to_use": [0, 1, 2],  # All columns: Date, Amount, Description
            "column_names": ['Date', 'Amount', 'Description']  # Fixed order to match actual file structure
        },
        "Chase": {
            "has_headers": True,
            "columns_to_use": [0, 2, 5],  # Transaction Date, Description, Amount
            "column_names": ['Date', 'Description', 'Amount']
        }
    }
    
    # Validate credit card provider
    if credit_card_provider not in provider_config:
        raise ValueError(f"Unsupported credit card provider: {credit_card_provider}. "
                        f"Supported providers: {list(provider_config.keys())}")
    
    config = provider_config[credit_card_provider]
    print(f"Processing {credit_card_provider} credit card statements...")
    
    # Check if aggregate file already exists
    if os.path.exists(output_file):
        print(f"Found existing aggregate file: {output_file}")
        print("Loading existing data...")
        aggregated_df = pd.read_csv(output_file)
        
        # Standardize existing dates to mm/dd/yyyy format
        aggregated_df['Date'] = pd.to_datetime(aggregated_df['Date'], errors='coerce').dt.strftime('%m/%d/%Y')
        
        # Convert Amount to numeric if it isn't already
        aggregated_df['Amount'] = pd.to_numeric(aggregated_df['Amount'].astype(str).str.replace(r'[\$,]', '', regex=True), errors='coerce')
        
        # Remove rows with invalid dates or amounts
        aggregated_df = aggregated_df.dropna(subset=['Date', 'Amount'])
        
        print(f"Existing data contains {len(aggregated_df)} transactions")
        
        # Create a set of tuples for fast duplicate checking
        # Using (Date, Amount, Description) as unique identifier
        existing_transactions = set(
            zip(aggregated_df['Date'].astype(str), 
                aggregated_df['Amount'].astype(str), 
                aggregated_df['Description'].astype(str))
        )
        print(f"Created lookup set with {len(existing_transactions)} unique transactions")
    else:
        print(f"No existing aggregate file found. Creating new file: {output_file}")
        # Create empty DataFrame with required headers
        aggregated_df = pd.DataFrame(columns=['Date', 'Amount', 'Description'])
        existing_transactions = set()
    
    print(f"\nStarting processing of {len(file_list)} files...")
    
    total_new_transactions = 0
    total_skipped_transactions = 0
    
    for i, filename in enumerate(file_list, 1):
        # Handle both full paths and relative filenames
        if os.path.isabs(filename):
            # If filename is already a full path, use it directly
            file_path = filename
        else:
            # If filename is relative, join with input_folder
            file_path = os.path.join(input_folder, filename)
        
        try:
            print(f"  → Attempting to read: {file_path}")
            print(f"  → File exists: {os.path.exists(file_path)}")
            
            # Read CSV based on provider configuration
            if config["has_headers"]:
                # Read with headers, then select specific columns
                temp_df = pd.read_csv(file_path)
                print(f"  → Read {len(temp_df)} total rows with headers")
                print(f"  → Available columns: {list(temp_df.columns)}")
                monthly_df = temp_df.iloc[:, config["columns_to_use"]].copy()
            else:
                # Read without headers, select specific columns
                temp_df = pd.read_csv(file_path, header=None)
                print(f"  → Read {len(temp_df)} total rows without headers")
                print(f"  → Available columns: {list(temp_df.columns)}")
                monthly_df = temp_df.iloc[:, config["columns_to_use"]].copy()
            
            print(f"  → Selected columns data shape: {monthly_df.shape}")
            print(f"  → First few rows before processing:")
            print(monthly_df.head(3))
            
            # Assign standardized column names based on provider configuration
            monthly_df.columns = config["column_names"]
            
            # Reorder columns to match output format: Date, Amount, Description
            monthly_df = monthly_df[['Date', 'Amount', 'Description']]
            
            # Standardize date format to mm/dd/yyyy
            print(f"  → Before date conversion: {monthly_df['Date'].head(3).tolist()}")
            monthly_df['Date'] = pd.to_datetime(monthly_df['Date'], errors='coerce').dt.strftime('%m/%d/%Y')
            print(f"  → After date conversion: {monthly_df['Date'].head(3).tolist()}")
            
            # Convert Amount to numeric, removing any currency symbols or commas
            print(f"  → Before amount conversion: {monthly_df['Amount'].head(3).tolist()}")
            monthly_df['Amount'] = pd.to_numeric(monthly_df['Amount'].astype(str).str.replace(r'[\$,]', '', regex=True), errors='coerce')
            print(f"  → After amount conversion: {monthly_df['Amount'].head(3).tolist()}")
            
            # Remove any rows where date parsing failed or amount is not numeric
            rows_before_cleanup = len(monthly_df)
            monthly_df = monthly_df.dropna(subset=['Date', 'Amount'])
            rows_after_cleanup = len(monthly_df)
            print(f"  → Rows before cleanup: {rows_before_cleanup}, after cleanup: {rows_after_cleanup}")
            
            if len(monthly_df) == 0:
                print(f"  → WARNING: No valid rows remaining after data cleanup!")
                continue
            
            # Check for duplicates and filter out existing transactions
            new_transactions = []
            skipped_count = 0
            
            for _, row in monthly_df.iterrows():
                # Create tuple for this transaction
                transaction_tuple = (str(row['Date']), str(row['Amount']), str(row['Description']))
                
                # Check if this transaction already exists
                if transaction_tuple not in existing_transactions:
                    new_transactions.append(row)
                    # Add to existing set to avoid duplicates within the same file
                    existing_transactions.add(transaction_tuple)
                else:
                    skipped_count += 1
            
            # Convert new transactions to DataFrame
            if new_transactions:
                new_df = pd.DataFrame(new_transactions)
                # Append to aggregated DataFrame
                aggregated_df = pd.concat([aggregated_df, new_df], ignore_index=True)
            
            new_count = len(new_transactions)
            total_new_transactions += new_count
            total_skipped_transactions += skipped_count
            
            print(f"✓ Processed file {i}/{len(file_list)}: {filename}")
            print(f"  - New transactions: {new_count}")
            print(f"  - Skipped duplicates: {skipped_count}")
            print(f"  - Total in file: {len(monthly_df)}")
            
        except FileNotFoundError:
            print(f"✗ File not found: {filename}")
            continue
        except Exception as e:
            print(f"✗ Error processing {filename}: {str(e)}")
            print(f"  - Provider: {credit_card_provider}")
            print(f"  - Expected columns: {config['columns_to_use']}")
            continue
    
    # Save aggregated data with error handling
    try:
        # Check if output directory exists
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            print(f"Creating output directory: {output_dir}")
            os.makedirs(output_dir, exist_ok=True)
        
        # Save the file
        aggregated_df.to_csv(output_file, index=False)
        print(f"✓ Successfully saved to: {output_file}")
        
    except PermissionError:
        print(f"✗ Permission denied when saving to: {output_file}")
        print("  - Check if the file is open in another program")
        print("  - Try running as administrator")
        print("  - Check folder permissions")
        
        # Try alternative filename
        alt_output = output_file.replace('.csv', '_backup.csv')
        try:
            aggregated_df.to_csv(alt_output, index=False)
            print(f"✓ Saved to alternative location: {alt_output}")
            output_file = alt_output
        except Exception as e:
            print(f"✗ Failed to save to alternative location: {str(e)}")
            raise
            
    except Exception as e:
        print(f"✗ Error saving file: {str(e)}")
        print(f"  - Output file path: {output_file}")
        print(f"  - Current working directory: {os.getcwd()}")
        
        # Try saving to current directory as fallback
        fallback_file = "aggregated_credit_card_fallback.csv"
        try:
            aggregated_df.to_csv(fallback_file, index=False)
            print(f"✓ Saved to fallback location: {fallback_file}")
            output_file = fallback_file
        except Exception as fallback_error:
            print(f"✗ Fallback save also failed: {str(fallback_error)}")
            raise
    
    print(f"\nAggregation complete!")
    print(f"Total transactions in final file: {len(aggregated_df)}")
    print(f"New transactions added: {total_new_transactions}")
    print(f"Duplicate transactions skipped: {total_skipped_transactions}")
    print(f"Final output location: {output_file}")
    
    return aggregated_df

def aggregate_with_file_list(file_list, input_folder="./", output_file="aggregated_credit_card_2025.csv", credit_card_provider="FirstBank"):
    """
    Convenience function to aggregate files when you have a specific list.
    
    Args:
        file_list (list): List of CSV filenames to process
        input_folder (str): Path to folder containing CSV files
        output_file (str): Path for the output aggregated CSV file
        credit_card_provider (str): Credit card provider ("FirstBank" or "Chase")
    """
    return aggregate_credit_card_csvs(input_folder, file_list, output_file, credit_card_provider)

# Example usage
if __name__ == "__main__":
    # Example for FirstBank (original format)
    firstbank_files = [
        "Transactions-2025-01-08.csv",
        "Transactions-2025-02-06.csv",
        "Transactions-2025-03-10.csv",
        "Transactions-2025-04-09.csv",
        "Transactions-2025-05-08.csv",
        "Transactions-2025-06-09.csv"
        # Add more FirstBank files as needed
    ]
    
    # Example for Chase (new format)
    chase_files = [
        "Chase1417_Activity20241224_20250706_20250706.CSV",
        "Chase7290_Activity20241224_20250706_20250706.CSV"
        # Add more Chase files as needed
    ]
    
    # Set your paths
    input_folder = "C:/Users/Graduate/Downloads/"  # Adjust path as needed
    
    # Process FirstBank files
    print("=" * 50)
    print("PROCESSING FIRSTBANK STATEMENTS")
    print("=" * 50)
    firstbank_output = "C:/Users/Graduate/Documents/PersonalFinance/FirstBankCard/CreditCard_2025_Aggregated.csv"
    result_df_firstbank = aggregate_with_file_list(
        file_list=firstbank_files,
        input_folder=input_folder,
        output_file=firstbank_output,
        credit_card_provider="FirstBank"
    )
    
    # Process Chase files
    print("\n" + "=" * 50)
    print("PROCESSING CHASE STATEMENTS")
    print("=" * 50)
    chase_output = "C:/Users/Graduate/Documents/PersonalFinance/Chase/CreditCard_2025_Aggregated.csv"
    result_df_chase = aggregate_with_file_list(
        file_list=chase_files,
        input_folder=input_folder,
        output_file=chase_output,
        credit_card_provider="Chase"
    )
    
 # Show sample of aggregated data for each provider
    print("\n" + "=" * 50)
    print("FIRSTBANK SAMPLE DATA")
    print("=" * 50)
    if len(result_df_firstbank) > 0:
        print("First 3 rows:")
        print(result_df_firstbank.head(3))
        
        # Safe calculation of total amount
        try:
            total_amount = result_df_firstbank['Amount'].sum()

            # Convert dates back to datetime for proper min/max calculation
            date_series = pd.to_datetime(result_df_firstbank['Date'], errors='coerce')
            min_date = date_series.min().strftime('%m/%d/%Y')
            max_date = date_series.max().strftime('%m/%d/%Y')

            print(f"\nDate range: {min_date} to {max_date}")
            print(f"Total amount: ${total_amount:,.2f}")
            print(f"Number of transactions: {len(result_df_firstbank)}")
        except Exception as e:
            print(f"Error calculating summary statistics: {str(e)}")
            print("Amount column data types:", result_df_firstbank['Amount'].dtype)
            print("Sample Amount values:", result_df_firstbank['Amount'].head())
    else:
        print("No FirstBank data processed")
    
    print("\n" + "=" * 50)
    print("CHASE SAMPLE DATA")
    print("=" * 50)
    if len(result_df_chase) > 0:
        print("First 3 rows:")
        print(result_df_chase.head(3))
        
        # Safe calculation of total amount
        try:
            total_amount = result_df_chase['Amount'].sum()

            # Convert dates back to datetime for proper min/max calculation
            date_series = pd.to_datetime(result_df_chase['Date'], errors='coerce')
            min_date = date_series.min().strftime('%m/%d/%Y')
            max_date = date_series.max().strftime('%m/%d/%Y')

            print(f"\nDate range: {min_date} to {max_date}")
            print(f"Total amount: ${total_amount:,.2f}")
            print(f"Number of transactions: {len(result_df_chase)}")
        except Exception as e:
            print(f"Error calculating summary statistics: {str(e)}")
            print("Amount column data types:", result_df_chase['Amount'].dtype)
            print("Sample Amount values:", result_df_chase['Amount'].head())
    else:
        print("No Chase data processed")