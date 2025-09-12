"""Tests for financial reporting functionality."""

import pytest
from unittest.mock import Mock, patch
from erpnext_mcp.domains.accounting import AccountingOperations
from erpnext_mcp.client.frappe_client import ERPNextClient
from erpnext_mcp.utils.error_handling import ERPNextError, ValidationError


class TestFinancialReports:
    """Test financial reporting functionality."""
    
    def setup_method(self):
        """Setup test fixtures."""
        # Mock ERPNext client
        self.mock_client = Mock(spec=ERPNextClient)
        self.accounting = AccountingOperations(self.mock_client)
    
    def test_get_balance_sheet(self):
        """Test Balance Sheet report generation."""
        # Mock successful report execution
        mock_report_data = {
            "result": [
                {"account": "Assets", "balance": 100000},
                {"account": "Liabilities", "balance": 50000},
                {"account": "Equity", "balance": 50000}
            ],
            "columns": ["Account", "Balance"]
        }
        self.mock_client.execute_report.return_value = mock_report_data
        
        result = self.accounting.get_balance_sheet("Test Company", "2025-01-01", "2025-01-31")
        
        # Verify client was called correctly
        self.mock_client.execute_report.assert_called_once_with(
            "Balance Sheet",
            {
                "company": "Test Company",
                "from_date": "2025-01-01",
                "to_date": "2025-01-31",
                "periodicity": "Monthly",
                "filter_based_on": "Date Range"
            }
        )
        
        # Verify response format
        assert result["success"] is True
        assert result["message"] == "Balance Sheet retrieved successfully"
        assert result["data"] == mock_report_data
    
    def test_get_profit_and_loss(self):
        """Test Profit and Loss Statement generation."""
        # Mock successful report execution
        mock_report_data = {
            "result": [
                {"account": "Revenue", "amount": 200000},
                {"account": "Expenses", "amount": 150000},
                {"account": "Net Profit", "amount": 50000}
            ],
            "columns": ["Account", "Amount"]
        }
        self.mock_client.execute_report.return_value = mock_report_data
        
        result = self.accounting.get_profit_and_loss("Test Company", "2025-01-01", "2025-01-31")
        
        # Verify client was called correctly
        self.mock_client.execute_report.assert_called_once_with(
            "Profit and Loss Statement",
            {
                "company": "Test Company",
                "from_date": "2025-01-01",
                "to_date": "2025-01-31",
                "periodicity": "Monthly",
                "filter_based_on": "Date Range"
            }
        )
        
        # Verify response format
        assert result["success"] is True
        assert result["message"] == "Profit and Loss Statement retrieved successfully"
        assert result["data"] == mock_report_data
    
    def test_get_cash_flow(self):
        """Test Cash Flow Statement generation."""
        # Mock successful report execution
        mock_report_data = {
            "result": [
                {"activity": "Operating Activities", "amount": 75000},
                {"activity": "Investing Activities", "amount": -25000},
                {"activity": "Financing Activities", "amount": -10000},
                {"activity": "Net Cash Flow", "amount": 40000}
            ],
            "columns": ["Activity", "Amount"]
        }
        self.mock_client.execute_report.return_value = mock_report_data
        
        result = self.accounting.get_cash_flow("Test Company", "2025-01-01", "2025-01-31")
        
        # Verify client was called correctly
        self.mock_client.execute_report.assert_called_once_with(
            "Cash Flow",
            {
                "company": "Test Company",
                "from_date": "2025-01-01",
                "to_date": "2025-01-31",
                "periodicity": "Monthly",
                "filter_based_on": "Date Range"
            }
        )
        
        # Verify response format
        assert result["success"] is True
        assert result["message"] == "Cash Flow Statement retrieved successfully"
        assert result["data"] == mock_report_data
    
    def test_get_trial_balance(self):
        """Test Trial Balance report generation."""
        # Mock successful report execution
        mock_report_data = {
            "result": [
                {"account": "Cash", "debit": 50000, "credit": 0},
                {"account": "Accounts Receivable", "debit": 30000, "credit": 0},
                {"account": "Accounts Payable", "debit": 0, "credit": 20000}
            ],
            "columns": ["Account", "Debit", "Credit"]
        }
        self.mock_client.execute_report.return_value = mock_report_data
        
        result = self.accounting.get_trial_balance("Test Company", "2025-01-01", "2025-01-31")
        
        # Verify client was called correctly
        self.mock_client.execute_report.assert_called_once_with(
            "Trial Balance",
            {
                "company": "Test Company",
                "from_date": "2025-01-01",
                "to_date": "2025-01-31",
                "periodicity": "Monthly"
            }
        )
        
        # Verify response format
        assert result["success"] is True
        assert result["message"] == "Trial Balance retrieved successfully"
        assert result["data"] == mock_report_data
    
    def test_get_general_ledger(self):
        """Test General Ledger report generation."""
        # Mock successful report execution
        mock_report_data = {
            "result": [
                {"date": "2025-01-15", "account": "Cash", "debit": 1000, "credit": 0, "balance": 1000},
                {"date": "2025-01-20", "account": "Cash", "debit": 0, "credit": 500, "balance": 500}
            ],
            "columns": ["Date", "Account", "Debit", "Credit", "Balance"]
        }
        self.mock_client.execute_report.return_value = mock_report_data
        
        result = self.accounting.get_general_ledger("Test Company", "2025-01-01", "2025-01-31")
        
        # Verify client was called correctly
        self.mock_client.execute_report.assert_called_once_with(
            "General Ledger",
            {
                "company": "Test Company",
                "from_date": "2025-01-01",
                "to_date": "2025-01-31",
                "group_by": "",
                "account": "",
                "party_type": "",
                "party": ""
            }
        )
        
        # Verify response format
        assert result["success"] is True
        assert result["message"] == "General Ledger retrieved successfully"
        assert result["data"] == mock_report_data
    
    def test_get_financial_statements_dispatch(self):
        """Test get_financial_statements method dispatching."""
        # Mock the specific report methods
        self.accounting.get_balance_sheet = Mock(return_value={"success": True, "data": "balance_sheet"})
        self.accounting.get_profit_and_loss = Mock(return_value={"success": True, "data": "profit_loss"})
        self.accounting.get_cash_flow = Mock(return_value={"success": True, "data": "cash_flow"})
        
        # Test Balance Sheet dispatch
        result = self.accounting.get_financial_statements("Test Company", "Balance Sheet", "2025-01-01", "2025-01-31")
        self.accounting.get_balance_sheet.assert_called_once_with("Test Company", "2025-01-01", "2025-01-31")
        assert result["data"] == "balance_sheet"
        
        # Test Profit and Loss dispatch
        result = self.accounting.get_financial_statements("Test Company", "Profit and Loss", "2025-01-01", "2025-01-31")
        self.accounting.get_profit_and_loss.assert_called_once_with("Test Company", "2025-01-01", "2025-01-31")
        assert result["data"] == "profit_loss"
        
        # Test Cash Flow dispatch
        result = self.accounting.get_financial_statements("Test Company", "Cash Flow", "2025-01-01", "2025-01-31")
        self.accounting.get_cash_flow.assert_called_once_with("Test Company", "2025-01-01", "2025-01-31")
        assert result["data"] == "cash_flow"
    
    def test_get_financial_statements_invalid_type(self):
        """Test get_financial_statements with invalid report type."""
        with pytest.raises(ValidationError) as excinfo:
            self.accounting.get_financial_statements("Test Company", "Invalid Report", "2025-01-01", "2025-01-31")
        
        assert "Unsupported report type" in str(excinfo.value)
        assert "Balance Sheet, Profit and Loss, Cash Flow" in str(excinfo.value)
    
    def test_report_error_handling(self):
        """Test error handling in financial reports."""
        # Mock client to raise an exception
        self.mock_client.execute_report.side_effect = ERPNextError("API Error")
        
        with pytest.raises(ERPNextError):
            self.accounting.get_balance_sheet("Test Company", "2025-01-01", "2025-01-31")
    
    def test_report_with_custom_parameters(self):
        """Test reports with custom parameters."""
        # Mock successful report execution
        mock_report_data = {"result": [], "columns": []}
        self.mock_client.execute_report.return_value = mock_report_data
        
        # Test Balance Sheet with custom periodicity
        self.accounting.get_balance_sheet(
            "Test Company", "2025-01-01", "2025-01-31", 
            periodicity="Quarterly", custom_param="test"
        )
        
        # Verify custom parameters are passed
        call_args = self.mock_client.execute_report.call_args
        filters = call_args[0][1]
        assert filters["periodicity"] == "Quarterly"
        assert filters["custom_param"] == "test"
        
        # Test General Ledger with account filter
        self.accounting.get_general_ledger(
            "Test Company", "2025-01-01", "2025-01-31",
            account="Cash", party="Customer ABC"
        )
        
        call_args = self.mock_client.execute_report.call_args
        filters = call_args[0][1]
        assert filters["account"] == "Cash"
        assert filters["party"] == "Customer ABC"


