# Expense Sharing Application  

## Overview
This project is a simplified backend design of an expense sharing application
similar to Splitwise. It allows users to create groups, add shared expenses,
track balances, and simplify settlements.

This solution focuses on:
- Clean object-oriented design
- Clear balance tracking
- Simplicity and correctness

## Features
- Create users and groups
- Add expenses with multiple split types:
  - Equal split
  - Exact amount split
  - Percentage split
- Track who owes whom
- Simplify balances to minimize transactions
- Settle dues between users

## Design Approach
- Implemented using Python and Object-Oriented Programming
- Uses in-memory data structures (no database)
- Balances are tracked as:
  - balances[A][B] = amount A owes B
- Simplification is done using net balance calculation

## How to Run
1. Ensure Python 3 is installed
2. Run the application:
   ```bash
   python expense_sharing.py
