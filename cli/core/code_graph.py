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

def process_node(node, path, parent_sig=None):
    if node.type == 'call':
        function_node = node.child_by_field_name('function')
        if not function_node:
            return

        function_name = function_node.text.decode()
        
        if function_name == 'defmodule':
            args_node = node.child_by_field_name('arguments')
            if args_node:
                module_sig = f"defmodule {args_node.text.decode()}"
                add_node(path, module_sig, 'defmodule')
                body_node = node.child_by_field_name('body')
                if body_node:
                    for child in body_node.children:
                        process_node(child, path, module_sig)
        
        elif function_name == 'def':
            args_node = node.child_by_field_name('arguments')
            if args_node and args_node.children:
                def_sig = f"def {args_node.children[0].text.decode()}"
                add_node(path, def_sig, 'def')
                if parent_sig:
                    G.add_edge(parent_sig, def_sig)
                body_node = node.child_by_field_name('body')
                if body_node:
                    for child in body_node.children:
                        process_node(child, path, def_sig)

        elif parent_sig: # It's a regular call inside a def
            call_sig = node.text.decode()
            add_node(path, call_sig, 'call')
            G.add_edge(parent_sig, call_sig)

def build_graph(project_path):
    global G
    G = nx.DiGraph()
    for root, _, files in os.walk(project_path):
        for f in files:
            if f.endswith('.ex') or f.endswith('.exs'):
                file_path = os.path.join(root, f)
                with open(file_path, 'rb') as file:
                    tree = parser.parse(file.read())
                    for node in tree.root_node.children:
                        process_node(node, file_path)
    return G

def save_graph(graph, path):
    nx.write_gml(graph, path)
