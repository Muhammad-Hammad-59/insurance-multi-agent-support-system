"""
backend/db/database.py
Handles SQLite connection, schema creation, and all query functions.
"""

import sqlite3
import os
from typing import Dict, Any, List, Optional
from backend.config import Config
DB_PATH = Config.SQLITE_PATH


def connect_db() -> sqlite3.Connection:
    """Connect to SQLite database."""
    return sqlite3.connect(DB_PATH)


def drop_and_create_tables(conn: sqlite3.Connection) -> None:
    """Drop existing tables and recreate schema."""
    cursor = conn.cursor()
    cursor.executescript("""
        DROP TABLE IF EXISTS claims;
        DROP TABLE IF EXISTS payments;
        DROP TABLE IF EXISTS billing;
        DROP TABLE IF EXISTS auto_policy_details;
        DROP TABLE IF EXISTS policies;
        DROP TABLE IF EXISTS customers;

        CREATE TABLE customers (
            customer_id VARCHAR(20) PRIMARY KEY,
            first_name  VARCHAR(50),
            last_name   VARCHAR(50),
            email       VARCHAR(100),
            phone       VARCHAR(20),
            date_of_birth DATE,
            state       VARCHAR(20)
        );

        CREATE TABLE policies (
            policy_number     VARCHAR(20) PRIMARY KEY,
            customer_id       VARCHAR(20),
            policy_type       VARCHAR(50),
            start_date        DATE,
            premium_amount    DECIMAL(10,2),
            billing_frequency VARCHAR(20),
            status            VARCHAR(20),
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        );

        CREATE TABLE auto_policy_details (
            policy_number            VARCHAR(20) PRIMARY KEY,
            vehicle_vin              VARCHAR(50),
            vehicle_make             VARCHAR(50),
            vehicle_model            VARCHAR(50),
            vehicle_year             INTEGER,
            liability_limit          DECIMAL(10,2),
            collision_deductible     DECIMAL(10,2),
            comprehensive_deductible DECIMAL(10,2),
            uninsured_motorist       BOOLEAN,
            rental_car_coverage      BOOLEAN,
            FOREIGN KEY (policy_number) REFERENCES policies(policy_number)
        );

        CREATE TABLE billing (
            bill_id       VARCHAR(20) PRIMARY KEY,
            policy_number VARCHAR(20),
            billing_date  DATE,
            due_date      DATE,
            amount_due    DECIMAL(10,2),
            status        VARCHAR(20),
            FOREIGN KEY (policy_number) REFERENCES policies(policy_number)
        );

        CREATE TABLE payments (
            payment_id     VARCHAR(20) PRIMARY KEY,
            bill_id        VARCHAR(20),
            payment_date   DATE,
            amount         DECIMAL(10,2),
            payment_method VARCHAR(50),
            transaction_id VARCHAR(100),
            status         VARCHAR(20),
            FOREIGN KEY (bill_id) REFERENCES billing(bill_id)
        );

        CREATE TABLE claims (
            claim_id       VARCHAR(20) PRIMARY KEY,
            policy_number  VARCHAR(20),
            claim_date     DATE,
            incident_type  VARCHAR(100),
            estimated_loss DECIMAL(10,2),
            status         VARCHAR(20),
            FOREIGN KEY (policy_number) REFERENCES policies(policy_number)
        );
    """)
    conn.commit()


def insert_data(conn: sqlite3.Connection, data: dict) -> None:
    """Insert all DataFrames into SQLite."""
    for table, df in data.items():
        df.to_sql(table, conn, if_exists="append", index=False)
    conn.commit()


# ─── Tool Functions (called by agents) ─────────────────────────────────────

def get_policy_details(policy_number: str) -> Dict[str, Any]:
    """Fetch a customer's policy details by policy number."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.*, c.first_name, c.last_name
        FROM policies p
        JOIN customers c ON p.customer_id = c.customer_id
        WHERE p.policy_number = ?
    """, (policy_number,))
    result = cursor.fetchone()
    conn.close()
    if result:
        columns = [desc[0] for desc in cursor.description]
        return dict(zip(columns, result))
    return {"error": "Policy not found"}


