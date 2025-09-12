"""Projects domain operations for ERPNext."""

from typing import Dict, Any, List, Optional
import logging
from ..client.frappe_client import ERPNextClient
from ..utils.doctype_mapping import DocTypes, map_business_params_to_doctype_fields, validate_required_fields
from ..utils.error_handling import ValidationError, format_success_response


logger = logging.getLogger(__name__)


class ProjectsOperations:
    """Projects domain operations."""
    
    def __init__(self, client: ERPNextClient):
        self.client = client
    
    def create_project(self,
                      project_name: str,
                      project_type: Optional[str] = None,
                      customer: Optional[str] = None,
                      expected_start_date: Optional[str] = None,
                      expected_end_date: Optional[str] = None,
                      **kwargs) -> Dict[str, Any]:
        """Create a new project.
        
        Args:
            project_name: Project name
            project_type: Type of project
            customer: Associated customer
            expected_start_date: Project start date (YYYY-MM-DD format)
            expected_end_date: Project end date (YYYY-MM-DD format)
            **kwargs: Additional project fields
            
        Returns:
            Created project data
        """
        logger.info(f"Creating project: {project_name}")
        
        # Prepare project data
        project_data = {
            "project_name": project_name,
            "project_type": project_type,
            "customer": customer,
            "expected_start_date": expected_start_date,
            "expected_end_date": expected_end_date,
            **kwargs
        }
        
        # Map business parameters to DocType fields
        mapped_data = map_business_params_to_doctype_fields(project_data, DocTypes.PROJECT)
        
        # Validate required fields
        missing_fields = validate_required_fields(mapped_data, DocTypes.PROJECT)
        if missing_fields:
            raise ValidationError(f"Missing required fields: {', '.join(missing_fields)}")
        
        # Create the project
        result = self.client.create_document(DocTypes.PROJECT, mapped_data)
        
        return format_success_response(result, "Project created successfully")
    
    def create_task(self,
                   subject: str,
                   project: Optional[str] = None,
                   priority: str = "Medium",
                   status: str = "Open",
                   assigned_to: Optional[str] = None,
                   expected_start_date: Optional[str] = None,
                   expected_end_date: Optional[str] = None,
                   **kwargs) -> Dict[str, Any]:
        """Create a new task.
        
        Args:
            subject: Task title/subject
            project: Associated project
            priority: "Low", "Medium", "High", "Urgent"
            status: Task status
            assigned_to: User assigned to task
            expected_start_date: Task start date (YYYY-MM-DD format)
            expected_end_date: Task end date (YYYY-MM-DD format)
            **kwargs: Additional task fields
            
        Returns:
            Created task data
        """
        logger.info(f"Creating task: {subject}")
        
        # Prepare task data
        task_data = {
            "subject": subject,
            "project": project,
            "priority": priority,
            "status": status,
            "assigned_to": assigned_to,
            "exp_start_date": expected_start_date,
            "exp_end_date": expected_end_date,
            **kwargs
        }
        
        # Map business parameters to DocType fields
        mapped_data = map_business_params_to_doctype_fields(task_data, DocTypes.TASK)
        
        # Validate required fields
        missing_fields = validate_required_fields(mapped_data, DocTypes.TASK)
        if missing_fields:
            raise ValidationError(f"Missing required fields: {', '.join(missing_fields)}")
        
        # Create the task
        result = self.client.create_document(DocTypes.TASK, mapped_data)
        
        return format_success_response(result, "Task created successfully")
    
    def log_time(self,
                employee: str,
                hours: float,
                activity_type: str,
                from_time: str,
                to_time: str,
                project: Optional[str] = None,
                task: Optional[str] = None,
                **kwargs) -> Dict[str, Any]:
        """Log time in a timesheet.
        
        Args:
            employee: Employee ID
            hours: Hours worked
            activity_type: Type of activity
            from_time: Start time (HH:MM format)
            to_time: End time (HH:MM format)
            project: Associated project
            task: Associated task
            **kwargs: Additional timesheet fields
            
        Returns:
            Created timesheet data
        """
        logger.info(f"Logging {hours} hours for employee: {employee}")
        
        # Prepare timesheet data with time log
        timesheet_data = {
            "employee": employee,
            "time_logs": [{
                "activity_type": activity_type,
                "hours": hours,
                "from_time": from_time,
                "to_time": to_time,
                "project": project,
                "task": task
            }],
            **kwargs
        }
        
        # Map business parameters to DocType fields
        mapped_data = map_business_params_to_doctype_fields(timesheet_data, DocTypes.TIMESHEET)
        
        # Create the timesheet
        result = self.client.create_document(DocTypes.TIMESHEET, mapped_data)
        
        return format_success_response(result, "Time logged successfully")
    
    def get_project(self, project_name: str) -> Dict[str, Any]:
        """Get a project by name.
        
        Args:
            project_name: Project name/ID
            
        Returns:
            Project data
        """
        logger.info(f"Getting project: {project_name}")
        
        result = self.client.get_document(DocTypes.PROJECT, project_name)
        
        return format_success_response(result, "Project retrieved successfully")
    
    def get_task(self, task_name: str) -> Dict[str, Any]:
        """Get a task by name.
        
        Args:
            task_name: Task name/ID
            
        Returns:
            Task data
        """
        logger.info(f"Getting task: {task_name}")
        
        result = self.client.get_document(DocTypes.TASK, task_name)
        
        return format_success_response(result, "Task retrieved successfully")
    
    def get_projects_list(self,
                         filters: Optional[Dict] = None,
                         limit: int = 20) -> Dict[str, Any]:
        """Get list of projects.
        
        Args:
            filters: Filter conditions
            limit: Maximum number of records
            
        Returns:
            List of projects
        """
        logger.info("Getting projects list")
        
        result = self.client.get_list(DocTypes.PROJECT, filters=filters, limit=limit)
        
        return format_success_response(result, "Projects retrieved successfully")
    
    def get_tasks_list(self,
                      filters: Optional[Dict] = None,
                      limit: int = 20) -> Dict[str, Any]:
        """Get list of tasks.
        
        Args:
            filters: Filter conditions
            limit: Maximum number of records
            
        Returns:
            List of tasks
        """
        logger.info("Getting tasks list")
        
        result = self.client.get_list(DocTypes.TASK, filters=filters, limit=limit)
        
        return format_success_response(result, "Tasks retrieved successfully")
    
    def update_task_status(self, task_name: str, status: str) -> Dict[str, Any]:
        """Update task status.
        
        Args:
            task_name: Task name/ID
            status: New status
            
        Returns:
            Updated task data
        """
        logger.info(f"Updating task {task_name} status to: {status}")
        
        result = self.client.update_document(DocTypes.TASK, task_name, {"status": status})
        
        return format_success_response(result, f"Task status updated to {status}")
    
    def get_project_tasks(self, project_name: str) -> Dict[str, Any]:
        """Get all tasks for a project.
        
        Args:
            project_name: Project name
            
        Returns:
            List of project tasks
        """
        logger.info(f"Getting tasks for project: {project_name}")
        
        filters = [["project", "=", project_name]]
        result = self.client.get_list(DocTypes.TASK, filters=filters)
        
        return format_success_response(result, f"Tasks retrieved for project {project_name}")
    
    def get_timesheets_list(self,
                           filters: Optional[Dict] = None,
                           limit: int = 20) -> Dict[str, Any]:
        """Get list of timesheets.
        
        Args:
            filters: Filter conditions
            limit: Maximum number of records
            
        Returns:
            List of timesheets
        """
        logger.info("Getting timesheets list")
        
        result = self.client.get_list(DocTypes.TIMESHEET, filters=filters, limit=limit)
        
        return format_success_response(result, "Timesheets retrieved successfully")