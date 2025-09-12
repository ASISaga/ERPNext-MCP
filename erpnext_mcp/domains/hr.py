"""HR domain operations for ERPNext."""

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


class HROperations:
    """HR domain operations."""

    def __init__(self, client: ERPNextClient):
        self.client = client

    def create_employee(
        self,
        employee_name: str,
        date_of_joining: str,
        department: Optional[str] = None,
        designation: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
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
            **kwargs,
        }

        # Map business parameters to DocType fields
        mapped_data = map_business_params_to_doctype_fields(
            employee_data, DocTypes.EMPLOYEE
        )

        # Validate required fields
        missing_fields = validate_required_fields(mapped_data, DocTypes.EMPLOYEE)
        if missing_fields:
            raise ValidationError(
                f"Missing required fields: {', '.join(missing_fields)}"
            )

        # Create the employee
        result = self.client.create_document(DocTypes.EMPLOYEE, mapped_data)

        return format_success_response(result, "Employee created successfully")

    def mark_attendance(
        self, employee: str, attendance_date: str, status: str, **kwargs
    ) -> Dict[str, Any]:
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
            **kwargs,
        }

        # Map business parameters to DocType fields
        mapped_data = map_business_params_to_doctype_fields(
            attendance_data, DocTypes.ATTENDANCE
        )

        # Create the attendance record
        result = self.client.create_document(DocTypes.ATTENDANCE, mapped_data)

        return format_success_response(result, "Attendance marked successfully")

    def create_leave_application(
        self,
        employee: str,
        leave_type: str,
        from_date: str,
        to_date: str,
        description: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
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
            **kwargs,
        }

        # Map business parameters to DocType fields
        mapped_data = map_business_params_to_doctype_fields(
            leave_data, DocTypes.LEAVE_APPLICATION
        )

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

    def get_employees_list(
        self, filters: Optional[Dict] = None, limit: int = 20
    ) -> Dict[str, Any]:
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

    def get_attendance_list(
        self, filters: Optional[Dict] = None, limit: int = 20
    ) -> Dict[str, Any]:
        """Get list of attendance records.

        Args:
            filters: Filter conditions
            limit: Maximum number of records

        Returns:
            List of attendance records
        """
        logger.info("Getting attendance list")

        result = self.client.get_list(DocTypes.ATTENDANCE, filters=filters, limit=limit)

        return format_success_response(
            result, "Attendance records retrieved successfully"
        )

    def get_leave_applications_list(
        self, filters: Optional[Dict] = None, limit: int = 20
    ) -> Dict[str, Any]:
        """Get list of leave applications.

        Args:
            filters: Filter conditions
            limit: Maximum number of records

        Returns:
            List of leave applications
        """
        logger.info("Getting leave applications list")

        result = self.client.get_list(
            DocTypes.LEAVE_APPLICATION, filters=filters, limit=limit
        )

        return format_success_response(
            result, "Leave applications retrieved successfully"
        )

    def approve_leave_application(self, leave_app_name: str) -> Dict[str, Any]:
        """Approve a leave application.

        Args:
            leave_app_name: Leave application name/ID

        Returns:
            Approved leave application data
        """
        logger.info(f"Approving leave application: {leave_app_name}")

        result = self.client.submit_document(DocTypes.LEAVE_APPLICATION, leave_app_name)

        return format_success_response(
            result, "Leave application approved successfully"
        )

    def get_employee_attendance_summary(
        self, employee: str, from_date: str, to_date: str
    ) -> Dict[str, Any]:
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
            "message": "This would require a custom ERPNext API method to get real attendance summary",
        }

        return format_success_response(
            result, f"Attendance summary retrieved for {employee}"
        )

    def create_leave_application(
        self, employee: str, leave_type: str, from_date: str, to_date: str, **kwargs
    ) -> Dict[str, Any]:
        """Create a leave application for an employee.

        Args:
            employee: Employee ID
            leave_type: Leave type (e.g., "Annual Leave", "Sick Leave")
            from_date: Leave start date (YYYY-MM-DD format)
            to_date: Leave end date (YYYY-MM-DD format)
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
            **kwargs,
        }

        # Map business parameters to DocType fields
        mapped_data = map_business_params_to_doctype_fields(
            leave_data, DocTypes.LEAVE_APPLICATION
        )

        # Validate required fields
        missing_fields = validate_required_fields(
            mapped_data, DocTypes.LEAVE_APPLICATION
        )
        if missing_fields:
            raise ValidationError(
                f"Missing required fields: {', '.join(missing_fields)}"
            )

        try:
            result = self.client.create_doc(DocTypes.LEAVE_APPLICATION, mapped_data)
            return format_success_response(
                result, "Leave Application created successfully"
            )
        except Exception as e:
            logger.error(f"Failed to create leave application: {str(e)}")
            raise

    def create_salary_structure(
        self, name: str, company: str, employee: str, **kwargs
    ) -> Dict[str, Any]:
        """Create a salary structure for an employee.

        Args:
            name: Salary structure name
            company: Company name
            employee: Employee ID
            **kwargs: Additional salary structure fields

        Returns:
            Created salary structure data
        """
        logger.info(f"Creating salary structure for employee: {employee}")

        # Prepare salary structure data
        salary_data = {"name": name, "company": company, "employee": employee, **kwargs}

        # Map business parameters to DocType fields
        mapped_data = map_business_params_to_doctype_fields(
            salary_data, DocTypes.SALARY_STRUCTURE
        )

        # Validate required fields
        missing_fields = validate_required_fields(
            mapped_data, DocTypes.SALARY_STRUCTURE
        )
        if missing_fields:
            raise ValidationError(
                f"Missing required fields: {', '.join(missing_fields)}"
            )

        try:
            result = self.client.create_doc(DocTypes.SALARY_STRUCTURE, mapped_data)
            return format_success_response(
                result, "Salary Structure created successfully"
            )
        except Exception as e:
            logger.error(f"Failed to create salary structure: {str(e)}")
            raise

    def create_salary_slip(
        self, employee: str, start_date: str, end_date: str, **kwargs
    ) -> Dict[str, Any]:
        """Create a salary slip for an employee.

        Args:
            employee: Employee ID
            start_date: Salary period start date (YYYY-MM-DD format)
            end_date: Salary period end date (YYYY-MM-DD format)
            **kwargs: Additional salary slip fields

        Returns:
            Created salary slip data
        """
        logger.info(f"Creating salary slip for employee: {employee}")

        # Prepare salary slip data
        slip_data = {
            "employee": employee,
            "start_date": start_date,
            "end_date": end_date,
            **kwargs,
        }

        # Map business parameters to DocType fields
        mapped_data = map_business_params_to_doctype_fields(
            slip_data, DocTypes.SALARY_SLIP
        )

        # Validate required fields
        missing_fields = validate_required_fields(mapped_data, DocTypes.SALARY_SLIP)
        if missing_fields:
            raise ValidationError(
                f"Missing required fields: {', '.join(missing_fields)}"
            )

        try:
            result = self.client.create_doc(DocTypes.SALARY_SLIP, mapped_data)
            return format_success_response(result, "Salary Slip created successfully")
        except Exception as e:
            logger.error(f"Failed to create salary slip: {str(e)}")
            raise

    def create_job_applicant(
        self, applicant_name: str, job_title: str, **kwargs
    ) -> Dict[str, Any]:
        """Create a job applicant record.

        Args:
            applicant_name: Applicant's name
            job_title: Job title applied for
            **kwargs: Additional job applicant fields

        Returns:
            Created job applicant data
        """
        logger.info(f"Creating job applicant: {applicant_name}")

        # Prepare job applicant data
        applicant_data = {
            "applicant_name": applicant_name,
            "job_title": job_title,
            **kwargs,
        }

        # Map business parameters to DocType fields
        mapped_data = map_business_params_to_doctype_fields(
            applicant_data, DocTypes.JOB_APPLICANT
        )

        # Validate required fields
        missing_fields = validate_required_fields(mapped_data, DocTypes.JOB_APPLICANT)
        if missing_fields:
            raise ValidationError(
                f"Missing required fields: {', '.join(missing_fields)}"
            )

        try:
            result = self.client.create_doc(DocTypes.JOB_APPLICANT, mapped_data)
            return format_success_response(result, "Job Applicant created successfully")
        except Exception as e:
            logger.error(f"Failed to create job applicant: {str(e)}")
            raise

    def approve_leave_application(self, leave_application_name: str) -> Dict[str, Any]:
        """Approve a leave application.

        Args:
            leave_application_name: Leave application name/ID

        Returns:
            Approved leave application data
        """
        logger.info(f"Approving leave application: {leave_application_name}")

        try:
            result = self.client.submit_doc(
                DocTypes.LEAVE_APPLICATION, leave_application_name
            )
            return format_success_response(
                result, "Leave Application approved successfully"
            )
        except Exception as e:
            logger.error(f"Failed to approve leave application: {str(e)}")
            raise

    def get_leave_applications_list(
        self,
        employee: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 20,
    ) -> Dict[str, Any]:
        """Get list of leave applications.

        Args:
            employee: Filter by employee (optional)
            status: Filter by status (optional)
            limit: Maximum number of records

        Returns:
            List of leave applications
        """
        logger.info(f"Getting leave applications list with limit: {limit}")

        try:
            filters = {}
            if employee:
                filters["employee"] = employee
            if status:
                filters["status"] = status

            result = self.client.get_list(
                DocTypes.LEAVE_APPLICATION,
                filters=filters,
                limit=limit,
                fields=[
                    "name",
                    "employee",
                    "leave_type",
                    "from_date",
                    "to_date",
                    "status",
                ],
            )
            return format_success_response(
                result, f"Retrieved {len(result)} leave applications"
            )
        except Exception as e:
            logger.error(f"Failed to get leave applications list: {str(e)}")
            raise