def get_claim_status(
    claim_id: Optional[str] = None,
    policy_number: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Get claim status and details by claim ID or policy number."""
    conn = connect_db()
    cursor = conn.cursor()
    if claim_id:
        cursor.execute("""
            SELECT c.*, p.policy_type
            FROM claims c
            JOIN policies p ON c.policy_number = p.policy_number
            WHERE c.claim_id = ?
        """, (claim_id,))
    elif policy_number:
        cursor.execute("""
            SELECT c.*, p.policy_type
            FROM claims c
            JOIN policies p ON c.policy_number = p.policy_number
            WHERE c.policy_number = ?
            ORDER BY c.claim_date DESC LIMIT 3
        """, (policy_number,))
    else:
        conn.close()
        return [{"error": "Provide claim_id or policy_number"}]
    result = cursor.fetchall()
    conn.close()
    if result:
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in result]
    return [{"error": "Claim not found"}]


def get_billing_info(
    policy_number: Optional[str] = None,
    customer_id: Optional[str] = None
) -> Dict[str, Any]:
    """Get billing information including current balance and due dates."""
    conn = connect_db()
    cursor = conn.cursor()
    if policy_number:
        cursor.execute("""
            SELECT b.*, p.premium_amount, p.billing_frequency
            FROM billing b
            JOIN policies p ON b.policy_number = p.policy_number
            WHERE b.policy_number = ? AND b.status = 'pending'
            ORDER BY b.due_date DESC LIMIT 1
        """, (policy_number,))
    elif customer_id:
        cursor.execute("""
            SELECT b.*, p.premium_amount, p.billing_frequency
            FROM billing b
            JOIN policies p ON b.policy_number = p.policy_number
            WHERE p.customer_id = ? AND b.status = 'pending'
            ORDER BY b.due_date DESC LIMIT 1
        """, (customer_id,))
    else:
        conn.close()
        return {"error": "Provide policy_number or customer_id"}
    result = cursor.fetchone()
    conn.close()
    if result:
        columns = [desc[0] for desc in cursor.description]
        return dict(zip(columns, result))
    return {"error": "Billing information not found"}


def get_payment_history(policy_number: str) -> List[Dict[str, Any]]:
    """Get payment history for a policy (last 10 payments)."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.payment_date, p.amount, p.status, p.payment_method
        FROM payments p
        JOIN billing b ON p.bill_id = b.bill_id
        WHERE b.policy_number = ?
        ORDER BY p.payment_date DESC LIMIT 10
    """, (policy_number,))
    results = cursor.fetchall()
    conn.close()
    if results:
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in results]
    return []


def get_auto_policy_details(policy_number: str) -> Dict[str, Any]:
    """Get auto-specific policy details including vehicle info and deductibles."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT apd.*, p.policy_type, p.premium_amount
        FROM auto_policy_details apd
        JOIN policies p ON apd.policy_number = p.policy_number
        WHERE apd.policy_number = ?
    """, (policy_number,))
    result = cursor.fetchone()
    conn.close()
    if result:
        columns = [desc[0] for desc in cursor.description]
        return dict(zip(columns, result))
    return {"error": "Auto policy details not found"}




def ask_user(question: str, missing_info: str = ""):
    """Ask the user for input and return the response."""
    print(f"🗣️ Asking user for input: {question}")
    if missing_info:
        print(f"---USER INPUT REQUIRED---\nMissing information: {missing_info}")
    else:
        print(f"---USER INPUT REQUIRED---")
    
    answer = input(f"{question}: ")
    return {"context": answer, "source": "User Input"}



ask_user_tool = {
    "type": "function",
    "function": {
        "name": "ask_user",
        "description": "Ask the user for missing information",
        "parameters": {
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": "Question to ask the user"
                },
                "missing_info": {
                    "type": "string",
                    "description": "What information is missing"
                }
            },
            "required": ["question"]
        }
    }
}