"""
ERPNext MCP Server

A comprehensive Model Context Protocol server exposing ERPNext operations
in business terms using frappe-client under the hood.
"""

__version__ = "0.1.0"
__author__ = "ASI Saga"

# Azure Functions HTTP trigger entry point
import azure.functions as func
import logging
from erpnext_mcp.server import main_handler

def main(req: func.HttpRequest) -> func.HttpResponse:
	logging.info('Python HTTP trigger function processed a request.')
	try:
		result = main_handler(req)
		return func.HttpResponse(result, status_code=200)
	except Exception as e:
		logging.error(f"Error: {e}")
		return func.HttpResponse(f"Error: {e}", status_code=500)