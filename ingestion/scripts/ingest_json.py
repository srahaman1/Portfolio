import argparse
import json
import sys
from time import time
import pandas as pd
from sqlalchemy import create_engine

def read_json_in_chunks(file_path, chunk_size=1000):
    """Read JSON file in chunks to handle large files."""
    records = []
    with open(file_path, 'r') as file:
        # Load the entire JSON file
        data = json.load(file)
        
        # Handle both JSON arrays and objects
        if isinstance(data, dict):
            data = [data]
        
        # Process in chunks
        for i in range(0, len(data), chunk_size):
            chunk = data[i:i + chunk_size]
            records.extend(chunk)
            if len(records) >= chunk_size:
                yield pd.DataFrame(records)
                records = []
    
    # Yield any remaining records
    if records:
        yield pd.DataFrame(records)

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    schema = params.schema
    table = params.table
    file_path = params.file_path
    
    print(f'Processing JSON file: {file_path}')

    # Create SQL engine with schema specification
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    
    # Create schema if it doesn't exist
    with engine.connect() as connection:
        connection.execute(f'CREATE SCHEMA IF NOT EXISTS {schema}')
        connection.commit()

    try:
        # Read first chunk to get structure
        df_iter = read_json_in_chunks(file_path)
        first_chunk = next(df_iter)
        
        # Create the table with schema
        full_table_name = f'{schema}.{table}'
        first_chunk.head(0).to_sql(
            name=table,
            schema=schema,
            con=engine,
            if_exists='replace',
            index=False
        )
        
        # Insert first chunk
        print('Inserting first chunk...')
        first_chunk.to_sql(
            name=table,
            schema=schema,
            con=engine,
            if_exists='append',
            index=False
        )

        # Insert remaining chunks
        t_start = time()
        count = 1
        
        for chunk_df in df_iter:
            count += 1
            print(f'Inserting batch {count}...')
            
            b_start = time()
            chunk_df.to_sql(
                name=table,
                schema=schema,
                con=engine,
                if_exists='append',
                index=False
            )
            b_end = time()
            
            print(f'Inserted! Time taken: {b_end-b_start:10.3f} seconds.\n')
        
        t_end = time()
        print(f'Completed! Total time taken was {t_end-t_start:10.3f} seconds for {count} batches.')
        
    except Exception as e:
        print(f'Error processing file: {str(e)}')
        sys.exit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Load JSON data into PostgreSQL database.')
    
    parser.add_argument('--user', default='root', help='Username for Postgres (default: root)')
    parser.add_argument('--password', default='root', help='Password for Postgres (default: root)')
    parser.add_argument('--host', default='pg-database', help='Hostname for Postgres (default: pg-database)')
    parser.add_argument('--port', default='5432', help='Port for Postgres (default: 5432)')
    parser.add_argument('--db', default='portfolio_db', help='Database name for Postgres (default: portfolio_db)')
    parser.add_argument('--schema', required=True, help='Schema name for Postgres')
    parser.add_argument('--table', required=True, help='Table name for Postgres')
    parser.add_argument('--file_path', required=True, help='Path to JSON file')
    
    args = parser.parse_args()
    main(args)