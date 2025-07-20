import pytest
from unittest.mock import MagicMock, patch
import networkx as nx
import io

from cli.agents.design import DesignAgent
from rich.console import Console
from cli.core.context_bundle import ContextBundle


def test_design_agent_generate():
    # Arrange
    mock_console = MagicMock(spec=Console)
    mock_console.status.return_value.__enter__.return_value = None
    agent = DesignAgent(console=mock_console)
    context = ContextBundle(user_instructions="test instructions", context="user provided context")

    mock_llm = MagicMock()
    mock_response = MagicMock()
    mock_response.content = "Generated design from LLM"
    mock_llm.invoke.return_value = mock_response
    agent.llm = mock_llm

    # Create a mock graph
    mock_graph = nx.DiGraph()
    mock_graph.add_node("node1")
    mock_graph.add_node("node2")
    mock_graph.add_edge("node1", "node2")

    # Serialize the mock graph to GML string
    mock_graph_gml = io.BytesIO()
    nx.write_gml(mock_graph, mock_graph_gml)
    mock_graph_gml_string = mock_graph_gml.getvalue().decode('utf-8')

    with patch("cli.agents.design.build_graph", return_value=mock_graph) as mock_build_graph, \
         patch.object(agent, "_render_prompt", return_value="Rendered Prompt") as mock_render:
        # Act
        result = agent.generate(context, project_path="/test/path")

        # Assert
        assert result == "Generated design from LLM"
        mock_build_graph.assert_called_once_with("/test/path")

        # Check that the context object passed to render is correct
        updated_context = mock_render.call_args.args[0]
        assert "## Project Code Graph" in updated_context.context
        assert mock_graph_gml_string in updated_context.context
        assert "## Additional Context from User" in updated_context.context
        assert "user provided context" in updated_context.context

        mock_render.assert_called_once()
        agent.llm.invoke.assert_called_once_with("Rendered Prompt")
