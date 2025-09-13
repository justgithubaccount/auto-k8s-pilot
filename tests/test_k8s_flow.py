# tests/test_k8s_flow.py
import os
from crewai import Crew, Process
from auto_k8s_pilot.crew import AutoK8sPilot
from auto_k8s_pilot.tools import kubectl_tool as ktool
import litellm
import types

def test_k8s_health_flow(monkeypatch):
    # Фиктивный ответ для get/logs
    def fake_run(self, action, **kwargs):
        if action == "get":
            return "pod-1 1/1 Running 2d node-a\npod-2 0/1 CrashLoopBackOff 1h node-b\n"
        if action == "logs":
            return "ERROR failed to connect to db\nERROR failed to connect to db\nWARN retrying...\n"
        return "OK"

    monkeypatch.setattr(ktool.KubectlTool, "_run", fake_run)

    monkeypatch.setenv("OPENAI_API_KEY", "test")

    def fake_completion(*args, **kwargs):
        return types.SimpleNamespace(
            choices=[
                types.SimpleNamespace(
                    message=types.SimpleNamespace(content="pod-1 CrashLoopBackOff")
                )
            ]
        )

    monkeypatch.setattr(litellm, "completion", fake_completion)

    c = AutoK8sPilot()
    crew = Crew(
        agents=[c.k8s_operator(), c.reporting_analyst()],
        tasks=[c.k8s_pods_overview(), c.explain_pods()],
        process=Process.sequential,
        verbose=False,
    )
    res = crew.kickoff(inputs={"topic": "app", "namespace": "default", "selector": "app=web", "tail": 100})
    # smoke-проверка, что есть артефакты сводки
    assert "pod-1" in str(res) and "CrashLoopBackOff" in str(res)
