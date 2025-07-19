import pytest
from unittest.mock import MagicMock, patch
from cli.agents.requirement import RequirementAgent
from cli.core.context_bundle import ContextBundle


def test_requirement_agent_generate():
    # Arrange
    agent = RequirementAgent()
    context = ContextBundle(user_instructions="test instructions")

    mock_llm = MagicMock()
    mock_response = MagicMock()
    mock_response.content = "Generated requirement from LLM"
    mock_llm.invoke.return_value = mock_response
    agent.llm = mock_llm

    with patch.object(agent, "_render_prompt", return_value="Rendered Prompt") as mock_render:
        # Act
        result = agent.generate(context)

        # Assert
        assert result == "Generated requirement from LLM"
        mock_render.assert_called_once_with(context)
        agent.llm.invoke.assert_called_once_with("Rendered Prompt")
