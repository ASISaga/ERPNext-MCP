# ERPNext MCP Server

A comprehensive Python MCP (Model Context Protocol) server exposing all major ERPNext operations in business-friendly terms. Built using frappe-client under the hood and organized by domain modules.

## Features

- **Business-Friendly Operations**: Operations are exposed using familiar business terms (e.g., `create_purchase_order`, `approve_invoice`) instead of technical DocType names
- **Domain-Based Organization**: Operations are organized into logical business domains:
  - **Accounting**: Invoices, payments, journal entries
  - **Purchasing**: Purchase orders, suppliers, receipts  
  - **Sales**: Sales orders, customers, quotations
  - **Inventory**: Items, stock entries, warehouses
  - **HR**: Employees, attendance, leave applications
  - **Projects**: Projects, tasks, timesheets
- **Comprehensive Error Handling**: Proper error mapping and JSON responses
- **Field Mapping**: Automatic conversion between business parameter names and ERPNext field names
- **JSON Results**: All operations return structured JSON responses

## Installation

```bash
pip install -r requirements.txt
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

#### Purchasing Operations

- `create_purchase_order(supplier, items, schedule_date)` - Create purchase order
- `create_supplier(supplier_name, supplier_type)` - Create new supplier
- `approve_purchase_order(po_name)` - Approve/submit purchase order

#### Sales Operations

- `create_sales_order(customer, items, delivery_date)` - Create sales order
- `create_customer(customer_name, customer_type)` - Create new customer
- `create_quotation(quotation_to, party_name, items)` - Create sales quotation

#### Inventory Operations

- `create_item(item_code, item_name, item_group)` - Create new item
- `create_stock_entry(stock_entry_type, items)` - Create stock movement entry
- `get_stock_balance(item_code, warehouse)` - Get item stock balance

#### HR Operations

- `create_employee(employee_name, date_of_joining)` - Create employee record
- `mark_attendance(employee, attendance_date, status)` - Mark employee attendance

#### Project Operations

- `create_project(project_name)` - Create new project
- `create_task(subject, project, priority)` - Create new task
- `log_time(employee, hours, activity_type, from_time, to_time)` - Log time in timesheet

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
│   ├── accounting.py        # Accounting operations
│   ├── purchasing.py        # Purchasing operations
│   ├── sales.py            # Sales operations
│   ├── inventory.py        # Inventory operations
│   ├── hr.py              # HR operations
│   └── projects.py        # Project operations
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