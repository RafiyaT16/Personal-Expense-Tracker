# Personal-Expense-Tracker
Sql project for tracking personal expense of a user, which can be used to find the total expense of a particular month, top spending categories of a user and has income vs expense comparison

Goal: To help users track income and expenses, analyze spending habits, and generate monthly/yearly financial summaries.

Features:
1. Add daily expenses with category, amount, and date.
2. View all expenses.
3. Clear all expenses.
4. Expenses are saved MySQL database.
5. Frontend is responsive and simple.

It has expenses table which consists of -
expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category VARCHAR(255),
    amount DECIMAL(10,2),
    date DATE
)
