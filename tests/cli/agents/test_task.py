import pytest
from cli.agents.task import TaskAgent
from cli.core.context_bundle import ContextBundle

def test_task_agent_generate():
    agent = TaskAgent()
    context = ContextBundle(user_instructions="test instructions")
    result = agent.generate(context)
    assert "Dummy task content" in result
