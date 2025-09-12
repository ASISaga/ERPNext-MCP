# Financial Reporting Tools - ERPNext MCP

This document provides detailed information about the financial reporting tools added to the ERPNext-MCP server.

## Overview

The ERPNext-MCP server now includes comprehensive financial reporting tools that provide access to all major financial statements and reports from ERPNext. These tools are designed to be business-friendly and follow the established patterns of the MCP server.

## Available Financial Reports

### Core Financial Statements

1. **Balance Sheet** (`get_balance_sheet`)
   - Shows financial position at a specific point in time
   - Assets, Liabilities, and Equity breakdown
   - Supports various periodicity options

2. **Profit & Loss Statement** (`get_profit_and_loss`, `get_income_statement`)
   - Shows financial performance over a period
   - Revenue and expense breakdown
   - Net profit/loss calculation
   - `get_income_statement` is an alias for P&L

3. **Cash Flow Statement** (`get_cash_flow_statement`)
   - Shows cash movements during a period
   - Operating, Investing, and Financing activities
   - Net cash flow calculation

### Detailed Financial Reports

4. **Trial Balance** (`get_trial_balance`)
   - Lists all accounts with their debit and credit balances
   - Ensures accounting equation balance
   - Foundation for other financial statements

5. **General Ledger** (`get_general_ledger`)
   - Detailed transaction history by account
   - Supports filtering by account, party, etc.
   - Most detailed financial report available

### Generic Interface

6. **Financial Statements Dispatcher** (`get_financial_statements`)
   - Generic interface to access any financial report
   - Routes to appropriate specific report method
   - Useful for programmatic access

## Common Parameters

All financial reporting tools accept these common parameters:

- `company` (string, required): The company name for which to generate the report
- `from_date` (string, required): Start date in YYYY-MM-DD format
- `to_date` (string, required): End date in YYYY-MM-DD format
- `periodicity` (string, optional): Report frequency - "Daily", "Weekly", "Monthly", "Quarterly", "Half-yearly", "Yearly"

## Report-Specific Parameters

### General Ledger Additional Parameters

- `account` (string, optional): Filter by specific account
- `party` (string, optional): Filter by specific customer/supplier
- `party_type` (string, optional): "Customer" or "Supplier"
- `group_by` (string, optional): Grouping option

## Usage Examples

### Basic Usage

```python
# Get Balance Sheet
balance_sheet = get_balance_sheet(
    company="My Company",
    from_date="2025-01-01",
    to_date="2025-01-31"
)

# Get Profit & Loss with quarterly periodicity
pnl = get_profit_and_loss(
    company="My Company",
    from_date="2025-01-01", 
    to_date="2025-03-31",
    periodicity="Quarterly"
)
```

### Advanced Filtering

```python
# Get General Ledger for specific account
ledger = get_general_ledger(
    company="My Company",
    from_date="2025-01-01",
    to_date="2025-01-31", 
    account="Cash - MC",
    party="Customer ABC"
)
```

### Using Generic Interface

```python
# Get any report using the dispatcher
report = get_financial_statements(
    company="My Company",
    report_type="Balance Sheet",  # or "Profit and Loss", "Cash Flow"
    from_date="2025-01-01",
    to_date="2025-01-31"
)
```

## Response Format

All financial reporting tools return a standardized JSON response:

```json
{
    "success": true,
    "message": "Balance Sheet retrieved successfully",
    "data": {
        "result": [
            {"account": "Assets", "balance": 100000},
            {"account": "Current Assets", "balance": 60000},
            {"account": "Cash", "balance": 30000}
        ],
        "columns": ["Account", "Balance"],
        "report_name": "Balance Sheet",
        "company": "My Company",
        "from_date": "2025-01-01",
        "to_date": "2025-01-31"
    }
}
```

## Error Handling

The financial reporting tools include robust error handling:

1. **API Failures**: Automatic fallback to alternative ERPNext APIs
2. **Invalid Parameters**: Validation errors with helpful messages
3. **Unsupported Reports**: Clear error messages for invalid report types
4. **Network Issues**: Graceful handling with error responses

Example error response:
```json
{
    "success": false,
    "error_code": "VALIDATION_ERROR",
    "message": "Unsupported report type: Invalid Report. Supported types: Balance Sheet, Profit and Loss, Cash Flow",
    "details": {}
}
```

## Technical Implementation

### ERPNext Integration

The tools integrate with ERPNext's standard reporting system:
- Uses ERPNext's built-in report APIs
- Supports all ERPNext report parameters
- Maintains compatibility with ERPNext versions

### Report Execution

1. **Primary Method**: `frappe.desk.query_report.run` API
2. **Fallback Method**: `frappe.desk.reportview.get_data` API  
3. **Error Handling**: Structured error responses when both methods fail

### MCP Integration

All tools are registered as MCP tools and can be called from:
- Claude Desktop with MCP
- VS Code with MCP extensions
- Custom MCP applications
- Command line MCP clients

## Best Practices

1. **Date Formats**: Always use YYYY-MM-DD format for dates
2. **Company Names**: Use exact company names as configured in ERPNext
3. **Periodicity**: Choose appropriate periodicity for your reporting needs
4. **Error Handling**: Always check the `success` field in responses
5. **Performance**: Use specific report tools rather than the generic dispatcher for better performance

## Troubleshooting

### Common Issues

1. **"Company not found"**: Ensure the company name exactly matches ERPNext
2. **"Report execution failed"**: Check ERPNext connectivity and permissions
3. **"Invalid date range"**: Ensure from_date is before to_date
4. **"No data returned"**: Verify the date range contains transactions

### Debug Information

When reports fail, the response includes:
- Error messages from ERPNext
- Report name and filters used
- Debugging information for troubleshooting

## Related Documentation

- [Main README](../README.md) - Overview of all ERPNext-MCP tools
- [Accounting Operations](../README.md#accounting-operations) - Other accounting tools
- [ERPNext Documentation](https://docs.erpnext.com/) - ERPNext system documentation