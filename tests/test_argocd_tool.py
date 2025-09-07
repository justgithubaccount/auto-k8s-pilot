import os, json
from auto_k8s_pilot.tools.argocd_tool import ArgoCDTool

class Resp:
    def __init__(self, payload, status=200):
        self._payload = payload
        self.status_code = status
    def raise_for_status(self): pass
    def json(self): return self._payload

def test_list_apps(monkeypatch):
    os.environ["ARGOCD_BASE_URL"] = "https://argocd.example.com"
    os.environ["ARGOCD_API_TOKEN"] = "xxx"

    def fake_get(url, headers, timeout, verify):
        return Resp({"items": [{"metadata": {"name": "app-a"}}, {"metadata": {"name": "app-b"}}]})

    import requests
    monkeypatch.setattr(requests, "get", fake_get)

    tool = ArgoCDTool()
    out = tool._run(op="list_apps")
    assert "app-a" in out and "app-b" in out
