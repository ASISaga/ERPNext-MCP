"""Main ERPNext MCP Server implementation."""

import logging
import asyncio
from typing import Any, Dict, List, Optional, Sequence
from mcp.server.fastmcp import FastMCP
from mcp.shared.exceptions import McpError
from pydantic import BaseModel

from .client.frappe_client import ERPNextClient
from .config import config
from .domains.accounting import AccountingOperations
from .domains.purchasing import PurchasingOperations
from .domains.sales import SalesOperations
from .domains.inventory import InventoryOperations
from .domains.hr import HROperations
from .domains.projects import ProjectsOperations
from .utils.error_handling import ERPNextError, format_error_response


# Configure logging
logging.basicConfig(level=getattr(logging, config.log_level))
logger = logging.getLogger(__name__)

# Initialize MCP server
app = FastMCP(name=config.server_name)

# Global ERPNext client and operations
client: Optional[ERPNextClient] = None
accounting: Optional[AccountingOperations] = None
purchasing: Optional[PurchasingOperations] = None
sales: Optional[SalesOperations] = None
inventory: Optional[InventoryOperations] = None
hr: Optional[HROperations] = None
projects: Optional[ProjectsOperations] = None


def initialize_client():
    """Initialize ERPNext client and domain operations."""
    global client, accounting, purchasing, sales, inventory, hr, projects
    
    try:
        client = ERPNextClient()
        
        # Initialize domain operations
        accounting = AccountingOperations(client)
        purchasing = PurchasingOperations(client)
        sales = SalesOperations(client)
        inventory = InventoryOperations(client)
        hr = HROperations(client)
        projects = ProjectsOperations(client)
        
        logger.info("ERPNext MCP Server initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize ERPNext client: {str(e)}")
        raise


def handle_operation_error(func):
    """Decorator to handle operation errors and convert to MCP format."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ERPNextError as e:
            logger.error(f"ERPNext error in {func.__name__}: {str(e)}")
            return format_error_response(e)
        except Exception as e:
            logger.error(f"Unexpected error in {func.__name__}: {str(e)}")
            error = ERPNextError(f"Operation failed: {str(e)}")
            return format_error_response(error)
    return wrapper


# Accounting Tools
@app.tool()
@handle_operation_error
def create_sales_invoice(customer: str, items: List[Dict[str, Any]], posting_date: str = None, due_date: str = None) -> Dict[str, Any]:
    """Create a sales invoice for a customer.
    
    Args:
        customer: Customer name or ID
        items: List of invoice items with item_code, qty, rate
        posting_date: Invoice date (YYYY-MM-DD format)
        due_date: Payment due date (YYYY-MM-DD format)
    """
    return accounting.create_sales_invoice(customer, items, posting_date, due_date)


@app.tool()
@handle_operation_error
def approve_sales_invoice(invoice_name: str) -> Dict[str, Any]:
    """Approve (submit) a sales invoice.
    
    Args:
        invoice_name: Sales invoice name/ID to approve
    """
    return accounting.approve_sales_invoice(invoice_name)


@app.tool()
@handle_operation_error
def create_purchase_invoice(supplier: str, items: List[Dict[str, Any]], posting_date: str = None, due_date: str = None) -> Dict[str, Any]:
    """Create a purchase invoice for a supplier.
    
    Args:
        supplier: Supplier name or ID
        items: List of invoice items with item_code, qty, rate
        posting_date: Invoice date (YYYY-MM-DD format)
        due_date: Payment due date (YYYY-MM-DD format)
    """
    return accounting.create_purchase_invoice(supplier, items, posting_date, due_date)


@app.tool()
@handle_operation_error
def create_payment(payment_type: str, party_type: str, party: str, paid_amount: float) -> Dict[str, Any]:
    """Create a payment entry.
    
    Args:
        payment_type: "Receive" or "Pay"
        party_type: "Customer" or "Supplier"
        party: Party name
        paid_amount: Payment amount
    """
    return accounting.create_payment(payment_type, party_type, party, paid_amount)


# Purchasing Tools
@app.tool()
@handle_operation_error
def create_purchase_order(supplier: str, items: List[Dict[str, Any]], schedule_date: str = None) -> Dict[str, Any]:
    """Create a purchase order for a supplier.
    
    Args:
        supplier: Supplier name or ID
        items: List of items with item_code, qty, rate
        schedule_date: Expected delivery date (YYYY-MM-DD format)
    """
    return purchasing.create_purchase_order(supplier, items, schedule_date)


@app.tool()
@handle_operation_error
def create_supplier(supplier_name: str, supplier_type: str = "Company") -> Dict[str, Any]:
    """Create a new supplier.
    
    Args:
        supplier_name: Supplier name
        supplier_type: "Company" or "Individual"
    """
    return purchasing.create_supplier(supplier_name, supplier_type)


@app.tool()
@handle_operation_error
def approve_purchase_order(po_name: str) -> Dict[str, Any]:
    """Approve (submit) a purchase order.
    
    Args:
        po_name: Purchase order name/ID to approve
    """
    return purchasing.approve_purchase_order(po_name)


# Sales Tools
@app.tool()
@handle_operation_error
def create_sales_order(customer: str, items: List[Dict[str, Any]], delivery_date: str = None) -> Dict[str, Any]:
    """Create a sales order for a customer.
    
    Args:
        customer: Customer name or ID
        items: List of items with item_code, qty, rate
        delivery_date: Expected delivery date (YYYY-MM-DD format)
    """
    return sales.create_sales_order(customer, items, delivery_date)


@app.tool()
@handle_operation_error
def create_customer(customer_name: str, customer_type: str = "Company") -> Dict[str, Any]:
    """Create a new customer.
    
    Args:
        customer_name: Customer name
        customer_type: "Company" or "Individual"
    """
    return sales.create_customer(customer_name, customer_type)


@app.tool()
@handle_operation_error
def create_quotation(quotation_to: str, party_name: str, items: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Create a sales quotation.
    
    Args:
        quotation_to: "Customer" or "Lead"
        party_name: Customer or lead name
        items: List of items with item_code, qty, rate
    """
    return sales.create_quotation(quotation_to, party_name, items)


