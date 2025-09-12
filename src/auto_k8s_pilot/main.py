#!/usr/bin/env python
import sys
import warnings
from datetime import datetime

from auto_k8s_pilot.crew import AutoK8sPilot

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# --- Local runner for the Crew ------------------------------------------------
# This file is just an entrypoint to run your crew locally.
# Keep it simple: only pass runtime inputs if you really need to.
# Otherwise, tasks.yaml already describes what to run.


def run():
    """
    Run the crew (sequential process by default).
    """
    # Example: you can override inputs here if needed
    inputs = {
        "namespace": "all",  # or "default"
        "current_year": str(datetime.now().year),
    }

    try:
        AutoK8sPilot().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    try:
        AutoK8sPilot().crew().train(
            n_iterations=int(sys.argv[1]),
            filename=sys.argv[2],
            inputs={"current_year": str(datetime.now().year)},
        )
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        AutoK8sPilot().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """
    Test the crew execution and returns the results.
    """
    try:
        AutoK8sPilot().crew().test(
            n_iterations=int(sys.argv[1]),
            eval_llm=sys.argv[2],
            inputs={"current_year": str(datetime.now().year)},
        )
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
