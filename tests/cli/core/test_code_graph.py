import os
import pytest
import networkx as nx
from cli.core.code_graph import build_graph

@pytest.fixture
def elixir_project(tmp_path):
    # Create a dummy Elixir project structure
    (tmp_path / "lib").mkdir()
    (tmp_path / "lib" / "my_app").mkdir()
    (tmp_path / "lib" / "my_app" / "my_module.ex").write_text("""
defmodule MyApp.MyModule do
  def greet(name) do
    IO.puts("Hello, " <> name)
  end

  def farewell(name) do
    greet(name)
    IO.puts("Goodbye, " <> name)
  end
end
""")
    return tmp_path

def test_build_graph_simple_module(elixir_project):
    graph = build_graph(str(elixir_project))

    # Assert that the graph contains the expected nodes and their kinds
    assert ("defmodule MyApp.MyModule", {'file': str(elixir_project / "lib" / "my_app" / "my_module.ex"), 'kind': 'defmodule'}) in graph.nodes(data=True)
    assert ("def greet(name)", {'file': str(elixir_project / "lib" / "my_app" / "my_module.ex"), 'kind': 'def'}) in graph.nodes(data=True)
    assert ("def farewell(name)", {'file': str(elixir_project / "lib" / "my_app" / "my_module.ex"), 'kind': 'def'}) in graph.nodes(data=True)

    # Assert that the graph contains the expected edges (function calls)
    edges = list(graph.edges())
    assert ("def farewell(name)", "greet(name)") in edges
