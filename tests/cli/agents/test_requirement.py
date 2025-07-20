import pytest
from unittest.mock import MagicMock, patch
from cli.agents.requirement import RequirementAgent
from cli.core.context_bundle import ContextBundle


def test_requirement_agent_generate():
    # Arrange
    mock_console = MagicMock()
    agent = RequirementAgent(console=mock_console)
    context = ContextBundle(user_instructions="test instructions", context="user provided context")

    mock_llm = MagicMock()
    mock_response = MagicMock()
    mock_response.content = "Generated requirement from LLM"
    mock_llm.invoke.return_value = mock_response
    agent.llm = mock_llm

    with patch.object(agent, "_gather_project_context", return_value="Mocked Project Context") as mock_gather, \
         patch.object(agent, "_render_prompt", return_value="Rendered Prompt") as mock_render, \
         patch.object(agent, "_get_clarifying_questions", return_value=None) as mock_questions:
        # Act
        result = agent.generate(context, project_path="/test/path")

        # Assert
        assert result == "Generated requirement from LLM"
        mock_gather.assert_called_once_with("/test/path")
        mock_questions.assert_called_once()

        # Check that the context object passed to render is correct
        updated_context = mock_render.call_args.args[0]
        assert "## Project Context" in updated_context.context
        assert "Mocked Project Context" in updated_context.context
        assert "## Additional Context from User" in updated_context.context
        assert "user provided context" in updated_context.context

        mock_render.assert_called_once()
        agent.llm.invoke.assert_called_once_with("Rendered Prompt")
