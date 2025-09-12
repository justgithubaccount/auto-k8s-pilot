import os
from pathlib import Path

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

from crewai_tools import SerperDevTool
from auto_k8s_pilot.tools.kubectl_tool import KubectlTool

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = PROJECT_ROOT / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

@CrewBase
class AutoK8sPilot:
    """AutoK8sPilot crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # @agent
    # def researcher(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config['researcher'],
    #         verbose=True,
    #         tools=[
    #             SerperDevTool(),
    #             KubectlTool(),
    #         ],
    #     )

    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['reporting_analyst'],
            verbose=True,
            # tools=[KubectlTool()],
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

    # @task
    # def research_task(self) -> Task:
    #     return Task(config=self.tasks_config['research_task'])

    # @task
    # def reporting_task(self) -> Task:
    #     return Task(
    #         config=self.tasks_config['reporting_task'],
    #         output_file='report.md'
    #     )

    # ← эти два таска нужны, чтобы k8s-задачи реально исполнялись
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

    # @task
    # def k8s_error_logs(self) -> Task:
    #     return Task(config=self.tasks_config['k8s_error_logs'])

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
