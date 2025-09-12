"""Inventory domain operations for ERPNext."""

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


class InventoryOperations:
    """Inventory domain operations."""

    def __init__(self, client: ERPNextClient):
        self.client = client

    def create_item(
        self,
        item_code: str,
        item_name: str,
        item_group: str,
        stock_uom: str = "Nos",
        **kwargs,
    ) -> Dict[str, Any]:
        """Create a new item.

        Args:
            item_code: Unique item code
            item_name: Item name
            item_group: Item group
            stock_uom: Stock unit of measure
            **kwargs: Additional item fields

        Returns:
            Created item data
        """
        logger.info(f"Creating item: {item_code}")

        # Prepare item data
        item_data = {
            "item_code": item_code,
            "item_name": item_name,
            "item_group": item_group,
            "stock_uom": stock_uom,
            **kwargs,
        }

        # Map business parameters to DocType fields
        mapped_data = map_business_params_to_doctype_fields(item_data, DocTypes.ITEM)

        # Validate required fields
        missing_fields = validate_required_fields(mapped_data, DocTypes.ITEM)
        if missing_fields:
            raise ValidationError(
                f"Missing required fields: {', '.join(missing_fields)}"
            )

        # Create the item
        result = self.client.create_document(DocTypes.ITEM, mapped_data)

        return format_success_response(result, "Item created successfully")

    def create_warehouse(
        self, warehouse_name: str, warehouse_type: str = "Stock", **kwargs
    ) -> Dict[str, Any]:
        """Create a new warehouse.

        Args:
            warehouse_name: Warehouse name
            warehouse_type: Warehouse type (Stock, Transit, etc.)
            **kwargs: Additional warehouse fields

        Returns:
            Created warehouse data
        """
        logger.info(f"Creating warehouse: {warehouse_name}")

        # Prepare warehouse data
        warehouse_data = {
            "warehouse_name": warehouse_name,
            "warehouse_type": warehouse_type,
            **kwargs,
        }

        # Map business parameters to DocType fields
        mapped_data = map_business_params_to_doctype_fields(
            warehouse_data, DocTypes.WAREHOUSE
        )

        # Create the warehouse
        result = self.client.create_document(DocTypes.WAREHOUSE, mapped_data)

        return format_success_response(result, "Warehouse created successfully")

    def create_stock_entry(
        self,
        stock_entry_type: str,
        items: List[Dict[str, Any]],
        posting_date: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Create a stock entry.

        Args:
            stock_entry_type: Type like "Material Issue", "Material Receipt", "Material Transfer"
            items: List of items with item_code, qty, warehouse info
            posting_date: Entry date (YYYY-MM-DD format)
            **kwargs: Additional stock entry fields

        Returns:
            Created stock entry data
        """
        logger.info(f"Creating stock entry: {stock_entry_type}")

        # Prepare stock entry data
        entry_data = {
            "stock_entry_type": stock_entry_type,
            "items": items,
            "posting_date": posting_date,
            **kwargs,
        }

        # Map business parameters to DocType fields
        mapped_data = map_business_params_to_doctype_fields(
            entry_data, DocTypes.STOCK_ENTRY
        )

        # Create the stock entry
        result = self.client.create_document(DocTypes.STOCK_ENTRY, mapped_data)

        return format_success_response(result, "Stock entry created successfully")

    def get_item(self, item_code: str) -> Dict[str, Any]:
        """Get an item by code.

        Args:
            item_code: Item code

        Returns:
            Item data
        """
        logger.info(f"Getting item: {item_code}")

        result = self.client.get_document(DocTypes.ITEM, item_code)

        return format_success_response(result, "Item retrieved successfully")

    def get_items_list(
        self, filters: Optional[Dict] = None, limit: int = 20
    ) -> Dict[str, Any]:
        """Get list of items.

        Args:
            filters: Filter conditions
            limit: Maximum number of records

        Returns:
            List of items
        """
        logger.info("Getting items list")

        result = self.client.get_list(DocTypes.ITEM, filters=filters, limit=limit)

        return format_success_response(result, "Items retrieved successfully")

    def search_items(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """Search items by code or name.

        Args:
            query: Search query
            limit: Maximum number of results

        Returns:
            List of matching items
        """
        logger.info(f"Searching items with query: {query}")

        result = self.client.search_documents(DocTypes.ITEM, query, limit=limit)

        return format_success_response(result, f"Found items matching '{query}'")

    def get_stock_balance(
        self, item_code: str, warehouse: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get stock balance for an item (placeholder - would need custom API).

        Args:
            item_code: Item code
            warehouse: Specific warehouse (optional)

        Returns:
            Stock balance information
        """
        logger.info(f"Getting stock balance for item: {item_code}")

        # This would typically call a custom ERPNext API method
        # For now, return a placeholder
        result = {
            "item_code": item_code,
            "warehouse": warehouse or "All Warehouses",
            "balance_qty": 0.0,
            "message": "This would require a custom ERPNext API method to get real stock balance",
        }

        return format_success_response(
            result, f"Stock balance retrieved for {item_code}"
        )

    def get_warehouses_list(
        self, filters: Optional[Dict] = None, limit: int = 20
    ) -> Dict[str, Any]:
        """Get list of warehouses.

        Args:
            filters: Filter conditions
            limit: Maximum number of records

        Returns:
            List of warehouses
        """
        logger.info("Getting warehouses list")

        result = self.client.get_list(DocTypes.WAREHOUSE, filters=filters, limit=limit)

        return format_success_response(result, "Warehouses retrieved successfully")

    def get_stock_entries_list(
        self, filters: Optional[Dict] = None, limit: int = 20
    ) -> Dict[str, Any]:
        """Get list of stock entries.

        Args:
            filters: Filter conditions
            limit: Maximum number of records

        Returns:
            List of stock entries
        """
        logger.info("Getting stock entries list")

        result = self.client.get_list(
            DocTypes.STOCK_ENTRY, filters=filters, limit=limit
        )

        return format_success_response(result, "Stock entries retrieved successfully")

    def submit_stock_entry(self, entry_name: str) -> Dict[str, Any]:
        """Submit a stock entry.

        Args:
            entry_name: Stock entry name/ID

        Returns:
            Submitted stock entry data
        """
        logger.info(f"Submitting stock entry: {entry_name}")

        result = self.client.submit_document(DocTypes.STOCK_ENTRY, entry_name)

        return format_success_response(result, "Stock entry submitted successfully")

    def create_item_price(
        self, item_code: str, price_list: str, price_list_rate: float, **kwargs
    ) -> Dict[str, Any]:
        """Create an item price for a price list.

        Args:
            item_code: Item code
            price_list: Price list name
            price_list_rate: Rate/price
            **kwargs: Additional item price fields

        Returns:
            Created item price data
        """
        logger.info(f"Creating item price for {item_code} in price list: {price_list}")

        # Prepare item price data
        price_data = {
            "item_code": item_code,
            "price_list": price_list,
            "price_list_rate": price_list_rate,
            **kwargs,
        }

        # Map business parameters to DocType fields
        mapped_data = map_business_params_to_doctype_fields(
            price_data, DocTypes.ITEM_PRICE
        )

        # Validate required fields
        missing_fields = validate_required_fields(mapped_data, DocTypes.ITEM_PRICE)
        if missing_fields:
            raise ValidationError(
                f"Missing required fields: {', '.join(missing_fields)}"
            )

        try:
            result = self.client.create_doc(DocTypes.ITEM_PRICE, mapped_data)
            return format_success_response(result, "Item Price created successfully")
        except Exception as e:
            logger.error(f"Failed to create item price: {str(e)}")
            raise

    def create_price_list(
        self, price_list_name: str, currency: str, **kwargs
    ) -> Dict[str, Any]:
        """Create a price list.

        Args:
            price_list_name: Price list name
            currency: Currency code
            **kwargs: Additional price list fields

        Returns:
            Created price list data
        """
        logger.info(f"Creating price list: {price_list_name}")

        # Prepare price list data
        price_list_data = {
            "price_list_name": price_list_name,
            "currency": currency,
            **kwargs,
        }

        # Map business parameters to DocType fields
        mapped_data = map_business_params_to_doctype_fields(
            price_list_data, DocTypes.PRICE_LIST
        )

        # Validate required fields
        missing_fields = validate_required_fields(mapped_data, DocTypes.PRICE_LIST)
        if missing_fields:
            raise ValidationError(
                f"Missing required fields: {', '.join(missing_fields)}"
            )

        try:
            result = self.client.create_doc(DocTypes.PRICE_LIST, mapped_data)
            return format_success_response(result, "Price List created successfully")
        except Exception as e:
            logger.error(f"Failed to create price list: {str(e)}")
            raise

    def create_batch(self, batch_id: str, item: str, **kwargs) -> Dict[str, Any]:
        """Create a batch for batch tracking.

        Args:
            batch_id: Batch ID
            item: Item code
            **kwargs: Additional batch fields (manufacturing_date, expiry_date, etc.)

        Returns:
            Created batch data
        """
        logger.info(f"Creating batch {batch_id} for item: {item}")

        # Prepare batch data
        batch_data = {"batch_id": batch_id, "item": item, **kwargs}

        # Map business parameters to DocType fields
        mapped_data = map_business_params_to_doctype_fields(batch_data, DocTypes.BATCH)

        # Validate required fields
        missing_fields = validate_required_fields(mapped_data, DocTypes.BATCH)
        if missing_fields:
            raise ValidationError(
                f"Missing required fields: {', '.join(missing_fields)}"
            )

        try:
            result = self.client.create_doc(DocTypes.BATCH, mapped_data)
            return format_success_response(result, "Batch created successfully")
        except Exception as e:
            logger.error(f"Failed to create batch: {str(e)}")
            raise

    def create_serial_no(
        self, serial_no: str, item_code: str, **kwargs
    ) -> Dict[str, Any]:
        """Create a serial number for serial tracking.

        Args:
            serial_no: Serial number
            item_code: Item code
            **kwargs: Additional serial number fields

        Returns:
            Created serial number data
        """
        logger.info(f"Creating serial number {serial_no} for item: {item_code}")

        # Prepare serial number data
        serial_data = {"serial_no": serial_no, "item_code": item_code, **kwargs}

        # Map business parameters to DocType fields
        mapped_data = map_business_params_to_doctype_fields(
            serial_data, DocTypes.SERIAL_NO
        )

        # Validate required fields
        missing_fields = validate_required_fields(mapped_data, DocTypes.SERIAL_NO)
        if missing_fields:
            raise ValidationError(
                f"Missing required fields: {', '.join(missing_fields)}"
            )

        try:
            result = self.client.create_doc(DocTypes.SERIAL_NO, mapped_data)
            return format_success_response(result, "Serial Number created successfully")
        except Exception as e:
            logger.error(f"Failed to create serial number: {str(e)}")
            raise

    def get_stock_report(
        self,
        warehouse: Optional[str] = None,
        item_group: Optional[str] = None,
        limit: int = 50,
    ) -> Dict[str, Any]:
        """Get stock balance report.

        Args:
            warehouse: Filter by warehouse (optional)
            item_group: Filter by item group (optional)
            limit: Maximum number of records

        Returns:
            Stock report data
        """
        logger.info(f"Getting stock report with limit: {limit}")

        try:
            # This would require calling ERPNext report APIs
            # For now, return stock ledger entries as a placeholder
            filters = {}
            if warehouse:
                filters["warehouse"] = warehouse

            result = self.client.get_list(
                DocTypes.STOCK_LEDGER_ENTRY,
                filters=filters,
                limit=limit,
                fields=[
                    "item_code",
                    "warehouse",
                    "actual_qty",
                    "valuation_rate",
                    "posting_date",
                ],
            )
            return format_success_response(
                result, f"Retrieved {len(result)} stock records"
            )
        except Exception as e:
            logger.error(f"Failed to get stock report: {str(e)}")
            raise

    def get_item_prices(
        self, item_code: str, price_list: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get item prices from price lists.

        Args:
            item_code: Item code
            price_list: Specific price list (optional)

        Returns:
            Item price data
        """
        logger.info(f"Getting prices for item: {item_code}")

        try:
            filters = {"item_code": item_code}
            if price_list:
                filters["price_list"] = price_list

            result = self.client.get_list(
                DocTypes.ITEM_PRICE,
                filters=filters,
                fields=["price_list", "price_list_rate", "valid_from", "valid_upto"],
            )
            return format_success_response(
                result, f"Retrieved {len(result)} price records"
            )
        except Exception as e:
            logger.error(f"Failed to get item prices: {str(e)}")
            raise
