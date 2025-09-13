import os
from pathlib import Path

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

from crewai_tools import SerperDevTool
from auto_k8s_pilot.tools.kubectl_tool import KubectlTool
from auto_k8s_pilot.tools.argocd_tool import ArgoCDTool
from auto_k8s_pilot.tools.loki_tool import LokiQueryTool
from auto_k8s_pilot.tools.github_issue_tool import GitHubIssueTool

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = PROJECT_ROOT / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

@CrewBase
class AutoK8sPilot:
    """AutoK8sPilot crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['reporting_analyst'],
            verbose=True,
        )

    @agent
    def k8s_operator(self) -> Agent:
        return Agent(
            config=self.agents_config['k8s_operator'],
            verbose=True,
            tools=[KubectlTool()],
        )

    @agent
    def infra_architect(self) -> Agent:
        return Agent(
            config=self.agents_config['infra_architect'],
            verbose=True,
        )

    @agent
    def argocd_observer(self) -> Agent:
        return Agent(
            config=self.agents_config['argocd_observer'],
            verbose=True,
            tools=[ArgoCDTool()],
        )

    @agent
    def loki_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['loki_analyst'],
            verbose=True,
            tools=[LokiQueryTool()],
        )

    @agent
    def incident_triager(self) -> Agent:
        return Agent(
            config=self.agents_config['incident_triager'],
            verbose=True,
            tools=[GitHubIssueTool()],
        )

    @task
    def k8s_pods_overview(self) -> Task:
        return Task(
            config=self.tasks_config['k8s_pods_overview'],
            output_file="output/pods_overview.md",
        )

    @task
    def explain_pods(self) -> Task:
        return Task(
            config=self.tasks_config['explain_pods'],
            output_file="output/pods_explained.md",
        )

    @task
    def cluster_summary(self) -> Task:
        return Task(
            config=self.tasks_config['cluster_summary'],
            output_file="output/cluster_summary.md",
        )

    @task
    def k8s_top_nodes(self) -> Task:
        return Task(
            config=self.tasks_config['k8s_top_nodes'],
            output_file="output/top_nodes.md",
        )

    @task
    def k8s_top_pods_ns_default(self) -> Task:
        return Task(
            config=self.tasks_config['k8s_top_pods_ns_default'],
            output_file="output/top_pods_default.md",
        )

    @task
    def k8s_events_recent(self) -> Task:
        return Task(
            config=self.tasks_config['k8s_events_recent'],
            output_file="output/events.md",
        )

    @task
    def argocd_list_apps(self) -> Task:
        return Task(
            config=self.tasks_config['argocd_list_apps'],
            output_file="output/argocd_apps.md",
        )

    @task
    def argocd_app_status_chat_api(self) -> Task:
        return Task(
            config=self.tasks_config['argocd_app_status_chat_api'],
            output_file="output/argocd_chat_api_status.md",
        )

    @task
    def argocd_sync_chat_api(self) -> Task:
        return Task(
            config=self.tasks_config['argocd_sync_chat_api'],
            output_file="output/argocd_chat_api_sync.md",
        )

    @task
    def loki_recent_errors_chat_api(self) -> Task:
        return Task(
            config=self.tasks_config['loki_recent_errors_chat_api'],
            output_file="output/loki_chat_api_errors.md",
        )

    @task
    def loki_http_activity_chat_api(self) -> Task:
        return Task(
            config=self.tasks_config['loki_http_activity_chat_api'],
            output_file="output/loki_chat_api_http.md",
        )

    @task
    def incident_create_issue_if_needed(self) -> Task:
        return Task(
            config=self.tasks_config['incident_create_issue_if_needed'],
            output_file="output/incident_issue.md",
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )

