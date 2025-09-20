# ERPNext MCP Server

A comprehensive Python MCP (Model Context Protocol) server exposing all major ERPNext operations in business-friendly terms. Built using frappe-client under the hood and organized by domain modules.

## Features

- **Business-Friendly Operations**: Operations are exposed using familiar business terms (e.g., `create_purchase_order`, `approve_invoice`) instead of technical DocType names
- **Domain-Based Organization**: Operations are organized into logical business domains:
  - **Accounting**: Invoices, payments, journal entries, cost centers, budgets, financial statements
  - **Purchasing**: Purchase orders, suppliers, receipts, returns  
  - **Sales**: Sales orders, customers, quotations, delivery notes, returns
  - **Inventory**: Items, stock entries, warehouses, price lists, batch/serial tracking
  - **HR**: Employees, attendance, leave applications, payroll, recruitment
  - **Projects**: Projects, tasks, timesheets
  - **Manufacturing**: BOMs, work orders, production planning, quality inspection
  - **CRM**: Leads, opportunities, campaigns, conversions
  - **Asset Management**: Asset tracking, maintenance, depreciation
  - **Support/Service**: Issue tracking, warranty claims, SLA management
  - **Utilities/Integration**: Workflows, custom fields, reports, bulk operations
- **Comprehensive Error Handling**: Proper error mapping and JSON responses
- **Field Mapping**: Automatic conversion between business parameter names and ERPNext field names
- **JSON Results**: All operations return structured JSON responses

## Installation


```bash
pip install .
```

Or install the package:

```bash
pip install -e .
```

## Configuration

Create a `.env` file in the project root:

```env
ERPNEXT_URL=http://your-erpnext-site.com
ERPNEXT_USERNAME=your_username
ERPNEXT_PASSWORD=your_password
# OR use API keys
ERPNEXT_API_KEY=your_api_key
ERPNEXT_API_SECRET=your_api_secret

# Optional settings
ERPNEXT_VERIFY_SSL=true
ERPNEXT_SERVER_HOST=localhost
ERPNEXT_SERVER_PORT=8080
ERPNEXT_LOG_LEVEL=INFO
```

## Usage

### Running the MCP Server

```bash
python -m erpnext_mcp.server
# OR
erpnext-mcp
```

### Available Operations

#### Accounting Operations

- `create_sales_invoice(customer, items, posting_date, due_date)` - Create sales invoice
- `create_purchase_invoice(supplier, items, posting_date, due_date)` - Create purchase invoice  
- `approve_sales_invoice(invoice_name)` - Approve/submit sales invoice
- `create_payment(payment_type, party_type, party, paid_amount)` - Create payment entry
- `create_cost_center(cost_center_name, parent_cost_center)` - Create cost center
- `create_budget(cost_center, fiscal_year, accounts)` - Create budget
- `create_fiscal_year(year, year_start_date, year_end_date)` - Create fiscal year

##### Financial Reporting Operations
- `get_financial_statements(company, report_type, from_date, to_date)` - Get financial reports (general)
- `get_balance_sheet(company, from_date, to_date, periodicity)` - Get Balance Sheet report
- `get_profit_and_loss(company, from_date, to_date, periodicity)` - Get Profit & Loss Statement
- `get_income_statement(company, from_date, to_date, periodicity)` - Get Income Statement (alias for P&L)
- `get_cash_flow_statement(company, from_date, to_date, periodicity)` - Get Cash Flow Statement
- `get_trial_balance(company, from_date, to_date, periodicity)` - Get Trial Balance report
- `get_general_ledger(company, from_date, to_date, account, party)` - Get General Ledger report

#### Purchasing Operations

- `create_purchase_order(supplier, items, schedule_date)` - Create purchase order
- `create_supplier(supplier_name, supplier_type)` - Create new supplier
- `approve_purchase_order(po_name)` - Approve/submit purchase order
- `create_purchase_receipt(supplier, items, posting_date)` - Create goods receipt
- `create_purchase_return(return_against, items)` - Create purchase return
- `submit_purchase_receipt(pr_name)` - Submit purchase receipt
- `get_purchase_receipts_list(supplier, status, limit)` - Get receipts list

#### Sales Operations

