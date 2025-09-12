"""Basic tests for ERPNext MCP Server."""

import pytest
from erpnext_mcp.utils.doctype_mapping import (
    DocTypes, 
    get_doctype_for_operation,
    map_business_params_to_doctype_fields,
    validate_required_fields
)
from erpnext_mcp.utils.error_handling import (
    ERPNextError,
    ValidationError,
    format_error_response,
    format_success_response
)


class TestDocTypeMapping:
    """Test DocType mapping utilities."""
    
    def test_get_doctype_for_operation(self):
        """Test getting DocType for business operations."""
        assert get_doctype_for_operation("create_sales_invoice") == DocTypes.SALES_INVOICE
        assert get_doctype_for_operation("create_purchase_order") == DocTypes.PURCHASE_ORDER
        assert get_doctype_for_operation("create_customer") == DocTypes.CUSTOMER
        
        with pytest.raises(ValueError):
            get_doctype_for_operation("invalid_operation")
    
    def test_map_business_params(self):
        """Test mapping business parameters to DocType fields."""
        params = {
            "customer_name": "Test Customer",
            "invoice_date": "2025-01-15",
            "grand_total": 1000.0
        }
        
        mapped = map_business_params_to_doctype_fields(params, DocTypes.SALES_INVOICE)
        
        assert mapped["customer_name"] == "Test Customer"
        assert mapped["posting_date"] == "2025-01-15"
        assert mapped["grand_total"] == 1000.0
        assert mapped["doctype"] == DocTypes.SALES_INVOICE
    
    def test_validate_required_fields(self):
        """Test required field validation."""
        # Valid data
        data = {
            "customer_name": "Test Customer",
            "customer_type": "Company"
        }
        missing = validate_required_fields(data, DocTypes.CUSTOMER)
        assert missing == []
        
        # Missing required fields
        data = {"customer_name": "Test Customer"}
        missing = validate_required_fields(data, DocTypes.CUSTOMER)
        assert "customer_type" in missing


class TestErrorHandling:
    """Test error handling utilities."""
    
    def test_erpnext_error(self):
        """Test ERPNext error creation."""
        error = ERPNextError("Test error", "TEST_ERROR", {"detail": "test"})
        assert error.message == "Test error"
        assert error.error_code == "TEST_ERROR"
        assert error.details == {"detail": "test"}
    
    def test_validation_error(self):
        """Test validation error creation."""
        error = ValidationError("Invalid data")
        assert error.error_code == "VALIDATION_ERROR"
        assert "Invalid data" in error.message
    
    def test_format_responses(self):
        """Test response formatting."""
        # Error response
        error = ERPNextError("Test error", "TEST_ERROR")
        error_response = format_error_response(error)
        
        assert error_response["success"] is False
        assert error_response["error_code"] == "TEST_ERROR"
        assert error_response["message"] == "Test error"
        
        # Success response
        data = {"name": "TEST-001"}
        success_response = format_success_response(data, "Success")
        
        assert success_response["success"] is True
        assert success_response["message"] == "Success"
        assert success_response["data"] == data


class TestConfig:
    """Test configuration management."""
    
    def test_config_import(self):
        """Test that config can be imported."""
        from erpnext_mcp.config import config
        assert config.server_name == "ERPNext MCP Server"
        assert config.server_version == "0.1.0"


class TestDomainModuleImports:
    """Test that all domain modules can be imported."""
    
    def test_import_accounting(self):
        """Test importing accounting domain."""
        from erpnext_mcp.domains.accounting import AccountingOperations
        assert AccountingOperations is not None
    
    def test_import_purchasing(self):
        """Test importing purchasing domain."""
        from erpnext_mcp.domains.purchasing import PurchasingOperations
        assert PurchasingOperations is not None
    
    def test_import_sales(self):
        """Test importing sales domain."""
        from erpnext_mcp.domains.sales import SalesOperations
        assert SalesOperations is not None
    
    def test_import_inventory(self):
        """Test importing inventory domain."""
        from erpnext_mcp.domains.inventory import InventoryOperations
        assert InventoryOperations is not None
    
    def test_import_hr(self):
        """Test importing HR domain."""
        from erpnext_mcp.domains.hr import HROperations
        assert HROperations is not None
    
    def test_import_projects(self):
        """Test importing projects domain."""
        from erpnext_mcp.domains.projects import ProjectsOperations
        assert ProjectsOperations is not None


class TestServerImport:
    """Test that server module can be imported."""
    
    def test_import_server(self):
        """Test importing the main server module."""
        from erpnext_mcp import server
        assert server.app is not None
        assert hasattr(server, 'main')