class TestERPNextClientReportExecution:
    """Test ERPNext client report execution functionality."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.client = ERPNextClient()
        # Mock the underlying frappe client
        self.client.client = Mock()
    
    def test_execute_report_success(self):
        """Test successful report execution."""
        # Mock successful API call
        mock_result = {
            "result": [{"account": "Cash", "balance": 1000}],
            "columns": ["Account", "Balance"]
        }
        self.client.client.get_api.return_value = mock_result
        
        result = self.client.execute_report("Balance Sheet", {"company": "Test Company"})
        
        # Verify API was called correctly
        self.client.client.get_api.assert_called_once_with(
            "frappe.desk.query_report.run",
            {
                "report_name": "Balance Sheet",
                "filters": {"company": "Test Company"}
            }
        )
        
        assert result == mock_result
    
    def test_execute_report_fallback(self):
        """Test report execution with fallback method."""
        # Mock primary method failure and fallback success
        self.client.client.get_api.side_effect = [
            Exception("Primary API failed"),  # First call fails
            {"result": [], "columns": []}      # Second call succeeds
        ]
        
        result = self.client.execute_report("Trial Balance", {"company": "Test Company"})
        
        # Verify both API calls were made
        assert self.client.client.get_api.call_count == 2
        
        # First call should be to primary API
        first_call = self.client.client.get_api.call_args_list[0]
        assert first_call[0][0] == "frappe.desk.query_report.run"
        
        # Second call should be to fallback API  
        second_call = self.client.client.get_api.call_args_list[1]
        assert second_call[0][0] == "frappe.desk.reportview.get_data"
    
    def test_execute_report_both_methods_fail(self):
        """Test report execution when both methods fail."""
        # Mock both methods failing
        self.client.client.get_api.side_effect = Exception("Both methods failed")
        
        result = self.client.execute_report("Balance Sheet", {"company": "Test Company"})
        
        # Should return error structure instead of raising exception
        assert result["error"] is True
        assert "Report execution failed" in result["message"]
        assert result["report_name"] == "Balance Sheet"
        assert result["filters"] == {"company": "Test Company"}