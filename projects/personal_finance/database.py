"""
Database management for Finance Application
Handles all data storage and retrieval
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Any


class FinanceDatabase:
    """Manages SQLite database for finance tracking"""
    
    def __init__(self, db_path: str = "finances.db"):
        self.db_path = db_path
        self.conn = None
        self.initialize_database()
    
    def initialize_database(self):
        """Create database and tables if they don't exist"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        
        cursor = self.conn.cursor()
        
        # Paycheck configurations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS paycheck_configs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                salary REAL NOT NULL,
                pay_periods INTEGER DEFAULT 26,
                
                -- 401k
                contribution_401k_percent REAL DEFAULT 0.15,
                employer_match_percent REAL DEFAULT 0.03,
                max_employer_match REAL DEFAULT 3000.00,
                
                -- HSA
                hsa_per_paycheck REAL DEFAULT 50.59,
                
                -- Transit FSA
                transit_fsa_per_paycheck REAL DEFAULT 0.0,
                
                -- Insurance
                medical_insurance_per_paycheck REAL DEFAULT 46.67,
                dental_premium_annual REAL DEFAULT 130.52,
                vision_premium_annual REAL DEFAULT 124.28,
                
                -- ESPP
                espp_percent REAL DEFAULT 0.04,
                
                -- State tax info
                state TEXT DEFAULT 'NY',
                standard_deduction_federal REAL DEFAULT 14600.0,
                standard_deduction_state REAL DEFAULT 8000.0,
                
                -- Post-tax allocations
                savings_percent REAL DEFAULT 0.0,
                savings2_percent REAL DEFAULT 0.0,
                roth_ira_per_paycheck REAL DEFAULT 0.0,
                brokerage_per_paycheck REAL DEFAULT 0.0,
                crypto_per_paycheck REAL DEFAULT 0.0,
                
                -- Metadata
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        """)
        
        # Net worth tracking table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS networth_snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                snapshot_date DATE NOT NULL UNIQUE,
                
                -- Assets
                robinhood REAL DEFAULT 0.0,
                crypto REAL DEFAULT 0.0,
                roth_ira REAL DEFAULT 0.0,
                k401_balance REAL DEFAULT 0.0,
                cd_savings REAL DEFAULT 0.0,
                checking REAL DEFAULT 0.0,
                savings REAL DEFAULT 0.0,
                hsa REAL DEFAULT 0.0,
                transit_fsa REAL DEFAULT 0.0,
                rsu_espp REAL DEFAULT 0.0,
                common_stock REAL DEFAULT 0.0,
                etfs REAL DEFAULT 0.0,
                business_account REAL DEFAULT 0.0,
                
                -- Calculated total
                total_assets REAL GENERATED ALWAYS AS (
                    robinhood + crypto + roth_ira + k401_balance + cd_savings +
                    checking + savings + hsa + transit_fsa + rsu_espp + 
                    common_stock + etfs + business_account
                ) STORED,
                
                -- Liabilities
                car_loan REAL DEFAULT 0.0,
                other_debt REAL DEFAULT 0.0,
                
                -- Calculated net worth
                net_worth REAL GENERATED ALWAYS AS (
                    robinhood + crypto + roth_ira + k401_balance + cd_savings +
                    checking + savings + hsa + transit_fsa + rsu_espp + 
                    common_stock + etfs + business_account - car_loan - other_debt
                ) STORED,
                
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Paycheck calculations history
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS paycheck_calculations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                config_id INTEGER,
                calculation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                
                -- Input values
                salary REAL,
                
                -- Calculated values (stored as JSON for flexibility)
                calculation_details TEXT,
                
                FOREIGN KEY (config_id) REFERENCES paycheck_configs(id)
            )
        """)
        
        # Tax brackets table (for reference and updates)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tax_brackets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tax_year INTEGER NOT NULL,
                jurisdiction TEXT NOT NULL,  -- 'federal', 'NY', 'NYC'
                filing_status TEXT DEFAULT 'single',
                
                -- Bracket data stored as JSON
                brackets TEXT NOT NULL,  -- JSON: [{"threshold": 0, "rate": 0.10}, ...]
                
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(tax_year, jurisdiction, filing_status)
            )
        """)
        
        self.conn.commit()
        
        # Initialize with 2024 tax brackets
        self._initialize_tax_brackets()
    
    def _initialize_tax_brackets(self):
        """Initialize tax brackets for 2024"""
        cursor = self.conn.cursor()
        
        # Check if brackets already exist
        cursor.execute("SELECT COUNT(*) FROM tax_brackets WHERE tax_year = 2024")
        if cursor.fetchone()[0] > 0:
            return  # Already initialized
        
        # Federal brackets (threshold = income level where this rate starts)
        federal_brackets = [
            {"threshold": 0, "rate": 0.10},      # $0 - $11,600
            {"threshold": 11600, "rate": 0.12},   # $11,600 - $47,150
            {"threshold": 47150, "rate": 0.22},   # $47,150 - $100,525
            {"threshold": 100525, "rate": 0.24},  # $100,525 - $191,950
            {"threshold": 191950, "rate": 0.32},  # $191,950 - $243,725
            {"threshold": 243725, "rate": 0.35},  # $243,725 - $609,350
            {"threshold": 609350, "rate": 0.37}   # $609,350+
        ]
        
        # NY State brackets (from Paycheck Optimization sheet rows 51-55)
        ny_brackets = [
            {"threshold": 0, "rate": 0.04},       # $0 - $8,500
            {"threshold": 8500, "rate": 0.045},   # $8,500 - $11,700
            {"threshold": 11700, "rate": 0.0525}, # $11,700 - $13,900
            {"threshold": 13900, "rate": 0.055},  # $13,900 - $80,650  (NOT 0.0585!)
            {"threshold": 80650, "rate": 0.06}    # $80,650+  (NOT 0.0625!)
        ]
        
        # NYC Local brackets (from Paycheck Optimization sheet rows 60-63)
        nyc_brackets = [
            {"threshold": 0, "rate": 0.03078},      # $0 - $12,000
            {"threshold": 12000, "rate": 0.03762},  # $12,000 - $25,000
            {"threshold": 25000, "rate": 0.03819},  # $25,000 - $50,000
            {"threshold": 50000, "rate": 0.03876}   # $50,000+
        ]
        
        cursor.execute("""
            INSERT INTO tax_brackets (tax_year, jurisdiction, brackets)
            VALUES (?, ?, ?)
        """, (2024, 'federal', json.dumps(federal_brackets)))
        
        cursor.execute("""
            INSERT INTO tax_brackets (tax_year, jurisdiction, brackets)
            VALUES (?, ?, ?)
        """, (2024, 'NY', json.dumps(ny_brackets)))
        
        cursor.execute("""
            INSERT INTO tax_brackets (tax_year, jurisdiction, brackets)
            VALUES (?, ?, ?)
        """, (2024, 'NYC', json.dumps(nyc_brackets)))
        
        self.conn.commit()
    
    def save_paycheck_config(self, config: Dict[str, Any]) -> int:
        """Save a new paycheck configuration"""
        cursor = self.conn.cursor()
        
        # Deactivate all other configs if this one is active
        if config.get('is_active', True):
            cursor.execute("UPDATE paycheck_configs SET is_active = 0")
        
        columns = ', '.join(config.keys())
        placeholders = ', '.join(['?' for _ in config])
        
        cursor.execute(f"""
            INSERT INTO paycheck_configs ({columns})
            VALUES ({placeholders})
        """, list(config.values()))
        
        self.conn.commit()
        return cursor.lastrowid
    
    def get_active_paycheck_config(self) -> Optional[Dict]:
        """Get the currently active paycheck configuration"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM paycheck_configs 
            WHERE is_active = 1 
            ORDER BY updated_at DESC 
            LIMIT 1
        """)
        
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def save_networth_snapshot(self, snapshot: Dict[str, Any]) -> int:
        """Save a net worth snapshot"""
        cursor = self.conn.cursor()
        
        # Use today's date if not provided
        if 'snapshot_date' not in snapshot:
            snapshot['snapshot_date'] = datetime.now().date().isoformat()
        
        columns = ', '.join(snapshot.keys())
        placeholders = ', '.join(['?' for _ in snapshot])
        
        try:
            cursor.execute(f"""
                INSERT INTO networth_snapshots ({columns})
                VALUES ({placeholders})
            """, list(snapshot.values()))
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            # Date already exists, update instead
            set_clause = ', '.join([f"{k} = ?" for k in snapshot.keys() if k != 'snapshot_date'])
            values = [v for k, v in snapshot.items() if k != 'snapshot_date']
            values.append(snapshot['snapshot_date'])
            
            cursor.execute(f"""
                UPDATE networth_snapshots 
                SET {set_clause}
                WHERE snapshot_date = ?
            """, values)
            self.conn.commit()
            return cursor.lastrowid
    
    def get_networth_history(self, limit: Optional[int] = None) -> List[Dict]:
        """Get net worth history, optionally limited to most recent entries"""
        cursor = self.conn.cursor()
        
        query = "SELECT * FROM networth_snapshots ORDER BY snapshot_date DESC"
        if limit:
            query += f" LIMIT {limit}"
        
        cursor.execute(query)
        return [dict(row) for row in cursor.fetchall()]
    
    def get_tax_brackets(self, year: int = 2024) -> Dict[str, List[Dict]]:
        """Get tax brackets for a given year"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT jurisdiction, brackets 
            FROM tax_brackets 
            WHERE tax_year = ?
        """, (year,))
        
        result = {}
        for row in cursor.fetchall():
            result[row['jurisdiction']] = json.loads(row['brackets'])
        
        return result
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


if __name__ == "__main__":
    # Test database creation
    db = FinanceDatabase("test_finances.db")
    print("✅ Database created successfully!")
    
    # Test saving a config
    config = {
        'name': 'Current Salary',
        'salary': 84975.0,
        'contribution_401k_percent': 0.15,
        'employer_match_percent': 0.03
    }
    config_id = db.save_paycheck_config(config)
    print(f"✅ Saved config with ID: {config_id}")
    
    # Test retrieving config
    active_config = db.get_active_paycheck_config()
    print(f"✅ Retrieved config: {active_config['name']}")
    
    # Test tax brackets
    brackets = db.get_tax_brackets()
    print(f"✅ Loaded tax brackets for: {', '.join(brackets.keys())}")
    
    db.close()
    
    # Clean up test database
    import os
    os.remove("test_finances.db")
    print("\n✅ Database module working correctly!")
