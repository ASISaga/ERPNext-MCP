# ERPNext-MCP Azure Functions Deployment

This folder is now ready to be deployed as an Azure Function App.

**Deployment Steps:**
1. Ensure you have the Azure Functions Core Tools and Azure CLI installed.
2. From this directory, run:
   ```pwsh
   func azure functionapp publish <YourFunctionAppName>
   ```
3. Set any required environment variables in Azure Portal or via `local.settings.json`.

**Structure:**
- `erpnext_mcp/` contains the function code and entry point (`__init__.py`).
- `function.json` defines the HTTP trigger binding.
- `host.json` and `local.settings.json` are for Azure Functions configuration.
- Dependencies are managed via `pyproject.toml`.

**Note:**
- You may need to add a `requirements.txt` for Azure Functions deployment if not using Oryx build with Poetry or PEP 517/518.
- Make sure all dependencies are included.
