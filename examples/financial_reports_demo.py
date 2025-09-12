#!/usr/bin/env python3
"""
Demo script showcasing ERPNext-MCP Financial Reporting Tools

This script demonstrates how to use the new financial reporting tools
added to the ERPNext-MCP server.
"""

# Note: This is a demonstration script. In actual usage, these functions 
# would be called via the MCP protocol from an MCP client.

def demo_financial_reports():
    """Demonstrate financial reporting functionality."""
    
    print("=== ERPNext-MCP Financial Reporting Tools Demo ===\n")
    
    # Company and date parameters for all reports
    company = "ABC Corporation"
    from_date = "2025-01-01"
    to_date = "2025-01-31"
    
    print("Available Financial Report Tools:")
    print("1. Balance Sheet")
    print("2. Profit & Loss Statement (Income Statement)")
    print("3. Cash Flow Statement") 
    print("4. Trial Balance")
    print("5. General Ledger")
    print("6. Generic Financial Statements (dispatcher)")
    print()
    
    print("=== Sample Usage Examples ===\n")
    
    # 1. Balance Sheet
    print("1. Balance Sheet Report:")
    print(f"""
    balance_sheet = get_balance_sheet(
        company="{company}",
        from_date="{from_date}",
        to_date="{to_date}",
        periodicity="Monthly"
    )
    """)
    
    # 2. Profit & Loss Statement
    print("2. Profit & Loss Statement:")
    print(f"""
    profit_loss = get_profit_and_loss(
        company="{company}",
        from_date="{from_date}",
        to_date="{to_date}",
        periodicity="Monthly"
    )
    """)
    
    # 3. Income Statement (alias)
    print("3. Income Statement (P&L alias):")
    print(f"""
    income_statement = get_income_statement(
        company="{company}",
        from_date="{from_date}",
        to_date="{to_date}",
        periodicity="Quarterly"
    )
    """)
    
    # 4. Cash Flow Statement
    print("4. Cash Flow Statement:")
    print(f"""
    cash_flow = get_cash_flow_statement(
        company="{company}",
        from_date="{from_date}",
        to_date="{to_date}",
        periodicity="Monthly"
    )
    """)
    
    # 5. Trial Balance
    print("5. Trial Balance:")
    print(f"""
    trial_balance = get_trial_balance(
        company="{company}",
        from_date="{from_date}",
        to_date="{to_date}",
        periodicity="Monthly"
    )
    """)
    
    # 6. General Ledger with filters
    print("6. General Ledger (with filters):")
    print(f"""
    general_ledger = get_general_ledger(
        company="{company}",
        from_date="{from_date}",
        to_date="{to_date}",
        account="Cash - ABC",
        party="Customer XYZ"
    )
    """)
    
    # 7. Generic dispatcher
    print("7. Generic Financial Statements dispatcher:")
    print(f"""
    # Get Balance Sheet using generic method
    statements = get_financial_statements(
        company="{company}",
        report_type="Balance Sheet",
        from_date="{from_date}",
        to_date="{to_date}"
    )
    
    # Get P&L using generic method  
    statements = get_financial_statements(
        company="{company}",
        report_type="Profit and Loss",
        from_date="{from_date}",
        to_date="{to_date}"
    )
    """)
    
    print("=== Expected Response Format ===\n")
    print("""
    {
        "success": true,
        "message": "Balance Sheet retrieved successfully",
        "data": {
            "result": [
                {"account": "Assets", "balance": 100000},
                {"account": "Liabilities", "balance": 50000},
                {"account": "Equity", "balance": 50000}
            ],
            "columns": ["Account", "Balance"],
            "company": "ABC Corporation",
            "from_date": "2025-01-01",
            "to_date": "2025-01-31"
        }
    }
    """)
    
    print("=== Advanced Usage ===\n")
    
    print("Different Periodicity Options:")
    print("- Daily")
    print("- Weekly") 
    print("- Monthly")
    print("- Quarterly")
    print("- Half-yearly")
    print("- Yearly")
    print()
    
    print("Report-specific Filters:")
    print("- General Ledger: account, party, party_type, group_by")
    print("- All Reports: periodicity, filter_based_on, custom parameters")
    print()
    
    print("=== Integration Notes ===\n")
    print("These tools integrate with ERPNext's standard reporting system:")
    print("- Balance Sheet → ERPNext 'Balance Sheet' report")
    print("- P&L Statement → ERPNext 'Profit and Loss Statement' report") 
    print("- Cash Flow → ERPNext 'Cash Flow' report")
    print("- Trial Balance → ERPNext 'Trial Balance' report")
    print("- General Ledger → ERPNext 'General Ledger' report")
    print()
    
    print("Error Handling:")
    print("- Automatic fallback to alternative ERPNext APIs")
    print("- Structured error responses with helpful messages")
    print("- Validation for unsupported report types")
    print()
    
    print("=== MCP Integration ===\n")
    print("These tools are exposed as MCP tools and can be called from any MCP client:")
    print("- Claude Desktop")
    print("- VS Code with MCP extension")  
    print("- Custom MCP applications")
    print("- Command line MCP tools")


if __name__ == "__main__":
    demo_financial_reports()