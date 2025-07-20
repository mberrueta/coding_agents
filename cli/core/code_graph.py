import os
import networkx as nx
from sentence_transformers import SentenceTransformer
from tree_sitter import Language, Parser

from tree_sitter import Parser
from tree_sitter_language_pack import get_language, get_parser

ELIXIR_LANGUAGE = get_language('elixir')

parser = get_parser('elixir')

embedder = SentenceTransformer('all-MiniLM-L6-v2')
G = nx.DiGraph()

def add_node(path, sig, kind):
    G.add_node(sig, file=path, kind=kind, embedding=embedder.encode(sig))

def _process_node(path, node, parent_signature=None):
    if node.type == 'call':
        identifier_node = node.child_by_field_name('function')
        if identifier_node and identifier_node.text.decode() in ['def', 'defmodule']:
            signature_node = node.child_by_field_name('arguments')
            if signature_node:
                if identifier_node.text.decode() == 'defmodule':
                    # For defmodule, the signature is just the module name
                    # The arguments node for defmodule is typically an alias node
                    if signature_node.type == 'alias':
                        signature = f"defmodule {signature_node.text.decode()}"
                    else:
                        signature = f"defmodule {signature_node.text.decode()}" # Fallback
                else:
                    # For def, the signature is the function name and arguments
                    signature = f"{identifier_node.text.decode()} {signature_node.text.decode()}"
                add_node(path, signature, identifier_node.text.decode())
                if parent_signature:
                    G.add_edge(parent_signature, signature)

                do_block_node = node.child_by_field_name('body')
                if do_block_node:
                    for child_of_do_block in do_block_node.children:
                        _process_node(path, child_of_do_block, signature)
        elif identifier_node: # It's a regular function call
            call_signature = node.text.decode()
            add_node(path, call_signature, 'call')
            if parent_signature:
                G.add_edge(parent_signature, call_signature)

def walk_tree(path, parent_node):
    for child in parent_node.children:
        _process_node(path, child)

def build_graph(project_path):
    global G # Clear the graph for each build
    G = nx.DiGraph()
    for root, _, files in os.walk(project_path):
        for f in files:
            if f.endswith('.ex') or f.endswith('.exs'):
                file_path = os.path.join(root, f)
                with open(file_path, 'rb') as file:
                    tree = parser.parse(file.read())
                walk_tree(file_path, tree.root_node)
    return G

def save_graph(graph, path):
    nx.write_gml(graph, path)
