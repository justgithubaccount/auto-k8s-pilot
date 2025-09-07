# tests/test_k8s_flow.py
import os
from crewai import Crew, Process
from latest_ai_development.crew import LatestAiDevelopment
from latest_ai_development.tools import kubectl_tool as ktool

def test_k8s_health_flow(monkeypatch):
    # Фиктивный ответ для get/logs
    def fake_run(self, action, **kwargs):
        if action == "get":
            return "pod-1 1/1 Running 2d node-a\npod-2 0/1 CrashLoopBackOff 1h node-b\n"
        if action == "logs":
            return "ERROR failed to connect to db\nERROR failed to connect to db\nWARN retrying...\n"
        return "OK"

    monkeypatch.setattr(ktool.KubectlTool, "_run", fake_run)

    c = LatestAiDevelopment()
    # В smoke-тесте берём только k8s-оператора и k8s-таски
    crew = Crew(
        agents=[c.k8s_operator()],
        tasks=[c.k8s_pods_overview(), c.k8s_error_logs()],
        process=Process.sequential,
        verbose=False,
    )
    res = crew.kickoff(inputs={"topic": "app", "namespace": "default", "selector": "app=web", "tail": 100})
    # smoke-проверка, что есть артефакты сводки
    assert "pod-1" in str(res) and "CrashLoopBackOff" in str(res)
