"""HR domain operations for ERPNext."""

from typing import Dict, Any, List, Optional
import logging
from ..client.frappe_client import ERPNextClient
from ..utils.doctype_mapping import DocTypes, map_business_params_to_doctype_fields, validate_required_fields
from ..utils.error_handling import ValidationError, format_success_response


logger = logging.getLogger(__name__)


class HROperations:
    """HR domain operations."""
    
    def __init__(self, client: ERPNextClient):
        self.client = client
    
    def create_employee(self,
                       employee_name: str,
                       date_of_joining: str,
                       department: Optional[str] = None,
                       designation: Optional[str] = None,
                       **kwargs) -> Dict[str, Any]:
        """Create a new employee.
        
        Args:
            employee_name: Employee full name
            date_of_joining: Join date (YYYY-MM-DD format)
            department: Department name
            designation: Job title/designation
            **kwargs: Additional employee fields
            
        Returns:
            Created employee data
        """
        logger.info(f"Creating employee: {employee_name}")
        
        # Prepare employee data
        employee_data = {
            "employee_name": employee_name,
            "date_of_joining": date_of_joining,
            "department": department,
            "designation": designation,
            **kwargs
        }
        
        # Map business parameters to DocType fields
        mapped_data = map_business_params_to_doctype_fields(employee_data, DocTypes.EMPLOYEE)
        
        # Validate required fields
        missing_fields = validate_required_fields(mapped_data, DocTypes.EMPLOYEE)
        if missing_fields:
            raise ValidationError(f"Missing required fields: {', '.join(missing_fields)}")
        
        # Create the employee
        result = self.client.create_document(DocTypes.EMPLOYEE, mapped_data)
        
        return format_success_response(result, "Employee created successfully")
    
    def mark_attendance(self,
                       employee: str,
                       attendance_date: str,
                       status: str,
                       **kwargs) -> Dict[str, Any]:
        """Mark attendance for an employee.
        
        Args:
            employee: Employee ID
            attendance_date: Attendance date (YYYY-MM-DD format)
            status: "Present", "Absent", "Half Day"
            **kwargs: Additional attendance fields
            
        Returns:
            Created attendance record
        """
        logger.info(f"Marking attendance for employee: {employee}")
        
        # Prepare attendance data
        attendance_data = {
            "employee": employee,
            "attendance_date": attendance_date,
            "status": status,
            **kwargs
        }
        
        # Map business parameters to DocType fields
        mapped_data = map_business_params_to_doctype_fields(attendance_data, DocTypes.ATTENDANCE)
        
        # Create the attendance record
        result = self.client.create_document(DocTypes.ATTENDANCE, mapped_data)
        
        return format_success_response(result, "Attendance marked successfully")
    
    def create_leave_application(self,
                               employee: str,
                               leave_type: str,
                               from_date: str,
                               to_date: str,
                               description: Optional[str] = None,
                               **kwargs) -> Dict[str, Any]:
        """Create a leave application.
        
        Args:
            employee: Employee ID
            leave_type: Type of leave
            from_date: Leave start date (YYYY-MM-DD format)
            to_date: Leave end date (YYYY-MM-DD format)
            description: Leave reason/description
            **kwargs: Additional leave application fields
            
        Returns:
            Created leave application data
        """
        logger.info(f"Creating leave application for employee: {employee}")
        
        # Prepare leave application data
        leave_data = {
            "employee": employee,
            "leave_type": leave_type,
            "from_date": from_date,
            "to_date": to_date,
            "description": description,
            **kwargs
        }
        
        # Map business parameters to DocType fields
        mapped_data = map_business_params_to_doctype_fields(leave_data, DocTypes.LEAVE_APPLICATION)
        
        # Create the leave application
        result = self.client.create_document(DocTypes.LEAVE_APPLICATION, mapped_data)
        
        return format_success_response(result, "Leave application created successfully")
    
    def get_employee(self, employee_id: str) -> Dict[str, Any]:
        """Get an employee by ID.
        
        Args:
            employee_id: Employee ID
            
        Returns:
            Employee data
        """
        logger.info(f"Getting employee: {employee_id}")
        
        result = self.client.get_document(DocTypes.EMPLOYEE, employee_id)
        
        return format_success_response(result, "Employee retrieved successfully")
    
    def get_employees_list(self,
                          filters: Optional[Dict] = None,
                          limit: int = 20) -> Dict[str, Any]:
        """Get list of employees.
        
        Args:
            filters: Filter conditions
            limit: Maximum number of records
            
        Returns:
            List of employees
        """
        logger.info("Getting employees list")
        
        result = self.client.get_list(DocTypes.EMPLOYEE, filters=filters, limit=limit)
        
        return format_success_response(result, "Employees retrieved successfully")
    
    def search_employees(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """Search employees by name or other criteria.
        
        Args:
            query: Search query
            limit: Maximum number of results
            
        Returns:
            List of matching employees
        """
        logger.info(f"Searching employees with query: {query}")
        
        result = self.client.search_documents(DocTypes.EMPLOYEE, query, limit=limit)
        
        return format_success_response(result, f"Found employees matching '{query}'")
    
    def get_attendance_list(self,
                           filters: Optional[Dict] = None,
                           limit: int = 20) -> Dict[str, Any]:
        """Get list of attendance records.
        
        Args:
            filters: Filter conditions
            limit: Maximum number of records
            
        Returns:
            List of attendance records
        """
        logger.info("Getting attendance list")
        
        result = self.client.get_list(DocTypes.ATTENDANCE, filters=filters, limit=limit)
        
        return format_success_response(result, "Attendance records retrieved successfully")
    
    def get_leave_applications_list(self,
                                   filters: Optional[Dict] = None,
                                   limit: int = 20) -> Dict[str, Any]:
        """Get list of leave applications.
        
        Args:
            filters: Filter conditions
            limit: Maximum number of records
            
        Returns:
            List of leave applications
        """
        logger.info("Getting leave applications list")
        
        result = self.client.get_list(DocTypes.LEAVE_APPLICATION, filters=filters, limit=limit)
        
        return format_success_response(result, "Leave applications retrieved successfully")
    
    def approve_leave_application(self, leave_app_name: str) -> Dict[str, Any]:
        """Approve a leave application.
        
        Args:
            leave_app_name: Leave application name/ID
            
        Returns:
            Approved leave application data
        """
        logger.info(f"Approving leave application: {leave_app_name}")
        
        result = self.client.submit_document(DocTypes.LEAVE_APPLICATION, leave_app_name)
        
        return format_success_response(result, "Leave application approved successfully")
    
    def get_employee_attendance_summary(self,
                                      employee: str,
                                      from_date: str,
                                      to_date: str) -> Dict[str, Any]:
        """Get attendance summary for an employee (placeholder - would need custom API).
        
        Args:
            employee: Employee ID
            from_date: Start date (YYYY-MM-DD format)
            to_date: End date (YYYY-MM-DD format)
            
        Returns:
            Attendance summary
        """
        logger.info(f"Getting attendance summary for employee: {employee}")
        
        # This would typically call a custom ERPNext API method
        # For now, return a placeholder
        result = {
            "employee": employee,
            "from_date": from_date,
            "to_date": to_date,
            "present_days": 0,
            "absent_days": 0,
            "half_days": 0,
            "message": "This would require a custom ERPNext API method to get real attendance summary"
        }
        
        return format_success_response(result, f"Attendance summary retrieved for {employee}")