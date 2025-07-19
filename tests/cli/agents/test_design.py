import pytest
from cli.agents.design import DesignAgent
from cli.core.context_bundle import ContextBundle

def test_design_agent_generate():
    agent = DesignAgent()
    context = ContextBundle(user_instructions="test instructions")
    result = agent.generate(context)
    assert "Dummy design content" in result
