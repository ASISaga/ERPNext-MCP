"""CRM (Customer Relationship Management) domain operations for ERPNext."""

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


class CRMOperations:
    """CRM domain operations."""

    def __init__(self, client: ERPNextClient):
        self.client = client

    def create_lead(
        self, lead_name: str, status: str = "Lead", **kwargs
    ) -> Dict[str, Any]:
        """Create a new lead.

        Args:
            lead_name: Lead's name or company name
            status: Lead status ("Lead", "Open", "Replied", "Opportunity", "Quotation", "Lost Quotation", "Interested", "Converted", "Do Not Contact")
            **kwargs: Additional lead fields (email_id, mobile_no, company_name, etc.)

        Returns:
            Created lead data
        """
        logger.info(f"Creating lead: {lead_name}")

        # Prepare lead data
        lead_data = {"lead_name": lead_name, "status": status, **kwargs}

        # Map business parameters to DocType fields
        mapped_data = map_business_params_to_doctype_fields(lead_data, DocTypes.LEAD)

        # Validate required fields
        missing_fields = validate_required_fields(mapped_data, DocTypes.LEAD)
        if missing_fields:
            raise ValidationError(
                f"Missing required fields: {', '.join(missing_fields)}"
            )

        try:
            result = self.client.create_doc(DocTypes.LEAD, mapped_data)
            return format_success_response(result, "Lead created successfully")
        except Exception as e:
            logger.error(f"Failed to create lead: {str(e)}")
            raise

    def create_opportunity(
        self,
        opportunity_from: str,
        party_name: str,
        opportunity_type: str = "Sales",
        **kwargs,
    ) -> Dict[str, Any]:
        """Create a new opportunity.

        Args:
            opportunity_from: "Lead" or "Customer"
            party_name: Name of lead or customer
            opportunity_type: "Sales" or "Support"
            **kwargs: Additional opportunity fields

        Returns:
            Created opportunity data
        """
        logger.info(f"Creating opportunity from {opportunity_from}: {party_name}")

        # Prepare opportunity data
        opp_data = {
            "opportunity_from": opportunity_from,
            "party_name": party_name,
            "opportunity_type": opportunity_type,
            **kwargs,
        }

        # Map business parameters to DocType fields
        mapped_data = map_business_params_to_doctype_fields(
            opp_data, DocTypes.OPPORTUNITY
        )

        # Validate required fields
        missing_fields = validate_required_fields(mapped_data, DocTypes.OPPORTUNITY)
        if missing_fields:
            raise ValidationError(
                f"Missing required fields: {', '.join(missing_fields)}"
            )

        try:
            result = self.client.create_doc(DocTypes.OPPORTUNITY, mapped_data)
            return format_success_response(result, "Opportunity created successfully")
        except Exception as e:
            logger.error(f"Failed to create opportunity: {str(e)}")
            raise

    def create_campaign(self, campaign_name: str, **kwargs) -> Dict[str, Any]:
        """Create a new campaign.

        Args:
            campaign_name: Campaign name
            **kwargs: Additional campaign fields (description, start_date, end_date, etc.)

        Returns:
            Created campaign data
        """
        logger.info(f"Creating campaign: {campaign_name}")

        # Prepare campaign data
        campaign_data = {"campaign_name": campaign_name, **kwargs}

        # Map business parameters to DocType fields
        mapped_data = map_business_params_to_doctype_fields(
            campaign_data, DocTypes.CAMPAIGN
        )

        # Validate required fields
        missing_fields = validate_required_fields(mapped_data, DocTypes.CAMPAIGN)
        if missing_fields:
            raise ValidationError(
                f"Missing required fields: {', '.join(missing_fields)}"
            )

        try:
            result = self.client.create_doc(DocTypes.CAMPAIGN, mapped_data)
            return format_success_response(result, "Campaign created successfully")
        except Exception as e:
            logger.error(f"Failed to create campaign: {str(e)}")
            raise

    def convert_lead_to_customer(self, lead_name: str) -> Dict[str, Any]:
        """Convert a lead to a customer.

        Args:
            lead_name: Lead name to convert

        Returns:
            Created customer data
        """
        logger.info(f"Converting lead to customer: {lead_name}")

        try:
            # Get lead data first
            lead_data = self.client.get_doc(DocTypes.LEAD, lead_name)

            # Create customer from lead data
            customer_data = {
                "customer_name": lead_data.get("lead_name"),
                "customer_type": (
                    "Company" if lead_data.get("company_name") else "Individual"
                ),
            }

            # Map additional fields if available
            if lead_data.get("email_id"):
                customer_data["email_id"] = lead_data["email_id"]
            if lead_data.get("mobile_no"):
                customer_data["mobile_no"] = lead_data["mobile_no"]

            # Create customer
            customer_result = self.client.create_doc(DocTypes.CUSTOMER, customer_data)

            # Update lead status to converted
            self.client.update_doc(DocTypes.LEAD, lead_name, {"status": "Converted"})

            return format_success_response(
                customer_result, "Lead converted to customer successfully"
            )
        except Exception as e:
            logger.error(f"Failed to convert lead to customer: {str(e)}")
            raise

    def convert_lead_to_opportunity(self, lead_name: str) -> Dict[str, Any]:
        """Convert a lead to an opportunity.

        Args:
            lead_name: Lead name to convert

        Returns:
            Created opportunity data
        """
        logger.info(f"Converting lead to opportunity: {lead_name}")

        try:
            # Create opportunity from lead
            opportunity_data = {
                "opportunity_from": "Lead",
                "party_name": lead_name,
                "opportunity_type": "Sales",
            }

            result = self.client.create_doc(DocTypes.OPPORTUNITY, opportunity_data)

            # Update lead status
            self.client.update_doc(DocTypes.LEAD, lead_name, {"status": "Opportunity"})

            return format_success_response(
                result, "Lead converted to opportunity successfully"
            )
        except Exception as e:
            logger.error(f"Failed to convert lead to opportunity: {str(e)}")
            raise

    def update_opportunity_status(
        self, opportunity_name: str, status: str
    ) -> Dict[str, Any]:
        """Update opportunity status.

        Args:
            opportunity_name: Opportunity name
            status: New status ("Open", "Quotation", "Replied", "Lost", "Converted")

        Returns:
            Updated opportunity data
        """
        logger.info(f"Updating opportunity {opportunity_name} status to: {status}")

        try:
            result = self.client.update_doc(
                DocTypes.OPPORTUNITY, opportunity_name, {"status": status}
            )
            return format_success_response(
                result, "Opportunity status updated successfully"
            )
        except Exception as e:
            logger.error(f"Failed to update opportunity status: {str(e)}")
            raise

    def search_leads(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """Search leads by name, email, or phone.

        Args:
            query: Search query
            limit: Maximum number of results

        Returns:
            List of matching leads
        """
        logger.info(f"Searching leads with query: {query}")

        try:
            filters = {"lead_name": ["like", f"%{query}%"]}

            result = self.client.get_list(
                DocTypes.LEAD,
                filters=filters,
                limit=limit,
                fields=["name", "lead_name", "status", "email_id", "mobile_no"],
            )
            return format_success_response(result, f"Found {len(result)} leads")
        except Exception as e:
            logger.error(f"Failed to search leads: {str(e)}")
            raise

    def get_leads_list(
        self, status: Optional[str] = None, limit: int = 20
    ) -> Dict[str, Any]:
        """Get list of leads.

        Args:
            status: Filter by status (optional)
            limit: Maximum number of records

        Returns:
            List of leads
        """
        logger.info(f"Getting leads list with limit: {limit}")

        try:
            filters = {}
            if status:
                filters["status"] = status

            result = self.client.get_list(
                DocTypes.LEAD,
                filters=filters,
                limit=limit,
                fields=[
                    "name",
                    "lead_name",
                    "status",
                    "email_id",
                    "mobile_no",
                    "creation",
                ],
            )
            return format_success_response(result, f"Retrieved {len(result)} leads")
        except Exception as e:
            logger.error(f"Failed to get leads list: {str(e)}")
            raise

    def get_opportunities_list(
        self, status: Optional[str] = None, limit: int = 20
    ) -> Dict[str, Any]:
        """Get list of opportunities.

        Args:
            status: Filter by status (optional)
            limit: Maximum number of records

        Returns:
            List of opportunities
        """
        logger.info(f"Getting opportunities list with limit: {limit}")

        try:
            filters = {}
            if status:
                filters["status"] = status

            result = self.client.get_list(
                DocTypes.OPPORTUNITY,
                filters=filters,
                limit=limit,
                fields=[
                    "name",
                    "party_name",
                    "opportunity_from",
                    "status",
                    "opportunity_amount",
                ],
            )
            return format_success_response(
                result, f"Retrieved {len(result)} opportunities"
            )
        except Exception as e:
            logger.error(f"Failed to get opportunities list: {str(e)}")
            raise
