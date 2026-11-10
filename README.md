 SplitMate – Smart Expense Sharing System

1. Project Overview
SplitMate is a Python-based expense-sharing application developed using Streamlit. It helps groups record shared expenses, calculate individual balances, analyse spending patterns, and track settlements.

 2. Project Objectives
- Simplify group expense management.
- Record expenses and identify who paid.
- Split expenses among selected members.
- Calculate individual balances.
- Provide spending analytics and visualisations.
- Track settlement status.

 3. Technology Stack
- Python – Application development
- Streamlit – User interface
- SQLite – Database management
- Pandas – Data handling and analysis
- NumPy – Numerical operations
- Matplotlib – Data visualisation

 4. Application Modules
      #Dashboard
                   Displays expense summaries, member balances, and suggested settlements.

    #Add Expense

                  Allows users to enter an expense, specify the payer, and select members sharing the expense.


    #Group Members

                Allows users to manage group members.

    #Analytics

                Displays spending summaries, member-wise analysis, and charts.

    #Settlement Payments    
                 Tracks settlement status and payment confirmations. It does not process live UPI transactions.

 5. Database Structure
The application uses SQLite with the following tables:
- `members` – Stores group member information.
- `expenses` – Stores expense records.
- `expense_members` – Stores expense-sharing details.
- `settlements` – Stores settlement information.

 6. Expense Calculation Methodology
Expenses are recorded against the selected payer and participating members. The application uses the recorded sharing details to calculate balances and suggest settlements.

7. Installation and Execution

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

 8. Data Analytics
The application provides:
- Total group expenditure.
- Average expense.
- Highest expense.
- Member-wise spending analysis.
- Spending visualisations.

 9. Limitations
- Settlement Payments tracks payment confirmation; it is not a live payment gateway.
- Expense records are stored in a local SQLite database.

 10. Future Enhancements
- Expense editing and deletion.
- Exportable expense reports.
- Integration with payment providers.
- Additional expense categories and analytics.