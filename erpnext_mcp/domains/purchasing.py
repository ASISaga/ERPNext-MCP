"""Purchasing domain operations for ERPNext."""

from typing import Dict, Any, List, Optional
import logging
from ..client.frappe_client import ERPNextClient
from ..utils.doctype_mapping import DocTypes, map_business_params_to_doctype_fields, validate_required_fields
from ..utils.error_handling import ValidationError, format_success_response


logger = logging.getLogger(__name__)


class PurchasingOperations:
    """Purchasing domain operations."""
    
    def __init__(self, client: ERPNextClient):
        self.client = client
    
    def create_purchase_order(self,
                            supplier: str,
                            items: List[Dict[str, Any]],
                            schedule_date: Optional[str] = None,
                            **kwargs) -> Dict[str, Any]:
        """Create a purchase order.
        
        Args:
            supplier: Supplier name or ID
            items: List of items with item_code, qty, rate
            schedule_date: Expected delivery date (YYYY-MM-DD format)
            **kwargs: Additional purchase order fields
            
        Returns:
            Created purchase order data
        """
        logger.info(f"Creating purchase order for supplier: {supplier}")
        
        # Prepare purchase order data
        po_data = {
            "supplier": supplier,
            "items": items,
            "schedule_date": schedule_date,
            **kwargs
        }
        
        # Map business parameters to DocType fields
        mapped_data = map_business_params_to_doctype_fields(po_data, DocTypes.PURCHASE_ORDER)
        
        # Validate required fields
        missing_fields = validate_required_fields(mapped_data, DocTypes.PURCHASE_ORDER)
        if missing_fields:
            raise ValidationError(f"Missing required fields: {', '.join(missing_fields)}")
        
        # Create the purchase order
        result = self.client.create_document(DocTypes.PURCHASE_ORDER, mapped_data)
        
        return format_success_response(result, "Purchase order created successfully")
    
    def approve_purchase_order(self, po_name: str) -> Dict[str, Any]:
        """Approve (submit) a purchase order.
        
        Args:
            po_name: Purchase order name/ID
            
        Returns:
            Approved purchase order data
        """
        logger.info(f"Approving purchase order: {po_name}")
        
        result = self.client.submit_document(DocTypes.PURCHASE_ORDER, po_name)
        
        return format_success_response(result, "Purchase order approved successfully")
    
    def create_supplier(self,
                       supplier_name: str,
                       supplier_type: str = "Company",
                       email: Optional[str] = None,
                       phone: Optional[str] = None,
                       **kwargs) -> Dict[str, Any]:
        """Create a new supplier.
        
        Args:
            supplier_name: Supplier name
            supplier_type: "Company" or "Individual"
            email: Supplier email
            phone: Supplier phone number
            **kwargs: Additional supplier fields
            
        Returns:
            Created supplier data
        """
        logger.info(f"Creating supplier: {supplier_name}")
        
        # Prepare supplier data
        supplier_data = {
            "supplier_name": supplier_name,
            "supplier_type": supplier_type,
            "email_id": email,
            "mobile_no": phone,
            **kwargs
        }
        
        # Map business parameters to DocType fields
        mapped_data = map_business_params_to_doctype_fields(supplier_data, DocTypes.SUPPLIER)
        
        # Validate required fields
        missing_fields = validate_required_fields(mapped_data, DocTypes.SUPPLIER)
        if missing_fields:
            raise ValidationError(f"Missing required fields: {', '.join(missing_fields)}")
        
        # Create the supplier
        result = self.client.create_document(DocTypes.SUPPLIER, mapped_data)
        
        return format_success_response(result, "Supplier created successfully")
    
    def create_supplier_quotation(self,
                                supplier: str,
                                items: List[Dict[str, Any]],
                                valid_till: Optional[str] = None,
                                **kwargs) -> Dict[str, Any]:
        """Create a supplier quotation.
        
        Args:
            supplier: Supplier name or ID
            items: List of items with item_code, qty, rate
            valid_till: Quotation validity date (YYYY-MM-DD format)
            **kwargs: Additional quotation fields
            
        Returns:
            Created supplier quotation data
        """
        logger.info(f"Creating supplier quotation for supplier: {supplier}")
        
        # Prepare quotation data
        quotation_data = {
            "supplier": supplier,
            "items": items,
            "valid_till": valid_till,
            **kwargs
        }
        
        # Map business parameters to DocType fields
        mapped_data = map_business_params_to_doctype_fields(quotation_data, DocTypes.SUPPLIER_QUOTATION)
        
        # Create the supplier quotation
        result = self.client.create_document(DocTypes.SUPPLIER_QUOTATION, mapped_data)
        
        return format_success_response(result, "Supplier quotation created successfully")
    
    def create_purchase_receipt(self,
                              supplier: str,
                              items: List[Dict[str, Any]],
                              posting_date: Optional[str] = None,
                              purchase_order: Optional[str] = None,
                              **kwargs) -> Dict[str, Any]:
        """Create a purchase receipt.
        
        Args:
            supplier: Supplier name or ID
            items: List of received items with item_code, qty, rate
            posting_date: Receipt date (YYYY-MM-DD format)
            purchase_order: Related purchase order name
            **kwargs: Additional receipt fields
            
        Returns:
            Created purchase receipt data
        """
        logger.info(f"Creating purchase receipt for supplier: {supplier}")
        
        # Prepare receipt data
        receipt_data = {
            "supplier": supplier,
            "items": items,
            "posting_date": posting_date,
            "purchase_order": purchase_order,
            **kwargs
        }
        
        # Map business parameters to DocType fields
        mapped_data = map_business_params_to_doctype_fields(receipt_data, DocTypes.PURCHASE_RECEIPT)
        
        # Create the purchase receipt
        result = self.client.create_document(DocTypes.PURCHASE_RECEIPT, mapped_data)
        
        return format_success_response(result, "Purchase receipt created successfully")
    
    def get_purchase_order(self, po_name: str) -> Dict[str, Any]:
        """Get a purchase order by name.
        
        Args:
            po_name: Purchase order name/ID
            
        Returns:
            Purchase order data
        """
        logger.info(f"Getting purchase order: {po_name}")
        
        result = self.client.get_document(DocTypes.PURCHASE_ORDER, po_name)
        
        return format_success_response(result, "Purchase order retrieved successfully")
    
    def get_purchase_orders_list(self,
                                filters: Optional[Dict] = None,
                                limit: int = 20) -> Dict[str, Any]:
        """Get list of purchase orders.
        
        Args:
            filters: Filter conditions
            limit: Maximum number of records
            
        Returns:
            List of purchase orders
        """
        logger.info("Getting purchase orders list")
        
        result = self.client.get_list(DocTypes.PURCHASE_ORDER, filters=filters, limit=limit)
        
        return format_success_response(result, "Purchase orders retrieved successfully")
    
    def get_supplier(self, supplier_name: str) -> Dict[str, Any]:
        """Get a supplier by name.
        
        Args:
            supplier_name: Supplier name/ID
            
        Returns:
            Supplier data
        """
        logger.info(f"Getting supplier: {supplier_name}")
        
        result = self.client.get_document(DocTypes.SUPPLIER, supplier_name)
        
        return format_success_response(result, "Supplier retrieved successfully")
    
    def get_suppliers_list(self,
                          filters: Optional[Dict] = None,
                          limit: int = 20) -> Dict[str, Any]:
        """Get list of suppliers.
        
        Args:
            filters: Filter conditions
            limit: Maximum number of records
            
        Returns:
            List of suppliers
        """
        logger.info("Getting suppliers list")
        
        result = self.client.get_list(DocTypes.SUPPLIER, filters=filters, limit=limit)
        
        return format_success_response(result, "Suppliers retrieved successfully")
    
    def search_suppliers(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """Search suppliers by name or other criteria.
        
        Args:
            query: Search query
            limit: Maximum number of results
            
        Returns:
            List of matching suppliers
        """
        logger.info(f"Searching suppliers with query: {query}")
        
        result = self.client.search_documents(DocTypes.SUPPLIER, query, limit=limit)
        
        return format_success_response(result, f"Found suppliers matching '{query}'")
    
    def get_supplier_quotations_list(self,
                                   filters: Optional[Dict] = None,
                                   limit: int = 20) -> Dict[str, Any]:
        """Get list of supplier quotations.
        
        Args:
            filters: Filter conditions
            limit: Maximum number of records
            
        Returns:
            List of supplier quotations
        """
        logger.info("Getting supplier quotations list")
        
        result = self.client.get_list(DocTypes.SUPPLIER_QUOTATION, filters=filters, limit=limit)
        
        return format_success_response(result, "Supplier quotations retrieved successfully")