# Inventory Tools
@app.tool()
@handle_operation_error
def create_item(item_code: str, item_name: str, item_group: str) -> Dict[str, Any]:
    """Create a new inventory item.
    
    Args:
        item_code: Unique item code
        item_name: Item name
        item_group: Item group
    """
    return inventory.create_item(item_code, item_name, item_group)


@app.tool()
@handle_operation_error
def create_stock_entry(stock_entry_type: str, items: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Create a stock entry for inventory movement.
    
    Args:
        stock_entry_type: Type like "Material Issue", "Material Receipt", "Material Transfer"
        items: List of items with item_code, qty, warehouse info
    """
    return inventory.create_stock_entry(stock_entry_type, items)


@app.tool()
@handle_operation_error
def get_stock_balance(item_code: str, warehouse: str = None) -> Dict[str, Any]:
    """Get stock balance for an item.
    
    Args:
        item_code: Item code
        warehouse: Specific warehouse (optional)
    """
    return inventory.get_stock_balance(item_code, warehouse)


# HR Tools
@app.tool()
@handle_operation_error
def create_employee(employee_name: str, date_of_joining: str) -> Dict[str, Any]:
    """Create a new employee record.
    
    Args:
        employee_name: Employee full name
        date_of_joining: Join date (YYYY-MM-DD format)
    """
    return hr.create_employee(employee_name, date_of_joining)


@app.tool()
@handle_operation_error
def mark_attendance(employee: str, attendance_date: str, status: str) -> Dict[str, Any]:
    """Mark attendance for an employee.
    
    Args:
        employee: Employee ID
        attendance_date: Attendance date (YYYY-MM-DD format)
        status: "Present", "Absent", "Half Day"
    """
    return hr.mark_attendance(employee, attendance_date, status)


# Project Tools
@app.tool()
@handle_operation_error
def create_project(project_name: str) -> Dict[str, Any]:
    """Create a new project.
    
    Args:
        project_name: Project name
    """
    return projects.create_project(project_name)


@app.tool()
@handle_operation_error
def create_task(subject: str, project: str = None, priority: str = "Medium") -> Dict[str, Any]:
    """Create a new task.
    
    Args:
        subject: Task title/subject
        project: Associated project (optional)
        priority: "Low", "Medium", "High", "Urgent"
    """
    return projects.create_task(subject, project, priority)


@app.tool()
@handle_operation_error
def log_time(employee: str, hours: float, activity_type: str, from_time: str, to_time: str) -> Dict[str, Any]:
    """Log time in a timesheet.
    
    Args:
        employee: Employee ID
        hours: Hours worked
        activity_type: Type of activity
        from_time: Start time (HH:MM format)
        to_time: End time (HH:MM format)
    """
    return projects.log_time(employee, hours, activity_type, from_time, to_time)


# Search and List Tools
@app.tool()
@handle_operation_error
def search_customers(query: str, limit: int = 10) -> Dict[str, Any]:
    """Search customers by name.
    
    Args:
        query: Search query
        limit: Maximum number of results
    """
    return sales.search_customers(query, limit)


@app.tool()
@handle_operation_error
def search_suppliers(query: str, limit: int = 10) -> Dict[str, Any]:
    """Search suppliers by name.
    
    Args:
        query: Search query
        limit: Maximum number of results
    """
    return purchasing.search_suppliers(query, limit)


@app.tool()
@handle_operation_error
def search_items(query: str, limit: int = 10) -> Dict[str, Any]:
    """Search items by code or name.
    
    Args:
        query: Search query
        limit: Maximum number of results
    """
    return inventory.search_items(query, limit)


@app.tool()
@handle_operation_error
def get_sales_orders_list(limit: int = 20) -> Dict[str, Any]:
    """Get list of sales orders.
    
    Args:
        limit: Maximum number of records
    """
    return sales.get_sales_orders_list(limit=limit)


@app.tool()
@handle_operation_error
def get_purchase_orders_list(limit: int = 20) -> Dict[str, Any]:
    """Get list of purchase orders.
    
    Args:
        limit: Maximum number of records
    """
    return purchasing.get_purchase_orders_list(limit=limit)


@app.tool()
@handle_operation_error
def get_invoices_list(invoice_type: str, limit: int = 20) -> Dict[str, Any]:
    """Get list of invoices.
    
    Args:
        invoice_type: "sales" or "purchase"
        limit: Maximum number of records
    """
    return accounting.get_invoices_list(invoice_type, limit=limit)


def main():
    """Main entry point for the ERPNext MCP Server."""
    # Initialize the client
    initialize_client()
    
    # Run the server
    import mcp.server.stdio
    mcp.server.stdio.run_server(app)


if __name__ == "__main__":
    main()