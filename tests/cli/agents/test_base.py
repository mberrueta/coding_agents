import os
import pytest
from cli.agents.base import BaseAgent
from cli.core.context_bundle import ContextBundle

class DummyAgent(BaseAgent):
    def generate(self, context: ContextBundle) -> str:
        return "dummy_implementation"

@pytest.fixture
def dummy_agent():
    template_path = "dummy_template.md.j2"
    with open(template_path, "w") as f:
        f.write("Hello, {{ user_instructions }}!")
    agent = DummyAgent(template_path)
    yield agent
    os.remove(template_path)

def test_render_prompt(dummy_agent):
    context = ContextBundle(user_instructions="World")
    prompt = dummy_agent._render_prompt(context)
    assert prompt == "Hello, World!"
