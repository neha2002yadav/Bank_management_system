#%%
import mysql.connector
import bcrypt

def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Neha@123",
        database="bank_management_system"
    )

# Utility: Hash a plain password
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

# ✅ Registration with password hashing
def register_user(connection, name, password, currency='USD'):
    hashed_password = hash_password(password)
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO accounts (account_holder_name, password, currency) VALUES (%s, %s, %s)",
        (name, password, currency)
    )
    connection.commit()

# ✅ Secure login using bcrypt
def login_user(connection, account_id, password):
    cursor = connection.cursor()
    cursor.execute("SELECT password FROM accounts WHERE account_id = %s", (account_id,))
    result = cursor.fetchone()

    if result:
        stored_hashed_password = result[0]
        try:
            return bcrypt.checkpw(password.encode(), stored_hashed_password.encode())
        except ValueError:
            print("⚠️ Invalid stored password format for account_id:", account_id)
            return False
    return False

# ✅ Deposit
def deposit(connection, account_id, amount):
    cursor = connection.cursor()
    cursor.execute("UPDATE accounts SET balance = balance + %s WHERE account_id = %s",
                   (amount, account_id))
    cursor.execute(
        "INSERT INTO transactions (account_id, transaction_type, amount) VALUES (%s, 'Deposit', %s)",
        (account_id, amount))
    connection.commit()

# ✅ Withdraw
def withdraw(connection, account_id, amount):
    cursor = connection.cursor()
    cursor.execute("SELECT balance FROM accounts WHERE account_id = %s", (account_id,))
    result = cursor.fetchone()
    if result and result[0] >= amount:
        cursor.execute("UPDATE accounts SET balance = balance - %s WHERE account_id = %s",
                       (amount, account_id))
        cursor.execute(
            "INSERT INTO transactions (account_id, transaction_type, amount) VALUES (%s, 'Withdrawal', %s)",
            (account_id, amount))
        connection.commit()
        return True
    else:
        return False

# ✅ View Balance
def view_balance(connection, account_id):
    cursor = connection.cursor()
    cursor.execute("SELECT balance FROM accounts WHERE account_id = %s", (account_id,))
    result = cursor.fetchone()
    return result[0] if result else 0.0

# ✅ View Transactions
def view_transactions(connection, account_id):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT transaction_type, amount, transaction_date FROM transactions WHERE account_id = %s",
        (account_id,))
    return cursor.fetchall()

# ✅ Delete Account
def delete_account(connection, account_id):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM transactions WHERE account_id = %s", (account_id,))
    cursor.execute("DELETE FROM accounts WHERE account_id = %s", (account_id,))
    connection.commit()

# ✅ Account Summary
def get_account_summary(connection, account_id):
    cursor = connection.cursor()

    # Get account holder info
    cursor.execute("SELECT account_holder_name, balance FROM accounts WHERE account_id = %s", (account_id,))
    account_info = cursor.fetchone()

    if not account_info:
        return None

    # Get transaction stats
    cursor.execute("""
        SELECT 
            SUM(CASE WHEN transaction_type = 'Deposit' THEN amount ELSE 0 END) AS total_deposits,
            SUM(CASE WHEN transaction_type = 'Withdrawal' THEN amount ELSE 0 END) AS total_withdrawals,
            COUNT(*) AS transaction_count
        FROM transactions WHERE account_id = %s
    """, (account_id,))
    transaction_summary = cursor.fetchone()

    return {
        "account_holder_name": account_info[0],
        "account_balance": account_info[1],
        "total_deposits": transaction_summary[0] or 0.0,
        "total_withdrawals": transaction_summary[1] or 0.0,
        "transaction_count": transaction_summary[2]
    }
