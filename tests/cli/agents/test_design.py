import pytest
from unittest.mock import MagicMock, patch
import networkx as nx
import io

from cli.agents.design import DesignAgent
from rich.console import Console
from cli.core.context_bundle import ContextBundle


def test_design_agent_generate_default_requirement(tmp_path):
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

    # Create a dummy requirement file at the default path
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    requirement_path = output_dir / "requirement.md"
    requirement_path.write_text("Default requirement.")

    with patch("cli.agents.design.build_graph", return_value=mock_graph) as mock_build_graph, \
         patch.object(agent, "_get_dependencies", return_value="mocked dependencies") as mock_get_deps, \
         patch.object(agent, "_render_prompt", return_value="Rendered Prompt") as mock_render, \
         patch("builtins.open", MagicMock(side_effect=[io.StringIO("Default requirement.")])):
        # Act
        # We need to change the working directory so the relative path works
        import os
        with patch.object(os, "getcwd", return_value=str(tmp_path)):
            result = agent.generate(context, project_path="/test/path")

        # Assert
        assert result == "Generated design from LLM"
        
        updated_context = mock_render.call_args.args[0]
        assert "Default requirement." in updated_context.context


