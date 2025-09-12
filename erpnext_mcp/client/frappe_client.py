"""ERPNext Frappe Client wrapper with enhanced error handling and business operations."""

from frappeclient import FrappeClient
from typing import Dict, Any, List, Optional, Union
import logging
from ..config import config
from ..utils.error_handling import ERPNextError, handle_frappe_errors


logger = logging.getLogger(__name__)


class ERPNextClient:
    """Enhanced ERPNext client wrapper with business-friendly operations."""
    
    def __init__(self, 
                 url: Optional[str] = None,
                 username: Optional[str] = None, 
                 password: Optional[str] = None,
                 api_key: Optional[str] = None,
                 api_secret: Optional[str] = None,
                 verify_ssl: bool = True):
        """Initialize ERPNext client.
        
        Args:
            url: ERPNext site URL
            username: Username for authentication
            password: Password for authentication  
            api_key: API key for authentication
            api_secret: API secret for authentication
            verify_ssl: Whether to verify SSL certificates
        """
        self.url = url or config.erpnext_url
        self.username = username or config.erpnext_username
        self.password = password or config.erpnext_password
        self.api_key = api_key or config.erpnext_api_key
        self.api_secret = api_secret or config.erpnext_api_secret
        self.verify_ssl = verify_ssl if verify_ssl is not None else config.verify_ssl
        
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self) -> None:
        """Initialize the Frappe client."""
        try:
            self.client = FrappeClient(
                url=self.url,
                username=self.username,
                password=self.password,
                api_key=self.api_key,
                api_secret=self.api_secret,
                verify=self.verify_ssl
            )
            logger.info(f"ERPNext client initialized for {self.url}")
        except Exception as e:
            logger.error(f"Failed to initialize ERPNext client: {str(e)}")
            raise ERPNextError(f"Failed to connect to ERPNext: {str(e)}")
    
    @handle_frappe_errors
    def create_document(self, doctype: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new document.
        
        Args:
            doctype: The DocType to create
            data: Document data
            
        Returns:
            Created document data
        """
        logger.info(f"Creating {doctype} document")
        result = self.client.insert(doctype, data)
        return result
    
    @handle_frappe_errors
    def get_document(self, doctype: str, name: str) -> Dict[str, Any]:
        """Get a document by name.
        
        Args:
            doctype: The DocType
            name: Document name
            
        Returns:
            Document data
        """
        logger.info(f"Getting {doctype} document: {name}")
        result = self.client.get_doc(doctype, name)
        return result
    
    @handle_frappe_errors
    def update_document(self, doctype: str, name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a document.
        
        Args:
            doctype: The DocType
            name: Document name  
            data: Updated document data
            
        Returns:
            Updated document data
        """
        logger.info(f"Updating {doctype} document: {name}")
        # Get existing document and merge with updates
        existing = self.client.get_doc(doctype, name)
        existing.update(data)
        result = self.client.update(existing)
        return result
    
    @handle_frappe_errors
    def delete_document(self, doctype: str, name: str) -> Dict[str, Any]:
        """Delete a document.
        
        Args:
            doctype: The DocType
            name: Document name
            
        Returns:
            Success confirmation
        """
        logger.info(f"Deleting {doctype} document: {name}")
        self.client.delete(doctype, name)
        return {"message": f"Document {doctype} {name} deleted successfully"}
    
    @handle_frappe_errors
    def submit_document(self, doctype: str, name: str) -> Dict[str, Any]:
        """Submit a document.
        
        Args:
            doctype: The DocType
            name: Document name
            
        Returns:
            Submitted document data
        """
        logger.info(f"Submitting {doctype} document: {name}")
        result = self.client.submit(doctype, name)
        return result
    
    @handle_frappe_errors  
    def cancel_document(self, doctype: str, name: str) -> Dict[str, Any]:
        """Cancel a document.
        
        Args:
            doctype: The DocType
            name: Document name
            
        Returns:
            Cancelled document data
        """
        logger.info(f"Cancelling {doctype} document: {name}")
        result = self.client.cancel(doctype, name)
        return result
    
    @handle_frappe_errors
    def get_list(self, doctype: str, filters: Optional[Dict] = None, 
                 fields: Optional[List[str]] = None, limit: int = 20) -> List[Dict[str, Any]]:
        """Get a list of documents.
        
        Args:
            doctype: The DocType
            filters: Filter conditions
            fields: Fields to fetch
            limit: Maximum number of records
            
        Returns:
            List of documents
        """
        logger.info(f"Getting {doctype} list with filters: {filters}")
        result = self.client.get_list(doctype, filters=filters, fields=fields, limit=limit)
        return result
    
    @handle_frappe_errors
    def search_documents(self, doctype: str, query: str, fields: Optional[List[str]] = None,
                        limit: int = 10) -> List[Dict[str, Any]]:
        """Search documents by query.
        
        Args:
            doctype: The DocType
            query: Search query
            fields: Fields to fetch
            limit: Maximum number of records
            
        Returns:
            List of matching documents
        """
        logger.info(f"Searching {doctype} with query: {query}")
        # Use get_list with name filter containing the query
        filters = [["name", "like", f"%{query}%"]]
        result = self.client.get_list(doctype, filters=filters, fields=fields, limit=limit)
        return result
    
    @handle_frappe_errors
    def call_api(self, method: str, params: Optional[Dict] = None) -> Any:
        """Call a custom API method.
        
        Args:
            method: API method name
            params: Method parameters
            
        Returns:
            API response
        """
        logger.info(f"Calling API method: {method}")
        result = self.client.get_api(method, params or {})
        return result