"""Asset Management domain operations for ERPNext."""

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


class AssetManagementOperations:
    """Asset Management domain operations."""

    def __init__(self, client: ERPNextClient):
        self.client = client

    def create_asset(
        self, asset_name: str, asset_category: str, item_code: str, **kwargs
    ) -> Dict[str, Any]:
        """Create a new asset.

        Args:
            asset_name: Asset name
            asset_category: Asset category
            item_code: Related item code
            **kwargs: Additional asset fields (location, purchase_date, gross_purchase_amount, etc.)

        Returns:
            Created asset data
        """
        logger.info(f"Creating asset: {asset_name}")

        # Prepare asset data
        asset_data = {
            "asset_name": asset_name,
            "asset_category": asset_category,
            "item_code": item_code,
            **kwargs,
        }

        # Map business parameters to DocType fields
        mapped_data = map_business_params_to_doctype_fields(asset_data, DocTypes.ASSET)

        # Validate required fields
        missing_fields = validate_required_fields(mapped_data, DocTypes.ASSET)
        if missing_fields:
            raise ValidationError(
                f"Missing required fields: {', '.join(missing_fields)}"
            )

        try:
            result = self.client.create_doc(DocTypes.ASSET, mapped_data)
            return format_success_response(result, "Asset created successfully")
        except Exception as e:
            logger.error(f"Failed to create asset: {str(e)}")
            raise

    def create_asset_category(
        self,
        asset_category_name: str,
        total_number_of_depreciations: int = 10,
        frequency_of_depreciation: int = 12,
        **kwargs,
    ) -> Dict[str, Any]:
        """Create a new asset category.

        Args:
            asset_category_name: Asset category name
            total_number_of_depreciations: Total number of depreciations
            frequency_of_depreciation: Frequency in months
            **kwargs: Additional asset category fields

        Returns:
            Created asset category data
        """
        logger.info(f"Creating asset category: {asset_category_name}")

        # Prepare asset category data
        category_data = {
            "asset_category_name": asset_category_name,
            "total_number_of_depreciations": total_number_of_depreciations,
            "frequency_of_depreciation": frequency_of_depreciation,
            **kwargs,
        }

        # Map business parameters to DocType fields
        mapped_data = map_business_params_to_doctype_fields(
            category_data, DocTypes.ASSET_CATEGORY
        )

        # Validate required fields
        missing_fields = validate_required_fields(mapped_data, DocTypes.ASSET_CATEGORY)
        if missing_fields:
            raise ValidationError(
                f"Missing required fields: {', '.join(missing_fields)}"
            )

        try:
            result = self.client.create_doc(DocTypes.ASSET_CATEGORY, mapped_data)
            return format_success_response(
                result, "Asset Category created successfully"
            )
        except Exception as e:
            logger.error(f"Failed to create asset category: {str(e)}")
            raise

    def create_asset_maintenance(
        self, asset: str, maintenance_type: str, periodicity: str, **kwargs
    ) -> Dict[str, Any]:
        """Create asset maintenance record.

        Args:
            asset: Asset name
            maintenance_type: Type of maintenance
            periodicity: "Daily", "Weekly", "Monthly", "Quarterly", "Half-yearly", "Yearly"
            **kwargs: Additional maintenance fields

        Returns:
            Created asset maintenance data
        """
        logger.info(f"Creating asset maintenance for: {asset}")

        # Prepare maintenance data
        maintenance_data = {
            "asset_name": asset,
            "maintenance_type": maintenance_type,
            "periodicity": periodicity,
            **kwargs,
        }

        # Map business parameters to DocType fields
        mapped_data = map_business_params_to_doctype_fields(
            maintenance_data, DocTypes.ASSET_MAINTENANCE
        )

        # Validate required fields
        missing_fields = validate_required_fields(
            mapped_data, DocTypes.ASSET_MAINTENANCE
        )
        if missing_fields:
            raise ValidationError(
                f"Missing required fields: {', '.join(missing_fields)}"
            )

        try:
            result = self.client.create_doc(DocTypes.ASSET_MAINTENANCE, mapped_data)
            return format_success_response(
                result, "Asset Maintenance created successfully"
            )
        except Exception as e:
            logger.error(f"Failed to create asset maintenance: {str(e)}")
            raise

    def create_asset_movement(
        self, asset: str, purpose: str, **kwargs
    ) -> Dict[str, Any]:
        """Create asset movement record.

        Args:
            asset: Asset name
            purpose: "Issue", "Receipt", "Transfer"
            **kwargs: Additional movement fields (from_employee, to_employee, target_location, etc.)

        Returns:
            Created asset movement data
        """
        logger.info(f"Creating asset movement for: {asset}")

        # Prepare movement data
        movement_data = {"asset": asset, "purpose": purpose, **kwargs}

        # Map business parameters to DocType fields
        mapped_data = map_business_params_to_doctype_fields(
            movement_data, DocTypes.ASSET_MOVEMENT
        )

        # Validate required fields
        missing_fields = validate_required_fields(mapped_data, DocTypes.ASSET_MOVEMENT)
        if missing_fields:
            raise ValidationError(
                f"Missing required fields: {', '.join(missing_fields)}"
            )

        try:
            result = self.client.create_doc(DocTypes.ASSET_MOVEMENT, mapped_data)
            return format_success_response(
                result, "Asset Movement created successfully"
            )
        except Exception as e:
            logger.error(f"Failed to create asset movement: {str(e)}")
            raise

    def create_asset_depreciation(self, asset: str, **kwargs) -> Dict[str, Any]:
        """Create asset depreciation entry.

        Args:
            asset: Asset name
            **kwargs: Additional depreciation fields

        Returns:
            Created depreciation entry data
        """
        logger.info(f"Creating asset depreciation for: {asset}")

        try:
            # Call ERPNext method to create depreciation
            result = self.client.call_method(
                "erpnext.assets.doctype.asset.depreciation.make_depreciation_entry",
                {"asset_name": asset},
            )
            return format_success_response(
                result, "Asset Depreciation created successfully"
            )
        except Exception as e:
            logger.error(f"Failed to create asset depreciation: {str(e)}")
            raise

    def transfer_asset(
        self,
        asset: str,
        target_location: str,
        to_employee: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Transfer asset to new location/employee.

        Args:
            asset: Asset name
            target_location: New location
            to_employee: New employee (optional)
            **kwargs: Additional transfer fields

        Returns:
            Asset movement data
        """
        logger.info(f"Transferring asset {asset} to: {target_location}")

        try:
            movement_data = {
                "asset": asset,
                "purpose": "Transfer",
                "target_location": target_location,
                **kwargs,
            }

            if to_employee:
                movement_data["to_employee"] = to_employee

            result = self.client.create_doc(DocTypes.ASSET_MOVEMENT, movement_data)

            # Submit the movement to make it effective
            self.client.submit_doc(DocTypes.ASSET_MOVEMENT, result["name"])

            return format_success_response(result, "Asset transferred successfully")
        except Exception as e:
            logger.error(f"Failed to transfer asset: {str(e)}")
            raise

    def get_assets_list(
        self,
        asset_category: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 20,
    ) -> Dict[str, Any]:
        """Get list of assets.

        Args:
            asset_category: Filter by category (optional)
            status: Filter by status (optional)
            limit: Maximum number of records

        Returns:
            List of assets
        """
        logger.info(f"Getting assets list with limit: {limit}")

        try:
            filters = {}
            if asset_category:
                filters["asset_category"] = asset_category
            if status:
                filters["status"] = status

            result = self.client.get_list(
                DocTypes.ASSET,
                filters=filters,
                limit=limit,
                fields=[
                    "name",
                    "asset_name",
                    "asset_category",
                    "status",
                    "location",
                    "purchase_date",
                ],
            )
            return format_success_response(result, f"Retrieved {len(result)} assets")
        except Exception as e:
            logger.error(f"Failed to get assets list: {str(e)}")
            raise

    def get_asset_maintenance_list(
        self, asset: Optional[str] = None, limit: int = 20
    ) -> Dict[str, Any]:
        """Get list of asset maintenance records.

        Args:
            asset: Filter by asset (optional)
            limit: Maximum number of records

        Returns:
            List of maintenance records
        """
        logger.info(f"Getting asset maintenance list with limit: {limit}")

        try:
            filters = {}
            if asset:
                filters["asset_name"] = asset

            result = self.client.get_list(
                DocTypes.ASSET_MAINTENANCE,
                filters=filters,
                limit=limit,
                fields=[
                    "name",
                    "asset_name",
                    "maintenance_type",
                    "periodicity",
                    "next_due_date",
                ],
            )
            return format_success_response(
                result, f"Retrieved {len(result)} maintenance records"
            )
        except Exception as e:
            logger.error(f"Failed to get asset maintenance list: {str(e)}")
            raise

    def search_assets(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """Search assets by name or category.

        Args:
            query: Search query
            limit: Maximum number of results

        Returns:
            List of matching assets
        """
        logger.info(f"Searching assets with query: {query}")

        try:
            filters = {"asset_name": ["like", f"%{query}%"]}

            result = self.client.get_list(
                DocTypes.ASSET,
                filters=filters,
                limit=limit,
                fields=["name", "asset_name", "asset_category", "status", "location"],
            )
            return format_success_response(result, f"Found {len(result)} assets")
        except Exception as e:
            logger.error(f"Failed to search assets: {str(e)}")
            raise
