"""Support/Service domain operations for ERPNext."""

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


class SupportOperations:
    """Support/Service domain operations."""

    def __init__(self, client: ERPNextClient):
        self.client = client

    def create_issue(
        self,
        subject: str,
        customer: str,
        issue_type: str = "Bug",
        priority: str = "Medium",
        **kwargs,
    ) -> Dict[str, Any]:
        """Create a support issue.

        Args:
            subject: Issue subject/title
            customer: Customer name
            issue_type: Type of issue ("Bug", "Feature", "Question", etc.)
            priority: Priority level ("Low", "Medium", "High", "Critical")
            **kwargs: Additional issue fields (description, raised_by, etc.)

        Returns:
            Created issue data
        """
        logger.info(f"Creating support issue: {subject}")

        # Prepare issue data
        issue_data = {
            "subject": subject,
            "customer": customer,
            "issue_type": issue_type,
            "priority": priority,
            **kwargs,
        }

        # Map business parameters to DocType fields
        mapped_data = map_business_params_to_doctype_fields(issue_data, DocTypes.ISSUE)

        # Validate required fields
        missing_fields = validate_required_fields(mapped_data, DocTypes.ISSUE)
        if missing_fields:
            raise ValidationError(
                f"Missing required fields: {', '.join(missing_fields)}"
            )

        try:
            result = self.client.create_doc(DocTypes.ISSUE, mapped_data)
            return format_success_response(result, "Issue created successfully")
        except Exception as e:
            logger.error(f"Failed to create issue: {str(e)}")
            raise

    def create_service_level_agreement(
        self,
        service_level: str,
        customer: str,
        start_date: str,
        end_date: str,
        **kwargs,
    ) -> Dict[str, Any]:
        """Create a Service Level Agreement.

        Args:
            service_level: Service level name
            customer: Customer name
            start_date: SLA start date (YYYY-MM-DD format)
            end_date: SLA end date (YYYY-MM-DD format)
            **kwargs: Additional SLA fields

        Returns:
            Created SLA data
        """
        logger.info(f"Creating SLA for customer: {customer}")

        # Prepare SLA data
        sla_data = {
            "service_level": service_level,
            "customer": customer,
            "start_date": start_date,
            "end_date": end_date,
            **kwargs,
        }

        # Map business parameters to DocType fields
        mapped_data = map_business_params_to_doctype_fields(
            sla_data, DocTypes.SERVICE_LEVEL_AGREEMENT
        )

        # Validate required fields
        missing_fields = validate_required_fields(
            mapped_data, DocTypes.SERVICE_LEVEL_AGREEMENT
        )
        if missing_fields:
            raise ValidationError(
                f"Missing required fields: {', '.join(missing_fields)}"
            )

        try:
            result = self.client.create_doc(
                DocTypes.SERVICE_LEVEL_AGREEMENT, mapped_data
            )
            return format_success_response(
                result, "Service Level Agreement created successfully"
            )
        except Exception as e:
            logger.error(f"Failed to create SLA: {str(e)}")
            raise

    def create_warranty_claim(
        self, customer: str, item_code: str, serial_no: str = None, **kwargs
    ) -> Dict[str, Any]:
        """Create a warranty claim.

        Args:
            customer: Customer name
            item_code: Item under warranty
            serial_no: Serial number (optional)
            **kwargs: Additional warranty claim fields

        Returns:
            Created warranty claim data
        """
        logger.info(f"Creating warranty claim for customer: {customer}")

        # Prepare warranty claim data
        warranty_data = {
            "customer": customer,
            "item_code": item_code,
            "serial_no": serial_no,
            **kwargs,
        }

        # Map business parameters to DocType fields
        mapped_data = map_business_params_to_doctype_fields(
            warranty_data, DocTypes.WARRANTY_CLAIM
        )

        # Validate required fields
        missing_fields = validate_required_fields(mapped_data, DocTypes.WARRANTY_CLAIM)
        if missing_fields:
            raise ValidationError(
                f"Missing required fields: {', '.join(missing_fields)}"
            )

        try:
            result = self.client.create_doc(DocTypes.WARRANTY_CLAIM, mapped_data)
            return format_success_response(
                result, "Warranty Claim created successfully"
            )
        except Exception as e:
            logger.error(f"Failed to create warranty claim: {str(e)}")
            raise

    def update_issue_status(self, issue_name: str, status: str) -> Dict[str, Any]:
        """Update issue status.

        Args:
            issue_name: Issue name/ID
            status: New status ("Open", "Replied", "Closed", "Hold")

        Returns:
            Updated issue data
        """
        logger.info(f"Updating issue {issue_name} status to: {status}")

        try:
            result = self.client.update_doc(
                DocTypes.ISSUE, issue_name, {"status": status}
            )
            return format_success_response(result, "Issue status updated successfully")
        except Exception as e:
            logger.error(f"Failed to update issue status: {str(e)}")
            raise

    def assign_issue(self, issue_name: str, assigned_to: str) -> Dict[str, Any]:
        """Assign an issue to a user.

        Args:
            issue_name: Issue name/ID
            assigned_to: User to assign the issue to

        Returns:
            Updated issue data
        """
        logger.info(f"Assigning issue {issue_name} to: {assigned_to}")

        try:
            # This would typically use ERPNext's assignment feature
            result = self.client.update_doc(
                DocTypes.ISSUE, issue_name, {"_assign": assigned_to}
            )
            return format_success_response(result, "Issue assigned successfully")
        except Exception as e:
            logger.error(f"Failed to assign issue: {str(e)}")
            raise

    def close_issue(self, issue_name: str, resolution: str = None) -> Dict[str, Any]:
        """Close an issue.

        Args:
            issue_name: Issue name/ID
            resolution: Resolution details (optional)

        Returns:
            Closed issue data
        """
        logger.info(f"Closing issue: {issue_name}")

        try:
            update_data = {"status": "Closed"}
            if resolution:
                update_data["resolution"] = resolution

            result = self.client.update_doc(DocTypes.ISSUE, issue_name, update_data)
            return format_success_response(result, "Issue closed successfully")
        except Exception as e:
            logger.error(f"Failed to close issue: {str(e)}")
            raise

    def get_issues_list(
        self,
        customer: Optional[str] = None,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        limit: int = 20,
    ) -> Dict[str, Any]:
        """Get list of support issues.

        Args:
            customer: Filter by customer (optional)
            status: Filter by status (optional)
            priority: Filter by priority (optional)
            limit: Maximum number of records

        Returns:
            List of issues
        """
        logger.info(f"Getting issues list with limit: {limit}")

        try:
            filters = {}
            if customer:
                filters["customer"] = customer
            if status:
                filters["status"] = status
            if priority:
                filters["priority"] = priority

            result = self.client.get_list(
                DocTypes.ISSUE,
                filters=filters,
                limit=limit,
                fields=[
                    "name",
                    "subject",
                    "customer",
                    "status",
                    "priority",
                    "creation",
                ],
            )
            return format_success_response(result, f"Retrieved {len(result)} issues")
        except Exception as e:
            logger.error(f"Failed to get issues list: {str(e)}")
            raise

    def get_warranty_claims_list(
        self,
        customer: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 20,
    ) -> Dict[str, Any]:
        """Get list of warranty claims.

        Args:
            customer: Filter by customer (optional)
            status: Filter by status (optional)
            limit: Maximum number of records

        Returns:
            List of warranty claims
        """
        logger.info(f"Getting warranty claims list with limit: {limit}")

        try:
            filters = {}
            if customer:
                filters["customer"] = customer
            if status:
                filters["status"] = status

            result = self.client.get_list(
                DocTypes.WARRANTY_CLAIM,
                filters=filters,
                limit=limit,
                fields=["name", "customer", "item_code", "status", "complaint_date"],
            )
            return format_success_response(
                result, f"Retrieved {len(result)} warranty claims"
            )
        except Exception as e:
            logger.error(f"Failed to get warranty claims list: {str(e)}")
            raise

    def search_issues(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """Search issues by subject or customer.

        Args:
            query: Search query
            limit: Maximum number of results

        Returns:
            List of matching issues
        """
        logger.info(f"Searching issues with query: {query}")

        try:
            filters = {"subject": ["like", f"%{query}%"]}

            result = self.client.get_list(
                DocTypes.ISSUE,
                filters=filters,
                limit=limit,
                fields=["name", "subject", "customer", "status", "priority"],
            )
            return format_success_response(result, f"Found {len(result)} issues")
        except Exception as e:
            logger.error(f"Failed to search issues: {str(e)}")
            raise
