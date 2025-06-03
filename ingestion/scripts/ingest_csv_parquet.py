import argparse
import os
import sys
from time import time
import pandas as pd 
import pyarrow.parquet as pq
from sqlalchemy import create_engine, text


def create_schema_if_not_exists(engine, schema_name):
    """Create a schema if it doesn't exist"""
    with engine.connect() as conn:
        conn.execute(text(f'CREATE SCHEMA IF NOT EXISTS {schema_name}'))
        conn.commit()


def main(params):
    # Get database connection parameters from environment variables or command line args
    user = params.user or os.getenv('DB_USER', 'root')
    password = params.password or os.getenv('DB_PASSWORD', 'root')
    host = params.host or os.getenv('DB_HOST', 'pg-database')
    port = params.port or os.getenv('DB_PORT', '5432')
    db = params.db or os.getenv('DB_NAME', 'portfolio_db')
    schema = params.schema  # Schema is required
    tb = params.tb
    url = params.url
    
    # Get the name of the file from url
    file_name = url.rsplit('/', 1)[-1].strip()
    print(f'Downloading {file_name} ...')
    # Download file from url
    os.system(f'curl {url.strip()} -o {file_name}')
    print('\n')

    # Create SQL engine
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    
    # Create schema if it doesn't exist
    create_schema_if_not_exists(engine, schema)

    # Read file based on csv or parquet
    if '.csv' in file_name:
        df = pd.read_csv(file_name, nrows=10)
        df_iter = pd.read_csv(file_name, iterator=True, chunksize=100000)
    elif '.parquet' in file_name:
        file = pq.ParquetFile(file_name)
        df = next(file.iter_batches(batch_size=10)).to_pandas()
        df_iter = file.iter_batches(batch_size=100000)
    else: 
        print('Error. Only .csv or .parquet files allowed.')
        sys.exit()

    # Create the table with schema
    df.head(0).to_sql(
        name=tb, 
        schema=schema,  # Add schema here
        con=engine, 
        if_exists='replace',
        index=False  # Don't include index as a column
    )

    # Insert values
    t_start = time()
    count = 0
    for batch in df_iter:
        count += 1

        if '.parquet' in file_name:
            batch_df = batch.to_pandas()
        else:
            batch_df = batch

        print(f'inserting batch {count}...')

        b_start = time()
        batch_df.to_sql(
            name=tb, 
            schema=schema,  # Add schema here
            con=engine, 
            if_exists='append',
            index=False  # Don't include index as a column
        )
        b_end = time()

        print(f'inserted! time taken {b_end-b_start:10.3f} seconds.\n')
        
    t_end = time()   
    print(f'Completed! Total time taken was {t_end-t_start:10.3f} seconds for {count} batches.')    

    # Clean up downloaded file
    os.remove(file_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV or Parquet file to Postgres database.')

    # Required arguments
    parser.add_argument('--schema', required=True, help='Schema name for the table')
    parser.add_argument('--tb', required=True, help='Table name')
    parser.add_argument('--url', required=True, help='URL for the file')

    # Optional arguments (can use environment variables instead)
    parser.add_argument('--user', help='Username for Postgres')
    parser.add_argument('--password', help='Password for Postgres')
    parser.add_argument('--host', help='Hostname for Postgres')
    parser.add_argument('--port', help='Port for Postgres')
    parser.add_argument('--db', help='Database name for Postgres')

    args = parser.parse_args()
    main(args)