"""Utilities and Integration domain operations for ERPNext."""

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


class UtilitiesOperations:
    """Utilities and Integration domain operations."""

    def __init__(self, client: ERPNextClient):
        self.client = client

    def create_workflow(
        self,
        workflow_name: str,
        document_type: str,
        states: List[Dict[str, Any]],
        transitions: List[Dict[str, Any]],
        **kwargs,
    ) -> Dict[str, Any]:
        """Create a workflow for document approval.

        Args:
            workflow_name: Workflow name
            document_type: DocType this workflow applies to
            states: List of workflow states
            transitions: List of workflow transitions
            **kwargs: Additional workflow fields

        Returns:
            Created workflow data
        """
        logger.info(f"Creating workflow: {workflow_name}")

        # Prepare workflow data
        workflow_data = {
            "workflow_name": workflow_name,
            "document_type": document_type,
            "states": states,
            "transitions": transitions,
            **kwargs,
        }

        # Map business parameters to DocType fields
        mapped_data = map_business_params_to_doctype_fields(
            workflow_data, DocTypes.WORKFLOW
        )

        # Validate required fields
        missing_fields = validate_required_fields(mapped_data, DocTypes.WORKFLOW)
        if missing_fields:
            raise ValidationError(
                f"Missing required fields: {', '.join(missing_fields)}"
            )

        try:
            result = self.client.create_doc(DocTypes.WORKFLOW, mapped_data)
            return format_success_response(result, "Workflow created successfully")
        except Exception as e:
            logger.error(f"Failed to create workflow: {str(e)}")
            raise

    def create_print_format(
        self, print_format_name: str, doc_type: str, **kwargs
    ) -> Dict[str, Any]:
        """Create a custom print format.

        Args:
            print_format_name: Print format name
            doc_type: DocType this format applies to
            **kwargs: Additional print format fields

        Returns:
            Created print format data
        """
        logger.info(f"Creating print format: {print_format_name}")

        # Prepare print format data
        print_data = {
            "print_format_name": print_format_name,
            "doc_type": doc_type,
            **kwargs,
        }

        # Map business parameters to DocType fields
        mapped_data = map_business_params_to_doctype_fields(
            print_data, DocTypes.PRINT_FORMAT
        )

        try:
            result = self.client.create_doc(DocTypes.PRINT_FORMAT, mapped_data)
            return format_success_response(result, "Print Format created successfully")
        except Exception as e:
            logger.error(f"Failed to create print format: {str(e)}")
            raise

    def create_custom_field(
        self, dt: str, fieldname: str, fieldtype: str, label: str, **kwargs
    ) -> Dict[str, Any]:
        """Create a custom field for a DocType.

        Args:
            dt: DocType to add field to
            fieldname: Field name
            fieldtype: Field type ("Data", "Int", "Float", "Select", etc.)
            label: Field label
            **kwargs: Additional custom field properties

        Returns:
            Created custom field data
        """
        logger.info(f"Creating custom field {fieldname} for {dt}")

        # Prepare custom field data
        field_data = {
            "dt": dt,
            "fieldname": fieldname,
            "fieldtype": fieldtype,
            "label": label,
            **kwargs,
        }

        # Map business parameters to DocType fields
        mapped_data = map_business_params_to_doctype_fields(
            field_data, DocTypes.CUSTOM_FIELD
        )

        try:
            result = self.client.create_doc(DocTypes.CUSTOM_FIELD, mapped_data)
            return format_success_response(result, "Custom Field created successfully")
        except Exception as e:
            logger.error(f"Failed to create custom field: {str(e)}")
            raise

    def backup_database(self) -> Dict[str, Any]:
        """Create a database backup.

        Returns:
            Backup status
        """
        logger.info("Initiating database backup")

        try:
            # This would call ERPNext backup method
            result = self.client.call_method("frappe.utils.backups.new_backup")
            return format_success_response(
                result, "Database backup initiated successfully"
            )
        except Exception as e:
            logger.error(f"Failed to initiate backup: {str(e)}")
            raise

    def get_system_settings(self) -> Dict[str, Any]:
        """Get system settings.

        Returns:
            System settings data
        """
        logger.info("Getting system settings")

        try:
            result = self.client.get_doc("System Settings", "System Settings")
            return format_success_response(result, "System settings retrieved")
        except Exception as e:
            logger.error(f"Failed to get system settings: {str(e)}")
            raise

    def create_notification(
        self, subject: str, document_type: str, recipients: List[str], **kwargs
    ) -> Dict[str, Any]:
        """Create an email notification rule.

        Args:
            subject: Notification subject
            document_type: DocType to trigger on
            recipients: List of recipients
            **kwargs: Additional notification fields

        Returns:
            Created notification data
        """
        logger.info(f"Creating notification for {document_type}")

        # Prepare notification data
        notification_data = {
            "subject": subject,
            "document_type": document_type,
            "recipients": recipients,
            **kwargs,
        }

        # Map business parameters to DocType fields
        mapped_data = map_business_params_to_doctype_fields(
            notification_data, DocTypes.NOTIFICATION
        )

        try:
            result = self.client.create_doc(DocTypes.NOTIFICATION, mapped_data)
            return format_success_response(result, "Notification created successfully")
        except Exception as e:
            logger.error(f"Failed to create notification: {str(e)}")
            raise

    def execute_report(
        self, report_name: str, filters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Execute a system report.

        Args:
            report_name: Name of the report
            filters: Report filters (optional)

        Returns:
            Report data
        """
        logger.info(f"Executing report: {report_name}")

        try:
            # This would call ERPNext report execution
            result = self.client.call_method(
                "frappe.desk.query_report.run",
                {"report_name": report_name, "filters": filters or {}},
            )
            return format_success_response(
                result, f"Report {report_name} executed successfully"
            )
        except Exception as e:
            logger.error(f"Failed to execute report: {str(e)}")
            raise

    def get_document_permissions(self, doctype: str, name: str) -> Dict[str, Any]:
        """Get document permissions for current user.

        Args:
            doctype: DocType name
            name: Document name

        Returns:
            Permission data
        """
        logger.info(f"Getting permissions for {doctype}: {name}")

        try:
            result = self.client.call_method(
                "frappe.permissions.get_doc_permissions",
                {"doctype": doctype, "name": name},
            )
            return format_success_response(result, "Permissions retrieved successfully")
        except Exception as e:
            logger.error(f"Failed to get permissions: {str(e)}")
            raise

    def bulk_update_documents(
        self, doctype: str, filters: Dict[str, Any], update_fields: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Bulk update multiple documents.

        Args:
            doctype: DocType to update
            filters: Filters to select documents
            update_fields: Fields to update

        Returns:
            Update status
        """
        logger.info(f"Bulk updating {doctype} documents")

        try:
            # Get list of documents matching filters
            docs = self.client.get_list(doctype, filters=filters, fields=["name"])

            updated_count = 0
            for doc in docs:
                try:
                    self.client.update_doc(doctype, doc["name"], update_fields)
                    updated_count += 1
                except Exception as e:
                    logger.warning(f"Failed to update {doc['name']}: {str(e)}")

            result = {
                "total_found": len(docs),
                "updated_count": updated_count,
                "update_fields": update_fields,
            }

            return format_success_response(
                result,
                f"Bulk update completed: {updated_count}/{len(docs)} documents updated",
            )
        except Exception as e:
            logger.error(f"Failed to bulk update documents: {str(e)}")
            raise

    def get_dashboard_data(self, dashboard_name: str) -> Dict[str, Any]:
        """Get dashboard data.

        Args:
            dashboard_name: Dashboard name

        Returns:
            Dashboard data
        """
        logger.info(f"Getting dashboard data: {dashboard_name}")

        try:
            # This would call ERPNext dashboard API
            result = {
                "dashboard_name": dashboard_name,
                "message": "This would require custom ERPNext dashboard API integration",
            }
            return format_success_response(result, "Dashboard data retrieved")
        except Exception as e:
            logger.error(f"Failed to get dashboard data: {str(e)}")
            raise
