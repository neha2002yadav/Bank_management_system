-- Create database
CREATE DATABASE IF NOT EXISTS bank_management_system;

-- Use the database
USE bank_management_system;

-- Create accounts table
CREATE TABLE IF NOT EXISTS accounts (
    account_id INT AUTO_INCREMENT PRIMARY KEY,
    account_holder_name VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL,
    currency VARCHAR(3) NOT NULL DEFAULT 'INR',
    balance DECIMAL(15, 2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create transactions table
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    account_id INT NOT NULL,
    transaction_type ENUM('deposit', 'withdrawal') NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id) ON DELETE CASCADE
);