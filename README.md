# Personal-Expense-Tracker
Sql project for tracking personal expense of a user, which can be used to find the total expense of a particular month, top spending categories of a user and has income vs expense comparison

Goal: To help users track income and expenses, analyze spending habits, and generate monthly/yearly financial summaries.

Tables-
1. Users(user_id (PK), name, email, password)
2. Categories(category_id (PK), category_name (e.g. Food, Travel, Bills, Entertainment), type (Income / Expense))
3. Transactions(transaction_id (PK), user_id (FK), category_id (FK), amount, date, payment_method (Cash, Card, UPI, etc.), note)
4. Budgets(budget_id (PK), user_id (FK), category_id (FK), amount_limit, month, year)
