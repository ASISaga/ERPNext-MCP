"""DocType mappings for business operations to ERPNext DocTypes."""

from typing import Dict, List, Any
from enum import Enum


class DocTypes(str, Enum):
    """ERPNext DocType constants."""
    
    # Accounting
    SALES_INVOICE = "Sales Invoice"
    PURCHASE_INVOICE = "Purchase Invoice"
    PAYMENT_ENTRY = "Payment Entry"
    JOURNAL_ENTRY = "Journal Entry"
    ACCOUNT = "Account"
    
    # Sales
    SALES_ORDER = "Sales Order"
    QUOTATION = "Quotation"
    CUSTOMER = "Customer"
    DELIVERY_NOTE = "Delivery Note"
    
    # Purchasing  
    PURCHASE_ORDER = "Purchase Order"
    SUPPLIER_QUOTATION = "Supplier Quotation"
    SUPPLIER = "Supplier"
    PURCHASE_RECEIPT = "Purchase Receipt"
    
    # Inventory
    ITEM = "Item"
    STOCK_ENTRY = "Stock Entry"
    WAREHOUSE = "Warehouse"
    ITEM_GROUP = "Item Group"
    STOCK_LEDGER_ENTRY = "Stock Ledger Entry"
    
    # HR
    EMPLOYEE = "Employee"
    ATTENDANCE = "Attendance"
    LEAVE_APPLICATION = "Leave Application"
    SALARY_SLIP = "Salary Slip"
    
    # Projects
    PROJECT = "Project"
    TASK = "Task"
    TIMESHEET = "Timesheet"


# Mapping of business operations to DocTypes
BUSINESS_OPERATIONS = {
    # Accounting operations
    "create_sales_invoice": DocTypes.SALES_INVOICE,
    "create_purchase_invoice": DocTypes.PURCHASE_INVOICE,
    "create_payment": DocTypes.PAYMENT_ENTRY,
    "create_journal_entry": DocTypes.JOURNAL_ENTRY,
    "approve_invoice": DocTypes.SALES_INVOICE,  # Will use submit operation
    
    # Sales operations
    "create_sales_order": DocTypes.SALES_ORDER,
    "create_quotation": DocTypes.QUOTATION,
    "create_customer": DocTypes.CUSTOMER,
    "create_delivery_note": DocTypes.DELIVERY_NOTE,
    
    # Purchasing operations
    "create_purchase_order": DocTypes.PURCHASE_ORDER,
    "create_supplier_quotation": DocTypes.SUPPLIER_QUOTATION,
    "create_supplier": DocTypes.SUPPLIER,
    "create_purchase_receipt": DocTypes.PURCHASE_RECEIPT,
    
    # Inventory operations
    "create_item": DocTypes.ITEM,
    "create_stock_entry": DocTypes.STOCK_ENTRY,
    "create_warehouse": DocTypes.WAREHOUSE,
    
    # HR operations
    "create_employee": DocTypes.EMPLOYEE,
    "mark_attendance": DocTypes.ATTENDANCE,
    "create_leave_application": DocTypes.LEAVE_APPLICATION,
    
    # Project operations
    "create_project": DocTypes.PROJECT,
    "create_task": DocTypes.TASK,
    "log_time": DocTypes.TIMESHEET,
}


# Field mappings for business-friendly parameter names
FIELD_MAPPINGS = {
    # Common fields
    "id": "name",
    "title": "title",
    "description": "description",
    "date": "posting_date",
    "due_date": "due_date",
    "status": "status",
    
    # Customer/Supplier fields
    "customer_name": "customer_name",
    "customer_email": "email_id",
    "customer_phone": "mobile_no",
    "supplier_name": "supplier_name",
    "supplier_email": "email_id",
    "supplier_phone": "mobile_no",
    
    # Invoice fields
    "invoice_number": "name",
    "invoice_date": "posting_date",
    "grand_total": "grand_total",
    "net_total": "net_total",
    "tax_amount": "total_taxes_and_charges",
    
    # Item fields
    "item_code": "item_code",
    "item_name": "item_name",
    "item_group": "item_group",
    "unit_price": "standard_rate",
    "quantity": "qty",
    "amount": "amount",
    
    # Project fields
    "project_name": "project_name",
    "project_description": "description",
    "start_date": "project_start_date",
    "end_date": "project_end_date",
    
    # Employee fields
    "employee_name": "employee_name",
    "employee_number": "employee",
    "department": "department",
    "designation": "designation",
    "join_date": "date_of_joining",
}


def map_business_params_to_doctype_fields(params: Dict[str, Any], doctype: str) -> Dict[str, Any]:
    """Map business-friendly parameter names to DocType field names.
    
    Args:
        params: Business parameters
        doctype: Target DocType
        
    Returns:
        Mapped DocType fields
    """
    mapped = {}
    
    for business_param, value in params.items():
        # Check if there's a specific mapping for this parameter
        if business_param in FIELD_MAPPINGS:
            mapped[FIELD_MAPPINGS[business_param]] = value
        else:
            # Use the parameter name as-is if no mapping exists
            mapped[business_param] = value
    
    # Add doctype field
    mapped["doctype"] = doctype
    
    return mapped


def get_doctype_for_operation(operation: str) -> str:
    """Get the DocType for a business operation.
    
    Args:
        operation: Business operation name
        
    Returns:
        ERPNext DocType name
        
    Raises:
        ValueError: If operation is not supported
    """
    if operation not in BUSINESS_OPERATIONS:
        raise ValueError(f"Unsupported operation: {operation}")
    
    return BUSINESS_OPERATIONS[operation]


def get_required_fields(doctype: str) -> List[str]:
    """Get commonly required fields for a DocType.
    
    Args:
        doctype: ERPNext DocType name
        
    Returns:
        List of required field names
    """
    required_fields = {
        DocTypes.CUSTOMER: ["customer_name", "customer_type"],
        DocTypes.SUPPLIER: ["supplier_name", "supplier_type"],
        DocTypes.ITEM: ["item_code", "item_name", "item_group"],
        DocTypes.SALES_INVOICE: ["customer", "posting_date", "items"],
        DocTypes.PURCHASE_INVOICE: ["supplier", "posting_date", "items"],
        DocTypes.SALES_ORDER: ["customer", "delivery_date", "items"],
        DocTypes.PURCHASE_ORDER: ["supplier", "schedule_date", "items"],
        DocTypes.PAYMENT_ENTRY: ["payment_type", "party_type", "party", "paid_amount"],
        DocTypes.EMPLOYEE: ["employee_name", "date_of_joining"],
        DocTypes.PROJECT: ["project_name"],
        DocTypes.TASK: ["subject"],
    }
    
    return required_fields.get(doctype, [])


def validate_required_fields(data: Dict[str, Any], doctype: str) -> List[str]:
    """Validate that required fields are present.
    
    Args:
        data: Document data
        doctype: ERPNext DocType name
        
    Returns:
        List of missing required fields
    """
    required = get_required_fields(doctype)
    missing = []
    
    for field in required:
        if field not in data or data[field] is None:
            missing.append(field)
    
    return missing