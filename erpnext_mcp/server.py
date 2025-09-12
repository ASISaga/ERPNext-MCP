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
from .domains.manufacturing import ManufacturingOperations
from .domains.crm import CRMOperations
from .domains.assets import AssetManagementOperations
from .domains.support import SupportOperations
from .domains.utilities import UtilitiesOperations
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
manufacturing: Optional[ManufacturingOperations] = None
crm: Optional[CRMOperations] = None
assets: Optional[AssetManagementOperations] = None
support: Optional[SupportOperations] = None
utilities: Optional[UtilitiesOperations] = None


def initialize_client():
    """Initialize ERPNext client and domain operations."""
    global client, accounting, purchasing, sales, inventory, hr, projects, manufacturing, crm, assets, support, utilities

    try:
        client = ERPNextClient()

        # Initialize domain operations
        accounting = AccountingOperations(client)
        purchasing = PurchasingOperations(client)
        sales = SalesOperations(client)
        inventory = InventoryOperations(client)
        hr = HROperations(client)
        projects = ProjectsOperations(client)
        manufacturing = ManufacturingOperations(client)
        crm = CRMOperations(client)
        assets = AssetManagementOperations(client)
        support = SupportOperations(client)
        utilities = UtilitiesOperations(client)

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
def create_sales_invoice(
    customer: str,
    items: List[Dict[str, Any]],
    posting_date: str = None,
    due_date: str = None,
) -> Dict[str, Any]:
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
def create_purchase_invoice(
    supplier: str,
    items: List[Dict[str, Any]],
    posting_date: str = None,
    due_date: str = None,
) -> Dict[str, Any]:
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
def create_payment(
    payment_type: str, party_type: str, party: str, paid_amount: float
) -> Dict[str, Any]:
    """Create a payment entry.

    Args:
        payment_type: "Receive" or "Pay"
        party_type: "Customer" or "Supplier"
        party: Party name
        paid_amount: Payment amount
    """
    return accounting.create_payment(payment_type, party_type, party, paid_amount)


@app.tool()
@handle_operation_error
def create_cost_center(
    cost_center_name: str, parent_cost_center: str = "All Cost Centers - "
) -> Dict[str, Any]:
    """Create a new cost center for accounting.

    Args:
        cost_center_name: Cost center name
        parent_cost_center: Parent cost center
    """
    return accounting.create_cost_center(cost_center_name, parent_cost_center)


