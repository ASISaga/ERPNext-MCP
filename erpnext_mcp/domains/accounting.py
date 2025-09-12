"""Accounting domain operations for ERPNext."""

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


class AccountingOperations:
    """Accounting domain operations."""

    def __init__(self, client: ERPNextClient):
        self.client = client

    def create_sales_invoice(
        self,
        customer: str,
        items: List[Dict[str, Any]],
        posting_date: Optional[str] = None,
        due_date: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
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
            **kwargs,
        }

        # Map business parameters to DocType fields
        mapped_data = map_business_params_to_doctype_fields(
            invoice_data, DocTypes.SALES_INVOICE
        )

        # Validate required fields
        missing_fields = validate_required_fields(mapped_data, DocTypes.SALES_INVOICE)
        if missing_fields:
            raise ValidationError(
                f"Missing required fields: {', '.join(missing_fields)}"
            )

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

    def create_purchase_invoice(
        self,
        supplier: str,
        items: List[Dict[str, Any]],
        posting_date: Optional[str] = None,
        due_date: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
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
            **kwargs,
        }

        # Map business parameters to DocType fields
        mapped_data = map_business_params_to_doctype_fields(
            invoice_data, DocTypes.PURCHASE_INVOICE
        )

        # Validate required fields
        missing_fields = validate_required_fields(
            mapped_data, DocTypes.PURCHASE_INVOICE
        )
        if missing_fields:
            raise ValidationError(
                f"Missing required fields: {', '.join(missing_fields)}"
            )

        # Create the invoice
        result = self.client.create_document(DocTypes.PURCHASE_INVOICE, mapped_data)

        return format_success_response(result, "Purchase invoice created successfully")

    def create_payment(
        self,
        payment_type: str,
        party_type: str,
        party: str,
        paid_amount: float,
        paid_from_account: Optional[str] = None,
        paid_to_account: Optional[str] = None,
        posting_date: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
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
            **kwargs,
        }

        # Map business parameters to DocType fields
        mapped_data = map_business_params_to_doctype_fields(
            payment_data, DocTypes.PAYMENT_ENTRY
        )

        # Validate required fields
        missing_fields = validate_required_fields(mapped_data, DocTypes.PAYMENT_ENTRY)
        if missing_fields:
            raise ValidationError(
                f"Missing required fields: {', '.join(missing_fields)}"
            )

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
        doctype = (
            DocTypes.SALES_INVOICE
            if invoice_type.lower() == "sales"
            else DocTypes.PURCHASE_INVOICE
        )
        logger.info(f"Getting {invoice_type} invoice: {invoice_name}")

        result = self.client.get_document(doctype, invoice_name)

        return format_success_response(
            result, f"{invoice_type.title()} invoice retrieved successfully"
        )

    def get_invoices_list(
        self, invoice_type: str, filters: Optional[Dict] = None, limit: int = 20
    ) -> Dict[str, Any]:
        """Get list of invoices.

        Args:
            invoice_type: "sales" or "purchase"
            filters: Filter conditions
            limit: Maximum number of records

        Returns:
            List of invoices
        """
        doctype = (
            DocTypes.SALES_INVOICE
            if invoice_type.lower() == "sales"
            else DocTypes.PURCHASE_INVOICE
        )
        logger.info(f"Getting {invoice_type} invoices list")

        result = self.client.get_list(doctype, filters=filters, limit=limit)

        return format_success_response(
            result, f"{invoice_type.title()} invoices retrieved successfully"
        )

    def get_payments_list(
        self, filters: Optional[Dict] = None, limit: int = 20
    ) -> Dict[str, Any]:
        """Get list of payments.

        Args:
            filters: Filter conditions
            limit: Maximum number of records

        Returns:
            List of payments
        """
        logger.info("Getting payments list")

        result = self.client.get_list(
            DocTypes.PAYMENT_ENTRY, filters=filters, limit=limit
        )

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
            "message": "This would require a custom ERPNext API method to get real balance",
        }

        return format_success_response(
            result, f"Account balance retrieved for {account}"
        )

    def create_cost_center(
        self,
        cost_center_name: str,
        parent_cost_center: str = "All Cost Centers - ",
        **kwargs,
    ) -> Dict[str, Any]:
        """Create a new cost center.

        Args:
            cost_center_name: Cost center name
            parent_cost_center: Parent cost center
            **kwargs: Additional cost center fields

        Returns:
            Created cost center data
        """
        logger.info(f"Creating cost center: {cost_center_name}")

        # Prepare cost center data
        cc_data = {
            "cost_center_name": cost_center_name,
            "parent_cost_center": parent_cost_center,
            **kwargs,
        }

        # Map business parameters to DocType fields
        mapped_data = map_business_params_to_doctype_fields(
            cc_data, DocTypes.COST_CENTER
        )

        try:
            result = self.client.create_doc(DocTypes.COST_CENTER, mapped_data)
            return format_success_response(result, "Cost Center created successfully")
        except Exception as e:
            logger.error(f"Failed to create cost center: {str(e)}")
            raise

    def create_budget(
        self,
        cost_center: str,
        fiscal_year: str,
        accounts: List[Dict[str, Any]],
        **kwargs,
    ) -> Dict[str, Any]:
        """Create a budget for cost center.

        Args:
            cost_center: Cost center name
            fiscal_year: Fiscal year
            accounts: List of accounts with budget amounts
            **kwargs: Additional budget fields

        Returns:
            Created budget data
        """
        logger.info(f"Creating budget for cost center: {cost_center}")

        # Prepare budget data
        budget_data = {
            "cost_center": cost_center,
            "fiscal_year": fiscal_year,
            "accounts": accounts,
            **kwargs,
        }

        # Map business parameters to DocType fields
        mapped_data = map_business_params_to_doctype_fields(
            budget_data, DocTypes.BUDGET
        )

        try:
            result = self.client.create_doc(DocTypes.BUDGET, mapped_data)
            return format_success_response(result, "Budget created successfully")
        except Exception as e:
            logger.error(f"Failed to create budget: {str(e)}")
            raise

    def create_fiscal_year(
        self, year: str, year_start_date: str, year_end_date: str, **kwargs
    ) -> Dict[str, Any]:
        """Create a fiscal year.

        Args:
            year: Fiscal year name
            year_start_date: Start date (YYYY-MM-DD format)
            year_end_date: End date (YYYY-MM-DD format)
            **kwargs: Additional fiscal year fields

        Returns:
            Created fiscal year data
        """
        logger.info(f"Creating fiscal year: {year}")

        # Prepare fiscal year data
        fy_data = {
            "year": year,
            "year_start_date": year_start_date,
            "year_end_date": year_end_date,
            **kwargs,
        }

        # Map business parameters to DocType fields
        mapped_data = map_business_params_to_doctype_fields(
            fy_data, DocTypes.FISCAL_YEAR
        )

        try:
            result = self.client.create_doc(DocTypes.FISCAL_YEAR, mapped_data)
            return format_success_response(result, "Fiscal Year created successfully")
        except Exception as e:
            logger.error(f"Failed to create fiscal year: {str(e)}")
            raise

    def get_financial_statements(
        self, company: str, report_type: str, from_date: str, to_date: str
    ) -> Dict[str, Any]:
        """Get financial statements.

        Args:
            company: Company name
            report_type: "Balance Sheet", "Profit and Loss", "Cash Flow"
            from_date: From date (YYYY-MM-DD format)
            to_date: To date (YYYY-MM-DD format)

        Returns:
            Financial statement data
        """
        logger.info(f"Getting {report_type} for company: {company}")

        try:
            # Call the appropriate specific report method
            if report_type.lower() in ["balance sheet", "balance_sheet"]:
                return self.get_balance_sheet(company, from_date, to_date)
            elif report_type.lower() in ["profit and loss", "profit_and_loss", "income statement", "income_statement"]:
                return self.get_profit_and_loss(company, from_date, to_date)
            elif report_type.lower() in ["cash flow", "cash_flow", "cash flow statement", "cash_flow_statement"]:
                return self.get_cash_flow(company, from_date, to_date)
            else:
                raise ValidationError(
                    f"Unsupported report type: {report_type}. Supported types: Balance Sheet, Profit and Loss, Cash Flow"
                )

        except Exception as e:
            logger.error(f"Failed to get financial statements: {str(e)}")
            raise

    def get_balance_sheet(
        self, company: str, from_date: str, to_date: str, **kwargs
    ) -> Dict[str, Any]:
        """Get Balance Sheet report.

        Args:
            company: Company name
            from_date: From date (YYYY-MM-DD format)
            to_date: To date (YYYY-MM-DD format)
            **kwargs: Additional report parameters

        Returns:
            Balance Sheet data
        """
        logger.info(f"Getting Balance Sheet for company: {company}")

        try:
            # Prepare report filters
            filters = {
                "company": company,
                "from_date": from_date,
                "to_date": to_date,
                "periodicity": kwargs.get("periodicity", "Monthly"),
                "filter_based_on": kwargs.get("filter_based_on", "Date Range"),
                **kwargs
            }

            # Execute Balance Sheet report via ERPNext API
            result = self.client.execute_report("Balance Sheet", filters)

            return format_success_response(
                result, "Balance Sheet retrieved successfully"
            )
        except Exception as e:
            logger.error(f"Failed to get Balance Sheet: {str(e)}")
            raise

    def get_profit_and_loss(
        self, company: str, from_date: str, to_date: str, **kwargs
    ) -> Dict[str, Any]:
        """Get Profit and Loss Statement (Income Statement).

        Args:
            company: Company name
            from_date: From date (YYYY-MM-DD format)
            to_date: To date (YYYY-MM-DD format)
            **kwargs: Additional report parameters

        Returns:
            Profit and Loss Statement data
        """
        logger.info(f"Getting Profit and Loss Statement for company: {company}")

        try:
            # Prepare report filters
            filters = {
                "company": company,
                "from_date": from_date,
                "to_date": to_date,
                "periodicity": kwargs.get("periodicity", "Monthly"),
                "filter_based_on": kwargs.get("filter_based_on", "Date Range"),
                **kwargs
            }

            # Execute Profit and Loss report via ERPNext API
            result = self.client.execute_report("Profit and Loss Statement", filters)

            return format_success_response(
                result, "Profit and Loss Statement retrieved successfully"
            )
        except Exception as e:
            logger.error(f"Failed to get Profit and Loss Statement: {str(e)}")
            raise

    def get_cash_flow(
        self, company: str, from_date: str, to_date: str, **kwargs
    ) -> Dict[str, Any]:
        """Get Cash Flow Statement.

        Args:
            company: Company name
            from_date: From date (YYYY-MM-DD format)
            to_date: To date (YYYY-MM-DD format)
            **kwargs: Additional report parameters

        Returns:
            Cash Flow Statement data
        """
        logger.info(f"Getting Cash Flow Statement for company: {company}")

        try:
            # Prepare report filters
            filters = {
                "company": company,
                "from_date": from_date,
                "to_date": to_date,
                "periodicity": kwargs.get("periodicity", "Monthly"),
                "filter_based_on": kwargs.get("filter_based_on", "Date Range"),
                **kwargs
            }

            # Execute Cash Flow report via ERPNext API
            result = self.client.execute_report("Cash Flow", filters)

            return format_success_response(
                result, "Cash Flow Statement retrieved successfully"
            )
        except Exception as e:
            logger.error(f"Failed to get Cash Flow Statement: {str(e)}")
            raise

    def get_trial_balance(
        self, company: str, from_date: str, to_date: str, **kwargs
    ) -> Dict[str, Any]:
        """Get Trial Balance report.

        Args:
            company: Company name
            from_date: From date (YYYY-MM-DD format)
            to_date: To date (YYYY-MM-DD format)
            **kwargs: Additional report parameters

        Returns:
            Trial Balance data
        """
        logger.info(f"Getting Trial Balance for company: {company}")

        try:
            # Prepare report filters
            filters = {
                "company": company,
                "from_date": from_date,
                "to_date": to_date,
                "periodicity": kwargs.get("periodicity", "Monthly"),
                **kwargs
            }

            # Execute Trial Balance report via ERPNext API
            result = self.client.execute_report("Trial Balance", filters)

            return format_success_response(
                result, "Trial Balance retrieved successfully"
            )
        except Exception as e:
            logger.error(f"Failed to get Trial Balance: {str(e)}")
            raise

    def get_general_ledger(
        self, company: str, from_date: str, to_date: str, **kwargs
    ) -> Dict[str, Any]:
        """Get General Ledger report.

        Args:
            company: Company name
            from_date: From date (YYYY-MM-DD format)
            to_date: To date (YYYY-MM-DD format)
            **kwargs: Additional report parameters like account, party, etc.

        Returns:
            General Ledger data
        """
        logger.info(f"Getting General Ledger for company: {company}")

        try:
            # Prepare report filters
            filters = {
                "company": company,
                "from_date": from_date,
                "to_date": to_date,
                "group_by": kwargs.get("group_by", ""),
                "account": kwargs.get("account", ""),
                "party_type": kwargs.get("party_type", ""),
                "party": kwargs.get("party", ""),
                **kwargs
            }

            # Execute General Ledger report via ERPNext API
            result = self.client.execute_report("General Ledger", filters)

            return format_success_response(
                result, "General Ledger retrieved successfully"
            )
        except Exception as e:
            logger.error(f"Failed to get General Ledger: {str(e)}")
            raise
