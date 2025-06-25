import streamlit as st
from db import create_connection
from bank_operations import (
    register_user, login_user, deposit, withdraw,
    view_balance, view_transactions, get_account_summary,
    delete_account
)

def main():
    connection = create_connection()

    st.set_page_config(page_title="Bank Management System", layout="centered")
    st.title("🏦 Bank Management System")

    menu = [
        "Register", "Login", "Deposit", "Withdraw",
        "Balance Inquiry", "Transaction History",
        "Account Summary", "Change Password", "Delete Account"
    ]
    choice = st.sidebar.selectbox("Menu", menu)
    st.markdown("---")

    # ------------------ Register ------------------
    if choice == "Register":
        st.subheader("👤 Register New Account")
        name = st.text_input("Account Holder Name")
        password = st.text_input("Password", type='password')
        currency = st.selectbox("Currency", ["USD", "EUR", "INR"])

        if st.button("Register"):
            if not name or not password:
                st.warning("Please fill in both name and password.")
            else:
                register_user(connection, name, password, currency)
                st.success(f"✅ Account successfully registered for **{name}**.")

    # ------------------ Login ------------------
    elif choice == "Login":
        st.subheader("🔐 Login to Your Account")
        account_id = st.number_input("Account ID", min_value=1, step=1)
        password = st.text_input("Password", type='password')

        if st.button("Login"):
            if not password:
                st.warning("Please enter your password.")
            else:
                cursor = connection.cursor()
                cursor.execute("SELECT password FROM accounts WHERE account_id = %s", (account_id,))
                result = cursor.fetchone()
                if result and result[0] == password:
                    st.success("✅ Login successful!")
                else:
                    st.error("❌ Incorrect Account ID or Password. Please try again.")

    # ------------------ Deposit ------------------
    elif choice == "Deposit":
        st.subheader("💵 Deposit")
        account_id = st.number_input("Account ID", min_value=1, step=1)
        amount = st.number_input("Amount", min_value=0.01)
        if st.button("Deposit"):
            deposit(connection, account_id, amount)
            st.success("✅ Deposit completed successfully!")

    # ------------------ Withdraw ------------------
    elif choice == "Withdraw":
        st.subheader("💸 Withdraw")
        account_id = st.number_input("Account ID", min_value=1, step=1)
        amount = st.number_input("Amount", min_value=0.01)
        if st.button("Withdraw"):
            if withdraw(connection, account_id, amount):
                st.success("✅ Withdrawal successful!")
            else:
                st.error("❌ Insufficient balance!")

    # ------------------ Balance Inquiry ------------------
    elif choice == "Balance Inquiry":
        st.subheader("📊 Balance Inquiry")
        account_id = st.number_input("Account ID", min_value=1, step=1)
        if st.button("Check Balance"):
            balance = view_balance(connection, account_id)
            if balance is not None:
                st.info(f"💰 Current Balance: ${balance:.2f}")
            else:
                st.error("❌ Account not found.")

    # ------------------ Transaction History ------------------
    elif choice == "Transaction History":
        st.subheader("🧾 Transaction History")
        account_id = st.number_input("Account ID", min_value=1, step=1)
        if st.button("View Transactions"):
            transactions = view_transactions(connection, account_id)
            if transactions:
                for t_type, amount, date in transactions:
                    st.write(f"**{t_type}** of ${amount:.2f} on {date}")
            else:
                st.warning("No transactions found.")

    # ------------------ Account Summary ------------------
    elif choice == "Account Summary":
        st.subheader("📄 Account Summary")
        account_id = st.number_input("Account ID", min_value=1, step=1)
        if st.button("Get Summary"):
            summary = get_account_summary(connection, account_id)
            if summary:
                st.write(f"**Account Holder**: {summary['account_holder_name']}")
                st.write(f"**Balance**: ${summary['account_balance']:.2f}")
                st.write(f"**Total Deposits**: ${summary['total_deposits']:.2f}")
                st.write(f"**Total Withdrawals**: ${summary['total_withdrawals']:.2f}")
                st.write(f"**Transactions**: {summary['transaction_count']}")
            else:
                st.error("❌ Account not found.")

    # ------------------ Change Password ------------------
    elif choice == "Change Password":
        st.subheader("🔑 Change Password")
        account_id = st.number_input("Account ID", min_value=1, step=1)
        old_password = st.text_input("Old Password", type='password')
        new_password = st.text_input("New Password", type='password')
        if st.button("Change Password"):
            cursor = connection.cursor()
            cursor.execute("SELECT password FROM accounts WHERE account_id = %s", (account_id,))
            result = cursor.fetchone()
            if result and result[0] == old_password:
                cursor.execute("UPDATE accounts SET password = %s WHERE account_id = %s", (new_password, account_id))
                connection.commit()
                st.success("✅ Password updated successfully.")
            else:
                st.error("❌ Old password is incorrect.")

    # ------------------ Delete Account ------------------
    elif choice == "Delete Account":
        st.subheader("❌ Delete Account")
        account_id = st.number_input("Account ID", min_value=1, step=1)
        if st.button("Delete Account"):
            delete_account(connection, account_id)
            st.success("🗑️ Account and transaction history deleted successfully.")

    connection.close()

if __name__ == '__main__':
    main()
