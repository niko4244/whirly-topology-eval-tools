"""
Open API & Extensibility:
- FastAPI endpoints for diagnostics, plugin management, and third-party integrations.
- Enables custom dashboards, external analysis modules, and developer experimentation.
"""

from fastapi import FastAPI, UploadFile, File
from typing import List, Dict

app = FastAPI()

# Example in-memory storage for diagnostics and plugins
diagnostics_store = {}
plugins_store = {}

@app.get("/diagnostics/{appliance_id}")
def get_diagnostics(appliance_id: str):
    """
    Get the latest diagnostic report for an appliance.
    """
    result = diagnostics_store.get(appliance_id, {"status": "No data"})
    return result

@app.post("/diagnostics/{appliance_id}")
def add_diagnostics(appliance_id: str, report: Dict):
    """
    Add or update a diagnostic report for an appliance.
    """
    diagnostics_store[appliance_id] = report
    return {"message": "Diagnostics updated", "report": report}

@app.post("/plugin")
def install_plugin(plugin_name: str, plugin_file: UploadFile = File(...)):
    """
    Register a new analysis plugin module.
    """
    plugins_store[plugin_name] = plugin_file.filename
    # TODO: Save/upload plugin file, validate, and load dynamically
    return {"message": f"Plugin {plugin_name} installed", "file": plugin_file.filename}

@app.get("/plugins")
def list_plugins():
    """
    List all installed plugins.
    """
    return list(plugins_store.keys())

@app.get("/status")
def system_status():
    """
    Get API system status and health.
    """
    return {"status": "ok", "plugins": list(plugins_store.keys())}