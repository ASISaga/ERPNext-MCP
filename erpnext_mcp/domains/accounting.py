"""Accounting domain operations for ERPNext."""

from typing import Dict, Any, List, Optional
import logging
from ..client.frappe_client import ERPNextClient
from ..utils.doctype_mapping import DocTypes, map_business_params_to_doctype_fields, validate_required_fields
from ..utils.error_handling import ValidationError, format_success_response


logger = logging.getLogger(__name__)


class AccountingOperations:
    """Accounting domain operations."""
    
    def __init__(self, client: ERPNextClient):
        self.client = client
    
    def create_sales_invoice(self, 
                           customer: str,
                           items: List[Dict[str, Any]],
                           posting_date: Optional[str] = None,
                           due_date: Optional[str] = None,
                           **kwargs) -> Dict[str, Any]:
        """Create a sales invoice.
        
        Args:
            customer: Customer name or ID
            items: List of invoice items with item_code, qty, rate
            posting_date: Invoice date (YYYY-MM-DD format)
            due_date: Payment due date (YYYY-MM-DD format)
            **kwargs: Additional invoice fields
            
        Returns:
            Created invoice data
        """
        logger.info(f"Creating sales invoice for customer: {customer}")
        
        # Prepare invoice data
        invoice_data = {
            "customer": customer,
            "items": items,
            "posting_date": posting_date,
            "due_date": due_date,
            **kwargs
        }
        
        # Map business parameters to DocType fields
        mapped_data = map_business_params_to_doctype_fields(invoice_data, DocTypes.SALES_INVOICE)
        
        # Validate required fields
        missing_fields = validate_required_fields(mapped_data, DocTypes.SALES_INVOICE)
        if missing_fields:
            raise ValidationError(f"Missing required fields: {', '.join(missing_fields)}")
        
        # Create the invoice
        result = self.client.create_document(DocTypes.SALES_INVOICE, mapped_data)
        
        return format_success_response(result, "Sales invoice created successfully")
    
    def approve_sales_invoice(self, invoice_name: str) -> Dict[str, Any]:
        """Approve (submit) a sales invoice.
        
        Args:
            invoice_name: Invoice name/ID
            
        Returns:
            Approved invoice data
        """
        logger.info(f"Approving sales invoice: {invoice_name}")
        
        result = self.client.submit_document(DocTypes.SALES_INVOICE, invoice_name)
        
        return format_success_response(result, "Sales invoice approved successfully")
    
    def create_purchase_invoice(self,
                              supplier: str,
                              items: List[Dict[str, Any]],
                              posting_date: Optional[str] = None,
                              due_date: Optional[str] = None,
                              **kwargs) -> Dict[str, Any]:
        """Create a purchase invoice.
        
        Args:
            supplier: Supplier name or ID
            items: List of invoice items with item_code, qty, rate
            posting_date: Invoice date (YYYY-MM-DD format)
            due_date: Payment due date (YYYY-MM-DD format)
            **kwargs: Additional invoice fields
            
        Returns:
            Created invoice data
        """
        logger.info(f"Creating purchase invoice for supplier: {supplier}")
        
        # Prepare invoice data
        invoice_data = {
            "supplier": supplier,
            "items": items,
            "posting_date": posting_date,
            "due_date": due_date,
            **kwargs
        }
        
        # Map business parameters to DocType fields
        mapped_data = map_business_params_to_doctype_fields(invoice_data, DocTypes.PURCHASE_INVOICE)
        
        # Validate required fields
        missing_fields = validate_required_fields(mapped_data, DocTypes.PURCHASE_INVOICE)
        if missing_fields:
            raise ValidationError(f"Missing required fields: {', '.join(missing_fields)}")
        
        # Create the invoice
        result = self.client.create_document(DocTypes.PURCHASE_INVOICE, mapped_data)
        
        return format_success_response(result, "Purchase invoice created successfully")
    
    def create_payment(self,
                      payment_type: str,
                      party_type: str,
                      party: str,
                      paid_amount: float,
                      paid_from_account: Optional[str] = None,
                      paid_to_account: Optional[str] = None,
                      posting_date: Optional[str] = None,
                      **kwargs) -> Dict[str, Any]:
        """Create a payment entry.
        
        Args:
            payment_type: "Receive" or "Pay"
            party_type: "Customer" or "Supplier"
            party: Party name
            paid_amount: Payment amount
            paid_from_account: Source account
            paid_to_account: Destination account
            posting_date: Payment date (YYYY-MM-DD format)
            **kwargs: Additional payment fields
            
        Returns:
            Created payment data
        """
        logger.info(f"Creating {payment_type} payment for {party_type}: {party}")
        
        # Prepare payment data
        payment_data = {
            "payment_type": payment_type,
            "party_type": party_type,
            "party": party,
            "paid_amount": paid_amount,
            "paid_from": paid_from_account,
            "paid_to": paid_to_account,
            "posting_date": posting_date,
            **kwargs
        }
        
        # Map business parameters to DocType fields
        mapped_data = map_business_params_to_doctype_fields(payment_data, DocTypes.PAYMENT_ENTRY)
        
        # Validate required fields
        missing_fields = validate_required_fields(mapped_data, DocTypes.PAYMENT_ENTRY)
        if missing_fields:
            raise ValidationError(f"Missing required fields: {', '.join(missing_fields)}")
        
        # Create the payment
        result = self.client.create_document(DocTypes.PAYMENT_ENTRY, mapped_data)
        
        return format_success_response(result, "Payment entry created successfully")
    
    def get_invoice(self, invoice_type: str, invoice_name: str) -> Dict[str, Any]:
        """Get an invoice by name.
        
        Args:
            invoice_type: "sales" or "purchase"
            invoice_name: Invoice name/ID
            
        Returns:
            Invoice data
        """
        doctype = DocTypes.SALES_INVOICE if invoice_type.lower() == "sales" else DocTypes.PURCHASE_INVOICE
        logger.info(f"Getting {invoice_type} invoice: {invoice_name}")
        
        result = self.client.get_document(doctype, invoice_name)
        
        return format_success_response(result, f"{invoice_type.title()} invoice retrieved successfully")
    
    def get_invoices_list(self,
                         invoice_type: str,
                         filters: Optional[Dict] = None,
                         limit: int = 20) -> Dict[str, Any]:
        """Get list of invoices.
        
        Args:
            invoice_type: "sales" or "purchase"
            filters: Filter conditions
            limit: Maximum number of records
            
        Returns:
            List of invoices
        """
        doctype = DocTypes.SALES_INVOICE if invoice_type.lower() == "sales" else DocTypes.PURCHASE_INVOICE
        logger.info(f"Getting {invoice_type} invoices list")
        
        result = self.client.get_list(doctype, filters=filters, limit=limit)
        
        return format_success_response(result, f"{invoice_type.title()} invoices retrieved successfully")
    
    def get_payments_list(self,
                         filters: Optional[Dict] = None,
                         limit: int = 20) -> Dict[str, Any]:
        """Get list of payments.
        
        Args:
            filters: Filter conditions  
            limit: Maximum number of records
            
        Returns:
            List of payments
        """
        logger.info("Getting payments list")
        
        result = self.client.get_list(DocTypes.PAYMENT_ENTRY, filters=filters, limit=limit)
        
        return format_success_response(result, "Payments retrieved successfully")
    
    def get_account_balance(self, account: str) -> Dict[str, Any]:
        """Get account balance (placeholder - would need custom API).
        
        Args:
            account: Account name
            
        Returns:
            Account balance information
        """
        logger.info(f"Getting balance for account: {account}")
        
        # This would typically call a custom ERPNext API method
        # For now, return a placeholder
        result = {
            "account": account,
            "balance": 0.0,
            "message": "This would require a custom ERPNext API method to get real balance"
        }
        
        return format_success_response(result, f"Account balance retrieved for {account}")