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

@pytest.mark.skip(reason="Elixir parsing is not stable")
def test_build_graph_simple_module(elixir_project):
    graph = build_graph(str(elixir_project))

    # Assert that the graph contains the expected nodes and their kinds
    nodes = {data['kind']: node for node, data in graph.nodes(data=True)}
    assert "defmodule" in nodes.values()
    assert "def" in nodes.values()
    
    module_node = [n for n, d in graph.nodes(data=True) if d['kind'] == 'defmodule'][0]
    assert module_node == "defmodule MyApp.MyModule"

    def_nodes = [n for n, d in graph.nodes(data=True) if d['kind'] == 'def']
    assert "def greet(name)" in def_nodes
    assert "def farewell(name)" in def_nodes

    # Assert that the graph contains the expected edges (function calls)
    edges = list(graph.edges())
    assert ("def farewell(name)", "greet(name)") in edges
