"""Manufacturing domain operations for ERPNext."""

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


class ManufacturingOperations:
    """Manufacturing domain operations."""

    def __init__(self, client: ERPNextClient):
        self.client = client

    def create_bom(
        self, item: str, items: List[Dict[str, Any]], quantity: float = 1.0, **kwargs
    ) -> Dict[str, Any]:
        """Create a Bill of Materials.

        Args:
            item: Finished item code
            items: List of raw material items with item_code, qty, rate
            quantity: Quantity to manufacture
            **kwargs: Additional BOM fields

        Returns:
            Created BOM data
        """
        logger.info(f"Creating BOM for item: {item}")

        # Prepare BOM data
        bom_data = {"item": item, "items": items, "quantity": quantity, **kwargs}

        # Map business parameters to DocType fields
        mapped_data = map_business_params_to_doctype_fields(bom_data, DocTypes.BOM)

        # Validate required fields
        missing_fields = validate_required_fields(mapped_data, DocTypes.BOM)
        if missing_fields:
            raise ValidationError(
                f"Missing required fields: {', '.join(missing_fields)}"
            )

        try:
            result = self.client.create_doc(DocTypes.BOM, mapped_data)
            return format_success_response(result, "BOM created successfully")
        except Exception as e:
            logger.error(f"Failed to create BOM: {str(e)}")
            raise

    def create_work_order(
        self,
        production_item: str,
        bom_no: str,
        qty: float,
        planned_start_date: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Create a Work Order for production.

        Args:
            production_item: Item to be manufactured
            bom_no: BOM number to use
            qty: Quantity to manufacture
            planned_start_date: Planned start date (YYYY-MM-DD format)
            **kwargs: Additional work order fields

        Returns:
            Created work order data
        """
        logger.info(f"Creating work order for {qty} units of {production_item}")

        # Prepare work order data
        wo_data = {
            "production_item": production_item,
            "bom_no": bom_no,
            "qty": qty,
            "planned_start_date": planned_start_date,
            **kwargs,
        }

        # Map business parameters to DocType fields
        mapped_data = map_business_params_to_doctype_fields(
            wo_data, DocTypes.WORK_ORDER
        )

        # Validate required fields
        missing_fields = validate_required_fields(mapped_data, DocTypes.WORK_ORDER)
        if missing_fields:
            raise ValidationError(
                f"Missing required fields: {', '.join(missing_fields)}"
            )

        try:
            result = self.client.create_doc(DocTypes.WORK_ORDER, mapped_data)
            return format_success_response(result, "Work Order created successfully")
        except Exception as e:
            logger.error(f"Failed to create work order: {str(e)}")
            raise

    def create_production_plan(
        self, company: str, for_warehouse: str, items: List[Dict[str, Any]], **kwargs
    ) -> Dict[str, Any]:
        """Create a Production Plan.

        Args:
            company: Company name
            for_warehouse: Target warehouse
            items: List of items to plan production for
            **kwargs: Additional production plan fields

        Returns:
            Created production plan data
        """
        logger.info(f"Creating production plan for company: {company}")

        # Prepare production plan data
        pp_data = {
            "company": company,
            "for_warehouse": for_warehouse,
            "items": items,
            **kwargs,
        }

        # Map business parameters to DocType fields
        mapped_data = map_business_params_to_doctype_fields(
            pp_data, DocTypes.PRODUCTION_PLAN
        )

        # Validate required fields
        missing_fields = validate_required_fields(mapped_data, DocTypes.PRODUCTION_PLAN)
        if missing_fields:
            raise ValidationError(
                f"Missing required fields: {', '.join(missing_fields)}"
            )

        try:
            result = self.client.create_doc(DocTypes.PRODUCTION_PLAN, mapped_data)
            return format_success_response(
                result, "Production Plan created successfully"
            )
        except Exception as e:
            logger.error(f"Failed to create production plan: {str(e)}")
            raise

    def create_job_card(
        self, work_order: str, operation: str, workstation: str, **kwargs
    ) -> Dict[str, Any]:
        """Create a Job Card for manufacturing operations.

        Args:
            work_order: Work order reference
            operation: Manufacturing operation
            workstation: Workstation to perform operation
            **kwargs: Additional job card fields

        Returns:
            Created job card data
        """
        logger.info(f"Creating job card for work order: {work_order}")

        # Prepare job card data
        jc_data = {
            "work_order": work_order,
            "operation": operation,
            "workstation": workstation,
            **kwargs,
        }

        # Map business parameters to DocType fields
        mapped_data = map_business_params_to_doctype_fields(jc_data, DocTypes.JOB_CARD)

        # Validate required fields
        missing_fields = validate_required_fields(mapped_data, DocTypes.JOB_CARD)
        if missing_fields:
            raise ValidationError(
                f"Missing required fields: {', '.join(missing_fields)}"
            )

        try:
            result = self.client.create_doc(DocTypes.JOB_CARD, mapped_data)
            return format_success_response(result, "Job Card created successfully")
        except Exception as e:
            logger.error(f"Failed to create job card: {str(e)}")
            raise

    def create_quality_inspection(
        self,
        inspection_type: str,
        reference_type: str,
        reference_name: str,
        item_code: str,
        **kwargs,
    ) -> Dict[str, Any]:
        """Create a Quality Inspection.

        Args:
            inspection_type: "Incoming", "Outgoing", or "In Process"
            reference_type: Reference document type
            reference_name: Reference document name
            item_code: Item being inspected
            **kwargs: Additional quality inspection fields

        Returns:
            Created quality inspection data
        """
        logger.info(f"Creating quality inspection for item: {item_code}")

        # Prepare quality inspection data
        qi_data = {
            "inspection_type": inspection_type,
            "reference_type": reference_type,
            "reference_name": reference_name,
            "item_code": item_code,
            **kwargs,
        }

        # Map business parameters to DocType fields
        mapped_data = map_business_params_to_doctype_fields(
            qi_data, DocTypes.QUALITY_INSPECTION
        )

        # Validate required fields
        missing_fields = validate_required_fields(
            mapped_data, DocTypes.QUALITY_INSPECTION
        )
        if missing_fields:
            raise ValidationError(
                f"Missing required fields: {', '.join(missing_fields)}"
            )

        try:
            result = self.client.create_doc(DocTypes.QUALITY_INSPECTION, mapped_data)
            return format_success_response(
                result, "Quality Inspection created successfully"
            )
        except Exception as e:
            logger.error(f"Failed to create quality inspection: {str(e)}")
            raise

    def start_work_order(self, work_order_name: str) -> Dict[str, Any]:
        """Start a work order production.

        Args:
            work_order_name: Work order name to start

        Returns:
            Updated work order data
        """
        logger.info(f"Starting work order: {work_order_name}")

        try:
            # Submit the work order to start it
            result = self.client.submit_doc(DocTypes.WORK_ORDER, work_order_name)
            return format_success_response(result, "Work Order started successfully")
        except Exception as e:
            logger.error(f"Failed to start work order: {str(e)}")
            raise

    def complete_work_order(self, work_order_name: str) -> Dict[str, Any]:
        """Complete a work order production.

        Args:
            work_order_name: Work order name to complete

        Returns:
            Updated work order data
        """
        logger.info(f"Completing work order: {work_order_name}")

        try:
            # Update status to complete the work order
            result = self.client.update_doc(
                DocTypes.WORK_ORDER, work_order_name, {"status": "Completed"}
            )
            return format_success_response(result, "Work Order completed successfully")
        except Exception as e:
            logger.error(f"Failed to complete work order: {str(e)}")
            raise

    def get_work_orders_list(
        self, status: Optional[str] = None, limit: int = 20
    ) -> Dict[str, Any]:
        """Get list of work orders.

        Args:
            status: Filter by status (optional)
            limit: Maximum number of records

        Returns:
            List of work orders
        """
        logger.info(f"Getting work orders list with limit: {limit}")

        try:
            filters = {}
            if status:
                filters["status"] = status

            result = self.client.get_list(
                DocTypes.WORK_ORDER,
                filters=filters,
                limit=limit,
                fields=[
                    "name",
                    "production_item",
                    "qty",
                    "status",
                    "planned_start_date",
                ],
            )
            return format_success_response(
                result, f"Retrieved {len(result)} work orders"
            )
        except Exception as e:
            logger.error(f"Failed to get work orders list: {str(e)}")
            raise

    def get_bom_list(
        self, item: Optional[str] = None, limit: int = 20
    ) -> Dict[str, Any]:
        """Get list of BOMs.

        Args:
            item: Filter by item (optional)
            limit: Maximum number of records

        Returns:
            List of BOMs
        """
        logger.info(f"Getting BOMs list with limit: {limit}")

        try:
            filters = {}
            if item:
                filters["item"] = item

            result = self.client.get_list(
                DocTypes.BOM,
                filters=filters,
                limit=limit,
                fields=["name", "item", "quantity", "is_active", "is_default"],
            )
            return format_success_response(result, f"Retrieved {len(result)} BOMs")
        except Exception as e:
            logger.error(f"Failed to get BOMs list: {str(e)}")
            raise
