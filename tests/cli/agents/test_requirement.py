import pytest
from cli.agents.requirement import RequirementAgent
from cli.core.context_bundle import ContextBundle

def test_requirement_agent_generate():
    agent = RequirementAgent()
    context = ContextBundle(user_instructions="test instructions")
    result = agent.generate(context)
    assert "Dummy requirement content" in result
