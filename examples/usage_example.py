#!/usr/bin/env python3
"""
Example usage of ERPNext MCP Server operations.

This script demonstrates how to use the ERPNext MCP server operations
without actually connecting to an ERPNext instance.
"""

import json
from erpnext_mcp.utils.doctype_mapping import (
    DocTypes,
    get_doctype_for_operation,
    map_business_params_to_doctype_fields,
    validate_required_fields
)
from erpnext_mcp.utils.error_handling import (
    format_success_response,
    format_error_response,
    ERPNextError
)


def example_field_mapping():
    """Demonstrate field mapping functionality."""
    print("=== Field Mapping Examples ===")
    
    # Example 1: Sales Invoice parameters
    invoice_params = {
        "customer_name": "ABC Corporation", 
        "invoice_date": "2025-01-15",
        "grand_total": 1000.0,
        "items": [
            {
                "item_code": "ITEM001",
                "quantity": 10,
                "unit_price": 100.0
            }
        ]
    }
    
    doctype = get_doctype_for_operation("create_sales_invoice")
    mapped_fields = map_business_params_to_doctype_fields(invoice_params, doctype)
    
    print(f"Business operation: create_sales_invoice")
    print(f"DocType: {doctype}")
    print("Original parameters:")
    print(json.dumps(invoice_params, indent=2))
    print("Mapped fields:")
    print(json.dumps(mapped_fields, indent=2))
    print()
    
    # Example 2: Customer parameters
    customer_params = {
        "customer_name": "XYZ Company",
        "customer_email": "contact@xyz.com", 
        "customer_phone": "+1-555-0123"
    }
    
    doctype = get_doctype_for_operation("create_customer")
    mapped_fields = map_business_params_to_doctype_fields(customer_params, doctype)
    
    print(f"Business operation: create_customer")
    print(f"DocType: {doctype}")
    print("Original parameters:")
    print(json.dumps(customer_params, indent=2))
    print("Mapped fields:")
    print(json.dumps(mapped_fields, indent=2))
    print()


def example_validation():
    """Demonstrate field validation."""
    print("=== Field Validation Examples ===")
    
    # Valid customer data
    valid_customer = {
        "customer_name": "Valid Customer",
        "customer_type": "Company"
    }
    missing = validate_required_fields(valid_customer, DocTypes.CUSTOMER)
    print(f"Valid customer data - Missing fields: {missing}")
    
    # Invalid customer data (missing required field)
    invalid_customer = {
        "customer_name": "Invalid Customer"
        # Missing customer_type
    }
    missing = validate_required_fields(invalid_customer, DocTypes.CUSTOMER)
    print(f"Invalid customer data - Missing fields: {missing}")
    print()


def example_response_formatting():
    """Demonstrate response formatting."""
    print("=== Response Formatting Examples ===")
    
    # Success response
    data = {
        "name": "SINV-2025-00001",
        "customer": "ABC Corporation",
        "grand_total": 1000.0,
        "status": "Draft"
    }
    success_response = format_success_response(data, "Sales invoice created successfully")
    print("Success response:")
    print(json.dumps(success_response, indent=2))
    print()
    
    # Error response
    error = ERPNextError(
        "Missing required field: customer_type", 
        "VALIDATION_ERROR",
        {"missing_fields": ["customer_type"]}
    )
    error_response = format_error_response(error)
    print("Error response:")
    print(json.dumps(error_response, indent=2))
    print()


def example_business_operations():
    """Show available business operations and their DocTypes."""
    print("=== Available Business Operations ===")
    
    operations = {
        # Accounting
        "create_sales_invoice": "Create sales invoice",
        "create_purchase_invoice": "Create purchase invoice", 
        "create_payment": "Create payment entry",
        "approve_invoice": "Approve/submit invoice",
        
        # Sales
        "create_sales_order": "Create sales order",
        "create_customer": "Create customer",
        "create_quotation": "Create quotation",
        
        # Purchasing
        "create_purchase_order": "Create purchase order",
        "create_supplier": "Create supplier",
        
        # Inventory
        "create_item": "Create inventory item",
        "create_stock_entry": "Create stock movement entry",
        
        # HR
        "create_employee": "Create employee record",
        "mark_attendance": "Mark employee attendance",
        
        # Projects
        "create_project": "Create project",
        "create_task": "Create task"
    }
    
    for operation, description in operations.items():
        try:
            doctype = get_doctype_for_operation(operation)
            print(f"• {operation:<25} → {doctype:<20} ({description})")
        except ValueError:
            print(f"• {operation:<25} → NOT_MAPPED         ({description})")
    
    print()


if __name__ == "__main__":
    print("ERPNext MCP Server - Usage Examples")
    print("=" * 50)
    print()
    
    example_business_operations()
    example_field_mapping()
    example_validation()
    example_response_formatting()
    
    print("=== Summary ===")
    print("✅ All examples completed successfully!")
    print("✅ The ERPNext MCP Server infrastructure is working correctly.")
    print()
    print("Next steps:")
    print("1. Configure your ERPNext connection in .env file")
    print("2. Run the MCP server: python -m erpnext_mcp.server")
    print("3. Use the business operations to interact with ERPNext")
    print()
    print("Available tools in MCP server:")
    tools = [
        "create_sales_invoice", "approve_sales_invoice", "create_purchase_invoice",
        "create_payment", "create_purchase_order", "create_supplier", 
        "approve_purchase_order", "create_sales_order", "create_customer",
        "create_quotation", "create_item", "create_stock_entry",
        "get_stock_balance", "create_employee", "mark_attendance",
        "create_project", "create_task", "log_time", "search_customers",
        "search_suppliers", "search_items", "get_sales_orders_list",
        "get_purchase_orders_list", "get_invoices_list"
    ]
    
    for i, tool in enumerate(tools, 1):
        print(f"{i:2d}. {tool}")