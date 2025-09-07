# src/auto_k8s_pilot/tools/argocd_tool.py
import os, requests
from typing import Type, Literal, Optional
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

class ArgoInput(BaseModel):
    op: Literal["list_apps", "app_status", "app_sync"] = Field(..., description="Operation")
    app: Optional[str] = Field(None, description="Application name for status/sync")

class ArgoCDTool(BaseTool):
    name: str = "argocd_tool"
    description: str = (
        "Argo CD API wrapper. Read-only by default (list_apps, app_status). "
        "app_sync requires ALLOW_MUTATING=true."
    )
    args_schema: Type[BaseModel] = ArgoInput

    def _run(self, op: str, app: Optional[str] = None) -> str:
        base = os.getenv("ARGOCD_BASE_URL")
        token = os.getenv("ARGOCD_API_TOKEN")
        if not base or not token:
            return "ERROR: Set ARGOCD_BASE_URL and ARGOCD_API_TOKEN"

        headers = {"Authorization": f"Bearer {token}"}
        allow_mutating = os.getenv("ALLOW_MUTATING", "false").lower() in ("1","true","yes")

        try:
            if op == "list_apps":
                r = requests.get(f"{base}/api/v1/applications", headers=headers, timeout=10, verify=False)
                r.raise_for_status()
                items = [a.get("metadata", {}).get("name") for a in r.json().get("items", [])]
                return "Apps:\n" + "\n".join(items[:100])
            elif op == "app_status":
                if not app:
                    return "ERROR: 'app' required"
                r = requests.get(f"{base}/api/v1/applications/{app}", headers=headers, timeout=10, verify=False)
                r.raise_for_status()
                data = r.json()
                sync = data.get("status", {}).get("sync", {})
                health = data.get("status", {}).get("health", {})
                return f"App: {app}\nSync: {sync.get('status')}\nHealth: {health.get('status')}"
            elif op == "app_sync":
                if not allow_mutating:
                    return "ERROR: Mutating ops disabled (ALLOW_MUTATING=false)"
                if not app:
                    return "ERROR: 'app' required"
                r = requests.post(f"{base}/api/v1/applications/{app}/sync", headers=headers, timeout=10, verify=False)
                r.raise_for_status()
                return f"Triggered sync for {app}"
            else:
                return "ERROR: unsupported op"
        except Exception as e:
            return f"ERROR: Argo API failed ({e})"
