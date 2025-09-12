"""Sales domain operations for ERPNext."""

from typing import Dict, Any, List, Optional
import logging
from ..client.frappe_client import ERPNextClient
from ..utils.doctype_mapping import (
    DocTypes,
    map_business_params_to_doctype_fields,
    validate_required_fields,
)
from ..utils.error_handling import ValidationError, format_success_response


logger = logging.getLogger(__name__)


class SalesOperations:
    """Sales domain operations."""

    def __init__(self, client: ERPNextClient):
        self.client = client

    def create_sales_order(
        self,
        customer: str,
        items: List[Dict[str, Any]],
        delivery_date: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Create a sales order.

        Args:
            customer: Customer name or ID
            items: List of items with item_code, qty, rate
            delivery_date: Expected delivery date (YYYY-MM-DD format)
            **kwargs: Additional sales order fields

        Returns:
            Created sales order data
        """
        logger.info(f"Creating sales order for customer: {customer}")

        # Prepare sales order data
        so_data = {
            "customer": customer,
            "items": items,
            "delivery_date": delivery_date,
            **kwargs,
        }

        # Map business parameters to DocType fields
        mapped_data = map_business_params_to_doctype_fields(
            so_data, DocTypes.SALES_ORDER
        )

        # Validate required fields
        missing_fields = validate_required_fields(mapped_data, DocTypes.SALES_ORDER)
        if missing_fields:
            raise ValidationError(
                f"Missing required fields: {', '.join(missing_fields)}"
            )

        # Create the sales order
        result = self.client.create_document(DocTypes.SALES_ORDER, mapped_data)

        return format_success_response(result, "Sales order created successfully")

    def create_customer(
        self,
        customer_name: str,
        customer_type: str = "Company",
        email: Optional[str] = None,
        phone: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Create a new customer.

        Args:
            customer_name: Customer name
            customer_type: "Company" or "Individual"
            email: Customer email
            phone: Customer phone number
            **kwargs: Additional customer fields

        Returns:
            Created customer data
        """
        logger.info(f"Creating customer: {customer_name}")

        # Prepare customer data
        customer_data = {
            "customer_name": customer_name,
            "customer_type": customer_type,
            "email_id": email,
            "mobile_no": phone,
            **kwargs,
        }

        # Map business parameters to DocType fields
        mapped_data = map_business_params_to_doctype_fields(
            customer_data, DocTypes.CUSTOMER
        )

        # Validate required fields
        missing_fields = validate_required_fields(mapped_data, DocTypes.CUSTOMER)
        if missing_fields:
            raise ValidationError(
                f"Missing required fields: {', '.join(missing_fields)}"
            )

        # Create the customer
        result = self.client.create_document(DocTypes.CUSTOMER, mapped_data)

        return format_success_response(result, "Customer created successfully")

    def create_quotation(
        self,
        quotation_to: str,  # "Customer" or "Lead"
        party_name: str,
        items: List[Dict[str, Any]],
        valid_till: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Create a sales quotation.

        Args:
            quotation_to: "Customer" or "Lead"
            party_name: Customer or lead name
            items: List of items with item_code, qty, rate
            valid_till: Quotation validity date (YYYY-MM-DD format)
            **kwargs: Additional quotation fields

        Returns:
            Created quotation data
        """
        logger.info(f"Creating quotation for {quotation_to}: {party_name}")

        # Prepare quotation data
        quotation_data = {
            "quotation_to": quotation_to,
            "party_name": party_name,
            "items": items,
            "valid_till": valid_till,
            **kwargs,
        }

        # Map business parameters to DocType fields
        mapped_data = map_business_params_to_doctype_fields(
            quotation_data, DocTypes.QUOTATION
        )

        # Create the quotation
        result = self.client.create_document(DocTypes.QUOTATION, mapped_data)

        return format_success_response(result, "Quotation created successfully")

    def create_delivery_note(
        self,
        customer: str,
        items: List[Dict[str, Any]],
        posting_date: Optional[str] = None,
        sales_order: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Create a delivery note.

        Args:
            customer: Customer name or ID
            items: List of delivered items with item_code, qty
            posting_date: Delivery date (YYYY-MM-DD format)
            sales_order: Related sales order name
            **kwargs: Additional delivery note fields

        Returns:
            Created delivery note data
        """
        logger.info(f"Creating delivery note for customer: {customer}")

        # Prepare delivery note data
        dn_data = {
            "customer": customer,
            "items": items,
            "posting_date": posting_date,
            "sales_order": sales_order,
            **kwargs,
        }

        # Map business parameters to DocType fields
        mapped_data = map_business_params_to_doctype_fields(
            dn_data, DocTypes.DELIVERY_NOTE
        )

        # Create the delivery note
        result = self.client.create_document(DocTypes.DELIVERY_NOTE, mapped_data)

        return format_success_response(result, "Delivery note created successfully")

    def get_sales_order(self, so_name: str) -> Dict[str, Any]:
        """Get a sales order by name.

        Args:
            so_name: Sales order name/ID

        Returns:
            Sales order data
        """
        logger.info(f"Getting sales order: {so_name}")

        result = self.client.get_document(DocTypes.SALES_ORDER, so_name)

        return format_success_response(result, "Sales order retrieved successfully")

    def get_customer(self, customer_name: str) -> Dict[str, Any]:
        """Get a customer by name.

        Args:
            customer_name: Customer name/ID

        Returns:
            Customer data
        """
        logger.info(f"Getting customer: {customer_name}")

        result = self.client.get_document(DocTypes.CUSTOMER, customer_name)

        return format_success_response(result, "Customer retrieved successfully")

    def get_customers_list(
        self, filters: Optional[Dict] = None, limit: int = 20
    ) -> Dict[str, Any]:
        """Get list of customers.

        Args:
            filters: Filter conditions
            limit: Maximum number of records

        Returns:
            List of customers
        """
        logger.info("Getting customers list")

        result = self.client.get_list(DocTypes.CUSTOMER, filters=filters, limit=limit)

        return format_success_response(result, "Customers retrieved successfully")

    def get_sales_orders_list(
        self, filters: Optional[Dict] = None, limit: int = 20
    ) -> Dict[str, Any]:
        """Get list of sales orders.

        Args:
            filters: Filter conditions
            limit: Maximum number of records

        Returns:
            List of sales orders
        """
        logger.info("Getting sales orders list")

        result = self.client.get_list(
            DocTypes.SALES_ORDER, filters=filters, limit=limit
        )

        return format_success_response(result, "Sales orders retrieved successfully")

    def search_customers(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """Search customers by name or other criteria.

        Args:
            query: Search query
            limit: Maximum number of results

        Returns:
            List of matching customers
        """
        logger.info(f"Searching customers with query: {query}")

        result = self.client.search_documents(DocTypes.CUSTOMER, query, limit=limit)

        return format_success_response(result, f"Found customers matching '{query}'")

    def approve_sales_order(self, so_name: str) -> Dict[str, Any]:
        """Approve (submit) a sales order.

        Args:
            so_name: Sales order name/ID

        Returns:
            Approved sales order data
        """
        logger.info(f"Approving sales order: {so_name}")

        result = self.client.submit_document(DocTypes.SALES_ORDER, so_name)

        return format_success_response(result, "Sales order approved successfully")

    def create_delivery_note(
        self,
        customer: str,
        items: List[Dict[str, Any]],
        posting_date: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Create a delivery note for goods delivery.

        Args:
            customer: Customer name or ID
            items: List of items with item_code, qty, warehouse
            posting_date: Delivery date (YYYY-MM-DD format)
            **kwargs: Additional delivery note fields

        Returns:
            Created delivery note data
        """
        logger.info(f"Creating delivery note for customer: {customer}")

        # Prepare delivery note data
        dn_data = {
            "customer": customer,
            "items": items,
            "posting_date": posting_date,
            **kwargs,
        }

        # Map business parameters to DocType fields
        mapped_data = map_business_params_to_doctype_fields(
            dn_data, DocTypes.DELIVERY_NOTE
        )

        # Validate required fields
        missing_fields = validate_required_fields(mapped_data, DocTypes.DELIVERY_NOTE)
        if missing_fields:
            raise ValidationError(
                f"Missing required fields: {', '.join(missing_fields)}"
            )

        try:
            result = self.client.create_doc(DocTypes.DELIVERY_NOTE, mapped_data)
            return format_success_response(result, "Delivery Note created successfully")
        except Exception as e:
            logger.error(f"Failed to create delivery note: {str(e)}")
            raise

    def create_sales_return(
        self, return_against: str, items: List[Dict[str, Any]], **kwargs
    ) -> Dict[str, Any]:
        """Create a sales return against a delivery note or sales invoice.

        Args:
            return_against: Original delivery note or sales invoice name
            items: List of items being returned with item_code, qty
            **kwargs: Additional sales return fields

        Returns:
            Created sales return data
        """
        logger.info(f"Creating sales return against: {return_against}")

        # Prepare sales return data (as a negative delivery note)
        return_data = {
            "is_return": 1,
            "return_against": return_against,
            "items": items,
            **kwargs,
        }

        # Map business parameters to DocType fields
        mapped_data = map_business_params_to_doctype_fields(
            return_data, DocTypes.DELIVERY_NOTE
        )

        try:
            result = self.client.create_doc(DocTypes.DELIVERY_NOTE, mapped_data)
            return format_success_response(result, "Sales Return created successfully")
        except Exception as e:
            logger.error(f"Failed to create sales return: {str(e)}")
            raise

    def submit_delivery_note(self, dn_name: str) -> Dict[str, Any]:
        """Submit/approve a delivery note.

        Args:
            dn_name: Delivery note name/ID

        Returns:
            Submitted delivery note data
        """
        logger.info(f"Submitting delivery note: {dn_name}")

        try:
            result = self.client.submit_doc(DocTypes.DELIVERY_NOTE, dn_name)
            return format_success_response(
                result, "Delivery Note submitted successfully"
            )
        except Exception as e:
            logger.error(f"Failed to submit delivery note: {str(e)}")
            raise

    def get_delivery_notes_list(
        self,
        customer: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 20,
    ) -> Dict[str, Any]:
        """Get list of delivery notes.

        Args:
            customer: Filter by customer (optional)
            status: Filter by status (optional)
            limit: Maximum number of records

        Returns:
            List of delivery notes
        """
        logger.info(f"Getting delivery notes list with limit: {limit}")

        try:
            filters = {}
            if customer:
                filters["customer"] = customer
            if status:
                filters["status"] = status

            result = self.client.get_list(
                DocTypes.DELIVERY_NOTE,
                filters=filters,
                limit=limit,
                fields=["name", "customer", "posting_date", "grand_total", "status"],
            )
            return format_success_response(
                result, f"Retrieved {len(result)} delivery notes"
            )
        except Exception as e:
            logger.error(f"Failed to get delivery notes list: {str(e)}")
            raise