- `create_sales_order(customer, items, delivery_date)` - Create sales order
- `create_customer(customer_name, customer_type)` - Create new customer
- `create_quotation(quotation_to, party_name, items)` - Create sales quotation
- `create_delivery_note(customer, items, posting_date)` - Create delivery note
- `create_sales_return(return_against, items)` - Create sales return
- `submit_delivery_note(dn_name)` - Submit delivery note
- `get_delivery_notes_list(customer, status, limit)` - Get delivery notes list

#### Inventory Operations

- `create_item(item_code, item_name, item_group)` - Create new item
- `create_stock_entry(stock_entry_type, items)` - Create stock movement entry
- `get_stock_balance(item_code, warehouse)` - Get item stock balance
- `create_item_price(item_code, price_list, price_list_rate)` - Create item price
- `create_price_list(price_list_name, currency)` - Create price list
- `create_batch(batch_id, item)` - Create batch for tracking
- `create_serial_no(serial_no, item_code)` - Create serial number
- `get_stock_report(warehouse, item_group, limit)` - Get stock report

#### HR Operations

- `create_employee(employee_name, date_of_joining)` - Create employee record
- `mark_attendance(employee, attendance_date, status)` - Mark employee attendance
- `create_leave_application(employee, leave_type, from_date, to_date)` - Create leave application
- `create_salary_structure(name, company, employee)` - Create salary structure
- `create_salary_slip(employee, start_date, end_date)` - Create salary slip
- `create_job_applicant(applicant_name, job_title)` - Create job applicant
- `approve_leave_application(leave_application_name)` - Approve leave

#### Project Operations

- `create_project(project_name)` - Create new project
- `create_task(subject, project, priority)` - Create new task
- `log_time(employee, hours, activity_type, from_time, to_time)` - Log time in timesheet

#### Manufacturing Operations

- `create_bom(item, items, quantity)` - Create Bill of Materials
- `create_work_order(production_item, bom_no, qty, planned_start_date)` - Create work order
- `create_production_plan(company, for_warehouse, items)` - Create production plan
- `start_work_order(work_order_name)` - Start work order
- `complete_work_order(work_order_name)` - Complete work order
- `create_quality_inspection(inspection_type, reference_type, reference_name, item_code)` - Create quality inspection
- `get_work_orders_list(status, limit)` - Get work orders list

#### CRM Operations

- `create_lead(lead_name, status)` - Create new lead
- `create_opportunity(opportunity_from, party_name, opportunity_type)` - Create opportunity
- `create_campaign(campaign_name)` - Create marketing campaign
- `convert_lead_to_customer(lead_name)` - Convert lead to customer
- `convert_lead_to_opportunity(lead_name)` - Convert lead to opportunity
- `update_opportunity_status(opportunity_name, status)` - Update opportunity status
- `search_leads(query, limit)` - Search leads

#### Asset Management Operations

- `create_asset(asset_name, asset_category, item_code)` - Create asset
- `create_asset_category(asset_category_name, total_number_of_depreciations, frequency_of_depreciation)` - Create asset category
- `create_asset_maintenance(asset, maintenance_type, periodicity)` - Create maintenance schedule
- `transfer_asset(asset, target_location, to_employee)` - Transfer asset
- `create_asset_depreciation(asset)` - Create depreciation entry
- `get_assets_list(asset_category, status, limit)` - Get assets list

#### Support/Service Operations

- `create_issue(subject, customer, issue_type, priority)` - Create support issue
- `create_service_level_agreement(service_level, customer, start_date, end_date)` - Create SLA
- `create_warranty_claim(customer, item_code, serial_no)` - Create warranty claim
- `update_issue_status(issue_name, status)` - Update issue status
- `assign_issue(issue_name, assigned_to)` - Assign issue to user
- `close_issue(issue_name, resolution)` - Close issue with resolution
- `get_issues_list(customer, status, priority, limit)` - Get issues list
- `search_issues(query, limit)` - Search issues

#### Utilities/Integration Operations

- `create_workflow(workflow_name, document_type, states, transitions)` - Create approval workflow
- `create_custom_field(dt, fieldname, fieldtype, label)` - Add custom field to DocType
- `backup_database()` - Create database backup
- `execute_report(report_name, filters)` - Execute system report
- `bulk_update_documents(doctype, filters, update_fields)` - Bulk update documents
- `get_system_settings()` - Get system configuration
- `get_document_permissions(doctype, name)` - Get document permissions