@app.tool()
@handle_operation_error
def create_budget(
    cost_center: str, fiscal_year: str, accounts: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Create a budget for cost center.

    Args:
        cost_center: Cost center name
        fiscal_year: Fiscal year
        accounts: List of accounts with budget amounts
    """
    return accounting.create_budget(cost_center, fiscal_year, accounts)


@app.tool()
@handle_operation_error
def create_fiscal_year(
    year: str, year_start_date: str, year_end_date: str
) -> Dict[str, Any]:
    """Create a fiscal year.

    Args:
        year: Fiscal year name
        year_start_date: Start date (YYYY-MM-DD format)
        year_end_date: End date (YYYY-MM-DD format)
    """
    return accounting.create_fiscal_year(year, year_start_date, year_end_date)


@app.tool()
@handle_operation_error
def get_financial_statements(
    company: str, report_type: str, from_date: str, to_date: str
) -> Dict[str, Any]:
    """Get financial statements.

    Args:
        company: Company name
        report_type: "Balance Sheet", "Profit and Loss", "Cash Flow"
        from_date: From date (YYYY-MM-DD format)
        to_date: To date (YYYY-MM-DD format)
    """
    return accounting.get_financial_statements(company, report_type, from_date, to_date)


@app.tool()
@handle_operation_error
def get_balance_sheet(
    company: str, from_date: str, to_date: str, periodicity: str = "Monthly"
) -> Dict[str, Any]:
    """Get Balance Sheet report for a company.

    Args:
        company: Company name
        from_date: From date (YYYY-MM-DD format)
        to_date: To date (YYYY-MM-DD format)
        periodicity: Report periodicity ("Daily", "Weekly", "Monthly", "Quarterly", "Half-yearly", "Yearly")
    """
    return accounting.get_balance_sheet(company, from_date, to_date, periodicity=periodicity)


@app.tool()
@handle_operation_error
def get_profit_and_loss(
    company: str, from_date: str, to_date: str, periodicity: str = "Monthly"
) -> Dict[str, Any]:
    """Get Profit and Loss Statement (Income Statement) for a company.

    Args:
        company: Company name
        from_date: From date (YYYY-MM-DD format)
        to_date: To date (YYYY-MM-DD format)
        periodicity: Report periodicity ("Daily", "Weekly", "Monthly", "Quarterly", "Half-yearly", "Yearly")
    """
    return accounting.get_profit_and_loss(company, from_date, to_date, periodicity=periodicity)


@app.tool()
@handle_operation_error
def get_income_statement(
    company: str, from_date: str, to_date: str, periodicity: str = "Monthly"
) -> Dict[str, Any]:
    """Get Income Statement (alias for Profit and Loss Statement) for a company.

    Args:
        company: Company name
        from_date: From date (YYYY-MM-DD format)
        to_date: To date (YYYY-MM-DD format)
        periodicity: Report periodicity ("Daily", "Weekly", "Monthly", "Quarterly", "Half-yearly", "Yearly")
    """
    return accounting.get_profit_and_loss(company, from_date, to_date, periodicity=periodicity)


@app.tool()
@handle_operation_error
def get_cash_flow_statement(
    company: str, from_date: str, to_date: str, periodicity: str = "Monthly"
) -> Dict[str, Any]:
    """Get Cash Flow Statement for a company.

    Args:
        company: Company name
        from_date: From date (YYYY-MM-DD format)
        to_date: To date (YYYY-MM-DD format)
        periodicity: Report periodicity ("Daily", "Weekly", "Monthly", "Quarterly", "Half-yearly", "Yearly")
    """
    return accounting.get_cash_flow(company, from_date, to_date, periodicity=periodicity)


@app.tool()
@handle_operation_error
def get_trial_balance(
    company: str, from_date: str, to_date: str, periodicity: str = "Monthly"
) -> Dict[str, Any]:
    """Get Trial Balance report for a company.

    Args:
        company: Company name
        from_date: From date (YYYY-MM-DD format)
        to_date: To date (YYYY-MM-DD format)
        periodicity: Report periodicity ("Daily", "Weekly", "Monthly", "Quarterly", "Half-yearly", "Yearly")
    """
    return accounting.get_trial_balance(company, from_date, to_date, periodicity=periodicity)


@app.tool()
@handle_operation_error
def get_general_ledger(
    company: str, from_date: str, to_date: str, account: str = None, party: str = None
) -> Dict[str, Any]:
    """Get General Ledger report for a company.

    Args:
        company: Company name
        from_date: From date (YYYY-MM-DD format)
        to_date: To date (YYYY-MM-DD format)
        account: Filter by specific account (optional)
        party: Filter by specific party/customer/supplier (optional)
    """
    return accounting.get_general_ledger(company, from_date, to_date, account=account, party=party)


# Purchasing Tools
@app.tool()
@handle_operation_error
def create_purchase_order(
    supplier: str, items: List[Dict[str, Any]], schedule_date: str = None
) -> Dict[str, Any]:
    """Create a purchase order for a supplier.

    Args:
        supplier: Supplier name or ID
        items: List of items with item_code, qty, rate
        schedule_date: Expected delivery date (YYYY-MM-DD format)
    """
    return purchasing.create_purchase_order(supplier, items, schedule_date)


@app.tool()
@handle_operation_error
def create_supplier(
    supplier_name: str, supplier_type: str = "Company"
) -> Dict[str, Any]:
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


@app.tool()
@handle_operation_error
def create_purchase_receipt(
    supplier: str, items: List[Dict[str, Any]], posting_date: str = None
) -> Dict[str, Any]:
    """Create a purchase receipt for goods received.

    Args:
        supplier: Supplier name or ID
        items: List of items received with item_code, qty, rate, warehouse
        posting_date: Receipt date (YYYY-MM-DD format)
    """
    return purchasing.create_purchase_receipt(supplier, items, posting_date)


@app.tool()
@handle_operation_error
def create_purchase_return(
    return_against: str, items: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Create a purchase return against a purchase receipt.

    Args:
        return_against: Original purchase receipt name
        items: List of items being returned with item_code, qty
    """
    return purchasing.create_purchase_return(return_against, items)


@app.tool()
@handle_operation_error
def submit_purchase_receipt(pr_name: str) -> Dict[str, Any]:
    """Submit/approve a purchase receipt.

    Args:
        pr_name: Purchase receipt name/ID to submit
    """
    return purchasing.submit_purchase_receipt(pr_name)


@app.tool()
@handle_operation_error
def get_purchase_receipts_list(
    supplier: str = None, status: str = None, limit: int = 20
) -> Dict[str, Any]:
    """Get list of purchase receipts.

    Args:
        supplier: Filter by supplier (optional)
        status: Filter by status (optional)
        limit: Maximum number of records
    """
    return purchasing.get_purchase_receipts_list(supplier, status, limit)


# Sales Tools
@app.tool()
@handle_operation_error
def create_sales_order(
    customer: str, items: List[Dict[str, Any]], delivery_date: str = None
) -> Dict[str, Any]:
    """Create a sales order for a customer.

    Args:
        customer: Customer name or ID
        items: List of items with item_code, qty, rate
        delivery_date: Expected delivery date (YYYY-MM-DD format)
    """
    return sales.create_sales_order(customer, items, delivery_date)


@app.tool()
@handle_operation_error
def create_customer(
    customer_name: str, customer_type: str = "Company"
) -> Dict[str, Any]:
    """Create a new customer.

    Args:
        customer_name: Customer name
        customer_type: "Company" or "Individual"
    """
    return sales.create_customer(customer_name, customer_type)


@app.tool()
@handle_operation_error
def create_quotation(
    quotation_to: str, party_name: str, items: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Create a sales quotation.

    Args:
        quotation_to: "Customer" or "Lead"
        party_name: Customer or lead name
        items: List of items with item_code, qty, rate
    """
    return sales.create_quotation(quotation_to, party_name, items)


@app.tool()
@handle_operation_error
def create_delivery_note(
    customer: str, items: List[Dict[str, Any]], posting_date: str = None
) -> Dict[str, Any]:
    """Create a delivery note for goods delivery.

    Args:
        customer: Customer name or ID
        items: List of items with item_code, qty, warehouse
        posting_date: Delivery date (YYYY-MM-DD format)
    """
    return sales.create_delivery_note(customer, items, posting_date)


@app.tool()
@handle_operation_error
def create_sales_return(
    return_against: str, items: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Create a sales return against a delivery note or sales invoice.

    Args:
        return_against: Original delivery note or sales invoice name
        items: List of items being returned with item_code, qty
    """
    return sales.create_sales_return(return_against, items)


@app.tool()
@handle_operation_error
def submit_delivery_note(dn_name: str) -> Dict[str, Any]:
    """Submit/approve a delivery note.

    Args:
        dn_name: Delivery note name/ID to submit
    """
    return sales.submit_delivery_note(dn_name)


@app.tool()
@handle_operation_error
def get_delivery_notes_list(
    customer: str = None, status: str = None, limit: int = 20
) -> Dict[str, Any]:
    """Get list of delivery notes.

    Args:
        customer: Filter by customer (optional)
        status: Filter by status (optional)
        limit: Maximum number of records
    """
    return sales.get_delivery_notes_list(customer, status, limit)


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
def create_stock_entry(
    stock_entry_type: str, items: List[Dict[str, Any]]
) -> Dict[str, Any]:
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


@app.tool()
@handle_operation_error
def create_item_price(
    item_code: str, price_list: str, price_list_rate: float
) -> Dict[str, Any]:
    """Create an item price for a price list.

    Args:
        item_code: Item code
        price_list: Price list name
        price_list_rate: Rate/price
    """
    return inventory.create_item_price(item_code, price_list, price_list_rate)


@app.tool()
@handle_operation_error
def create_price_list(price_list_name: str, currency: str) -> Dict[str, Any]:
    """Create a price list.

    Args:
        price_list_name: Price list name
        currency: Currency code (e.g., "USD", "INR")
    """
    return inventory.create_price_list(price_list_name, currency)


@app.tool()
@handle_operation_error
def create_batch(batch_id: str, item: str) -> Dict[str, Any]:
    """Create a batch for batch tracking.

    Args:
        batch_id: Batch ID
        item: Item code
    """
    return inventory.create_batch(batch_id, item)


@app.tool()
@handle_operation_error
def create_serial_no(serial_no: str, item_code: str) -> Dict[str, Any]:
    """Create a serial number for serial tracking.

    Args:
        serial_no: Serial number
        item_code: Item code
    """
    return inventory.create_serial_no(serial_no, item_code)


@app.tool()
@handle_operation_error
def get_stock_report(
    warehouse: str = None, item_group: str = None, limit: int = 50
) -> Dict[str, Any]:
    """Get stock balance report.

    Args:
        warehouse: Filter by warehouse (optional)
        item_group: Filter by item group (optional)
        limit: Maximum number of records
    """
    return inventory.get_stock_report(warehouse, item_group, limit)


@app.tool()
@handle_operation_error
def get_item_prices(item_code: str, price_list: str = None) -> Dict[str, Any]:
    """Get item prices from price lists.

    Args:
        item_code: Item code
        price_list: Specific price list (optional)
    """
    return inventory.get_item_prices(item_code, price_list)


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


@app.tool()
@handle_operation_error
def create_leave_application(
    employee: str, leave_type: str, from_date: str, to_date: str
) -> Dict[str, Any]:
    """Create a leave application for an employee.

    Args:
        employee: Employee ID
        leave_type: Leave type (e.g., "Annual Leave", "Sick Leave")
        from_date: Leave start date (YYYY-MM-DD format)
        to_date: Leave end date (YYYY-MM-DD format)
    """
    return hr.create_leave_application(employee, leave_type, from_date, to_date)


@app.tool()
@handle_operation_error
def create_salary_structure(name: str, company: str, employee: str) -> Dict[str, Any]:
    """Create a salary structure for an employee.

    Args:
        name: Salary structure name
        company: Company name
        employee: Employee ID
    """
    return hr.create_salary_structure(name, company, employee)


@app.tool()
@handle_operation_error
def create_salary_slip(employee: str, start_date: str, end_date: str) -> Dict[str, Any]:
    """Create a salary slip for an employee.

    Args:
        employee: Employee ID
        start_date: Salary period start date (YYYY-MM-DD format)
        end_date: Salary period end date (YYYY-MM-DD format)
    """
    return hr.create_salary_slip(employee, start_date, end_date)


@app.tool()
@handle_operation_error
def create_job_applicant(applicant_name: str, job_title: str) -> Dict[str, Any]:
    """Create a job applicant record for recruitment.

    Args:
        applicant_name: Applicant's name
        job_title: Job title applied for
    """
    return hr.create_job_applicant(applicant_name, job_title)


@app.tool()
@handle_operation_error
def approve_leave_application(leave_application_name: str) -> Dict[str, Any]:
    """Approve a leave application.

    Args:
        leave_application_name: Leave application name/ID to approve
    """
    return hr.approve_leave_application(leave_application_name)


@app.tool()
@handle_operation_error
def get_leave_applications_list(
    employee: str = None, status: str = None, limit: int = 20
) -> Dict[str, Any]:
    """Get list of leave applications.

    Args:
        employee: Filter by employee (optional)
        status: Filter by status (optional)
        limit: Maximum number of records
    """
    return hr.get_leave_applications_list(employee, status, limit)


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
def create_task(
    subject: str, project: str = None, priority: str = "Medium"
) -> Dict[str, Any]:
    """Create a new task.

    Args:
        subject: Task title/subject
        project: Associated project (optional)
        priority: "Low", "Medium", "High", "Urgent"
    """
    return projects.create_task(subject, project, priority)


@app.tool()
@handle_operation_error
def log_time(
    employee: str, hours: float, activity_type: str, from_time: str, to_time: str
) -> Dict[str, Any]:
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


# Manufacturing Tools
@app.tool()
@handle_operation_error
def create_bom(
    item: str, items: List[Dict[str, Any]], quantity: float = 1.0
) -> Dict[str, Any]:
    """Create a Bill of Materials for manufacturing.

    Args:
        item: Finished item code to manufacture
        items: List of raw material items with item_code, qty, rate
        quantity: Quantity of finished item produced
    """
    return manufacturing.create_bom(item, items, quantity)


@app.tool()
@handle_operation_error
def create_work_order(
    production_item: str, bom_no: str, qty: float, planned_start_date: str = None
) -> Dict[str, Any]:
    """Create a work order for production.

    Args:
        production_item: Item code to manufacture
        bom_no: BOM number to use for production
        qty: Quantity to manufacture
        planned_start_date: Planned start date (YYYY-MM-DD format)
    """
    return manufacturing.create_work_order(
        production_item, bom_no, qty, planned_start_date
    )


@app.tool()
@handle_operation_error
def create_production_plan(
    company: str, for_warehouse: str, items: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Create a production plan for multiple items.

    Args:
        company: Company name
        for_warehouse: Target warehouse for production
        items: List of items to plan production for
    """
    return manufacturing.create_production_plan(company, for_warehouse, items)


@app.tool()
@handle_operation_error
def start_work_order(work_order_name: str) -> Dict[str, Any]:
    """Start a work order for production.

    Args:
        work_order_name: Work order name to start
    """
    return manufacturing.start_work_order(work_order_name)


@app.tool()
@handle_operation_error
def complete_work_order(work_order_name: str) -> Dict[str, Any]:
    """Complete a work order.

    Args:
        work_order_name: Work order name to complete
    """
    return manufacturing.complete_work_order(work_order_name)


@app.tool()
@handle_operation_error
def create_quality_inspection(
    inspection_type: str, reference_type: str, reference_name: str, item_code: str
) -> Dict[str, Any]:
    """Create a quality inspection.

    Args:
        inspection_type: "Incoming", "Outgoing", or "In Process"
        reference_type: Reference document type (e.g., "Purchase Receipt", "Work Order")
        reference_name: Reference document name
        item_code: Item being inspected
    """
    return manufacturing.create_quality_inspection(
        inspection_type, reference_type, reference_name, item_code
    )


@app.tool()
@handle_operation_error
def get_work_orders_list(status: str = None, limit: int = 20) -> Dict[str, Any]:
    """Get list of work orders.

    Args:
        status: Filter by status (optional)
        limit: Maximum number of records
    """
    return manufacturing.get_work_orders_list(status, limit)


@app.tool()
@handle_operation_error
def get_bom_list(item: str = None, limit: int = 20) -> Dict[str, Any]:
    """Get list of BOMs.

    Args:
        item: Filter by item (optional)
        limit: Maximum number of records
    """
    return manufacturing.get_bom_list(item, limit)


# CRM Tools
@app.tool()
@handle_operation_error
def create_lead(lead_name: str, status: str = "Lead") -> Dict[str, Any]:
    """Create a new lead.

    Args:
        lead_name: Lead's name or company name
        status: Lead status (default: "Lead")
    """
    return crm.create_lead(lead_name, status)


@app.tool()
@handle_operation_error
def create_opportunity(
    opportunity_from: str, party_name: str, opportunity_type: str = "Sales"
) -> Dict[str, Any]:
    """Create a new opportunity.

    Args:
        opportunity_from: "Lead" or "Customer"
        party_name: Name of lead or customer
        opportunity_type: "Sales" or "Support"
    """
    return crm.create_opportunity(opportunity_from, party_name, opportunity_type)


@app.tool()
@handle_operation_error
def create_campaign(campaign_name: str) -> Dict[str, Any]:
    """Create a new marketing campaign.

    Args:
        campaign_name: Campaign name
    """
    return crm.create_campaign(campaign_name)


@app.tool()
@handle_operation_error
def convert_lead_to_customer(lead_name: str) -> Dict[str, Any]:
    """Convert a lead to a customer.

    Args:
        lead_name: Lead name to convert
    """
    return crm.convert_lead_to_customer(lead_name)


@app.tool()
@handle_operation_error
def convert_lead_to_opportunity(lead_name: str) -> Dict[str, Any]:
    """Convert a lead to an opportunity.

    Args:
        lead_name: Lead name to convert
    """
    return crm.convert_lead_to_opportunity(lead_name)


@app.tool()
@handle_operation_error
def update_opportunity_status(opportunity_name: str, status: str) -> Dict[str, Any]:
    """Update opportunity status.

    Args:
        opportunity_name: Opportunity name
        status: New status ("Open", "Quotation", "Replied", "Lost", "Converted")
    """
    return crm.update_opportunity_status(opportunity_name, status)


@app.tool()
@handle_operation_error
def search_leads(query: str, limit: int = 10) -> Dict[str, Any]:
    """Search leads by name, email, or phone.

    Args:
        query: Search query
        limit: Maximum number of results
    """
    return crm.search_leads(query, limit)


@app.tool()
@handle_operation_error
def get_leads_list(status: str = None, limit: int = 20) -> Dict[str, Any]:
    """Get list of leads.

    Args:
        status: Filter by status (optional)
        limit: Maximum number of records
    """
    return crm.get_leads_list(status, limit)


@app.tool()
@handle_operation_error
def get_opportunities_list(status: str = None, limit: int = 20) -> Dict[str, Any]:
    """Get list of opportunities.

    Args:
        status: Filter by status (optional)
        limit: Maximum number of records
    """
    return crm.get_opportunities_list(status, limit)


# Asset Management Tools
@app.tool()
@handle_operation_error
def create_asset(
    asset_name: str, asset_category: str, item_code: str
) -> Dict[str, Any]:
    """Create a new asset.

    Args:
        asset_name: Asset name
        asset_category: Asset category
        item_code: Related item code
    """
    return assets.create_asset(asset_name, asset_category, item_code)


@app.tool()
@handle_operation_error
def create_asset_category(
    asset_category_name: str,
    total_number_of_depreciations: int = 10,
    frequency_of_depreciation: int = 12,
) -> Dict[str, Any]:
    """Create a new asset category.

    Args:
        asset_category_name: Asset category name
        total_number_of_depreciations: Total number of depreciations
        frequency_of_depreciation: Frequency in months
    """
    return assets.create_asset_category(
        asset_category_name, total_number_of_depreciations, frequency_of_depreciation
    )


@app.tool()
@handle_operation_error
def create_asset_maintenance(
    asset: str, maintenance_type: str, periodicity: str
) -> Dict[str, Any]:
    """Create asset maintenance schedule.

    Args:
        asset: Asset name
        maintenance_type: Type of maintenance
        periodicity: "Daily", "Weekly", "Monthly", "Quarterly", "Half-yearly", "Yearly"
    """
    return assets.create_asset_maintenance(asset, maintenance_type, periodicity)


@app.tool()
@handle_operation_error
def transfer_asset(
    asset: str, target_location: str, to_employee: str = None
) -> Dict[str, Any]:
    """Transfer asset to new location or employee.

    Args:
        asset: Asset name
        target_location: New location
        to_employee: New employee (optional)
    """
    return assets.transfer_asset(asset, target_location, to_employee)


@app.tool()
@handle_operation_error
def create_asset_depreciation(asset: str) -> Dict[str, Any]:
    """Create depreciation entry for an asset.

    Args:
        asset: Asset name
    """
    return assets.create_asset_depreciation(asset)


@app.tool()
@handle_operation_error
def get_assets_list(
    asset_category: str = None, status: str = None, limit: int = 20
) -> Dict[str, Any]:
    """Get list of assets.

    Args:
        asset_category: Filter by category (optional)
        status: Filter by status (optional)
        limit: Maximum number of records
    """
    return assets.get_assets_list(asset_category, status, limit)


@app.tool()
@handle_operation_error
def search_assets(query: str, limit: int = 10) -> Dict[str, Any]:
    """Search assets by name or category.

    Args:
        query: Search query
        limit: Maximum number of results
    """
    return assets.search_assets(query, limit)


# Support/Service Tools
@app.tool()
@handle_operation_error
def create_issue(
    subject: str, customer: str, issue_type: str = "Bug", priority: str = "Medium"
) -> Dict[str, Any]:
    """Create a support issue.

    Args:
        subject: Issue subject/title
        customer: Customer name
        issue_type: Type of issue ("Bug", "Feature", "Question", etc.)
        priority: Priority level ("Low", "Medium", "High", "Critical")
    """
    return support.create_issue(subject, customer, issue_type, priority)


@app.tool()
@handle_operation_error
def create_service_level_agreement(
    service_level: str, customer: str, start_date: str, end_date: str
) -> Dict[str, Any]:
    """Create a Service Level Agreement.

    Args:
        service_level: Service level name
        customer: Customer name
        start_date: SLA start date (YYYY-MM-DD format)
        end_date: SLA end date (YYYY-MM-DD format)
    """
    return support.create_service_level_agreement(
        service_level, customer, start_date, end_date
    )


@app.tool()
@handle_operation_error
def create_warranty_claim(
    customer: str, item_code: str, serial_no: str = None
) -> Dict[str, Any]:
    """Create a warranty claim.

    Args:
        customer: Customer name
        item_code: Item under warranty
        serial_no: Serial number (optional)
    """
    return support.create_warranty_claim(customer, item_code, serial_no)


@app.tool()
@handle_operation_error
def update_issue_status(issue_name: str, status: str) -> Dict[str, Any]:
    """Update issue status.

    Args:
        issue_name: Issue name/ID
        status: New status ("Open", "Replied", "Closed", "Hold")
    """
    return support.update_issue_status(issue_name, status)


@app.tool()
@handle_operation_error
def assign_issue(issue_name: str, assigned_to: str) -> Dict[str, Any]:
    """Assign an issue to a user.

    Args:
        issue_name: Issue name/ID
        assigned_to: User to assign the issue to
    """
    return support.assign_issue(issue_name, assigned_to)


@app.tool()
@handle_operation_error
def close_issue(issue_name: str, resolution: str = None) -> Dict[str, Any]:
    """Close an issue.

    Args:
        issue_name: Issue name/ID
        resolution: Resolution details (optional)
    """
    return support.close_issue(issue_name, resolution)


@app.tool()
@handle_operation_error
def get_issues_list(
    customer: str = None, status: str = None, priority: str = None, limit: int = 20
) -> Dict[str, Any]:
    """Get list of support issues.

    Args:
        customer: Filter by customer (optional)
        status: Filter by status (optional)
        priority: Filter by priority (optional)
        limit: Maximum number of records
    """
    return support.get_issues_list(customer, status, priority, limit)


@app.tool()
@handle_operation_error
def search_issues(query: str, limit: int = 10) -> Dict[str, Any]:
    """Search issues by subject or customer.

    Args:
        query: Search query
        limit: Maximum number of results
    """
    return support.search_issues(query, limit)


# Utilities/Integration Tools
@app.tool()
@handle_operation_error
def create_workflow(
    workflow_name: str,
    document_type: str,
    states: List[Dict[str, Any]],
    transitions: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """Create a workflow for document approval.

    Args:
        workflow_name: Workflow name
        document_type: DocType this workflow applies to
        states: List of workflow states with state, allow_edit properties
        transitions: List of workflow transitions with state, next_state, allowed properties
    """
    return utilities.create_workflow(workflow_name, document_type, states, transitions)


@app.tool()
@handle_operation_error
def create_custom_field(
    dt: str, fieldname: str, fieldtype: str, label: str
) -> Dict[str, Any]:
    """Create a custom field for a DocType.

    Args:
        dt: DocType to add field to
        fieldname: Field name (must be unique)
        fieldtype: Field type ("Data", "Int", "Float", "Select", "Check", etc.)
        label: Field label for display
    """
    return utilities.create_custom_field(dt, fieldname, fieldtype, label)


@app.tool()
@handle_operation_error
def backup_database() -> Dict[str, Any]:
    """Create a database backup.

    Returns:
        Backup initiation status
    """
    return utilities.backup_database()


@app.tool()
@handle_operation_error
def execute_report(report_name: str, filters: Dict[str, Any] = None) -> Dict[str, Any]:
    """Execute a system report.

    Args:
        report_name: Name of the report to execute
        filters: Report filters (optional)
    """
    return utilities.execute_report(report_name, filters)


@app.tool()
@handle_operation_error
def bulk_update_documents(
    doctype: str, filters: Dict[str, Any], update_fields: Dict[str, Any]
) -> Dict[str, Any]:
    """Bulk update multiple documents.

    Args:
        doctype: DocType to update
        filters: Filters to select documents (e.g., {"status": "Draft"})
        update_fields: Fields to update (e.g., {"status": "Approved"})
    """
    return utilities.bulk_update_documents(doctype, filters, update_fields)


@app.tool()
@handle_operation_error
def get_system_settings() -> Dict[str, Any]:
    """Get system settings and configuration.

    Returns:
        System settings data
    """
    return utilities.get_system_settings()


@app.tool()
@handle_operation_error
def get_document_permissions(doctype: str, name: str) -> Dict[str, Any]:
    """Get document permissions for current user.

    Args:
        doctype: DocType name
        name: Document name
    """
    return utilities.get_document_permissions(doctype, name)


def main():
    """Main entry point for the ERPNext MCP Server."""
    # Initialize the client
    initialize_client()

    # Run the server
    import mcp.server.stdio

    mcp.server.stdio.run_server(app)


if __name__ == "__main__":
    main()