#### Search and List Operations

- `search_customers(query, limit)` - Search customers
- `search_suppliers(query, limit)` - Search suppliers
- `search_items(query, limit)` - Search items
- `get_sales_orders_list(limit)` - Get sales orders list
- `get_purchase_orders_list(limit)` - Get purchase orders list
- `get_invoices_list(invoice_type, limit)` - Get invoices list

## Example Usage

### Creating a Sales Invoice

```python
# Create a sales invoice
result = create_sales_invoice(
    customer="ABC Corporation",
    items=[
        {
            "item_code": "ITEM001",
            "qty": 10,
            "rate": 100.0
        }
    ],
    posting_date="2025-01-15",
    due_date="2025-02-15"
)

# Approve the invoice
approve_result = approve_sales_invoice(result["data"]["name"])
```

### Creating a Purchase Order

```python
# Create a purchase order
po_result = create_purchase_order(
    supplier="XYZ Supplier",
    items=[
        {
            "item_code": "RAW001", 
            "qty": 50,
            "rate": 25.0
        }
    ],
    schedule_date="2025-01-20"
)

# Approve the purchase order
approve_result = approve_purchase_order(po_result["data"]["name"])
```

### Financial Reporting

```python
# Get Balance Sheet for a company
balance_sheet = get_balance_sheet(
    company="ABC Corporation",
    from_date="2025-01-01",
    to_date="2025-01-31",
    periodicity="Monthly"
)

# Get Profit and Loss Statement
profit_loss = get_profit_and_loss(
    company="ABC Corporation", 
    from_date="2025-01-01",
    to_date="2025-01-31",
    periodicity="Monthly"
)

# Get Cash Flow Statement
cash_flow = get_cash_flow_statement(
    company="ABC Corporation",
    from_date="2025-01-01", 
    to_date="2025-01-31",
    periodicity="Monthly"
)

# Get Trial Balance
trial_balance = get_trial_balance(
    company="ABC Corporation",
    from_date="2025-01-01",
    to_date="2025-01-31"
)

# Get General Ledger with filters
general_ledger = get_general_ledger(
    company="ABC Corporation",
    from_date="2025-01-01",
    to_date="2025-01-31",
    account="Cash - ABC",
    party="Customer XYZ"
)

# Use the general financial statements method
statements = get_financial_statements(
    company="ABC Corporation",
    report_type="Balance Sheet",
    from_date="2025-01-01",
    to_date="2025-01-31"
)
```

## Response Format

All operations return a standardized JSON response:

```json
{
    "success": true,
    "message": "Operation completed successfully",
    "data": {
        // ERPNext document data
    }
}
```

Error responses:

```json
{
    "success": false,
    "error_code": "VALIDATION_ERROR",
    "message": "Missing required fields: customer, items",
    "details": {
        // Additional error details
    }
}
```

## Project Structure

```
erpnext_mcp/
├── __init__.py
├── server.py                 # Main MCP server implementation
├── config.py                # Configuration management
├── client/
│   ├── __init__.py
│   └── frappe_client.py     # Enhanced Frappe client wrapper
├── domains/                 # Business domain modules
│   ├── __init__.py
│   ├── accounting.py        # Accounting operations (invoices, payments, budgets)
│   ├── purchasing.py        # Purchasing operations
│   ├── sales.py            # Sales operations
│   ├── inventory.py        # Inventory operations (stock, pricing, batches)
│   ├── hr.py              # HR operations (employees, payroll, recruitment)
│   ├── projects.py        # Project operations
│   ├── manufacturing.py   # Manufacturing operations (BOM, work orders)
│   ├── crm.py            # CRM operations (leads, opportunities)
│   ├── assets.py         # Asset management operations
│   ├── support.py        # Support/Service operations
│   └── utilities.py      # Utilities and integration operations
└── utils/
    ├── __init__.py
    ├── doctype_mapping.py   # DocType and field mappings
    └── error_handling.py    # Error handling utilities
```

## Development

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black erpnext_mcp/
isort erpnext_mcp/
```

### Type Checking

```bash
mypy erpnext_mcp/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run the linting and tests
6. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions, please open a GitHub issue.