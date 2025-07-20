from tree_sitter_language_pack import get_language, get_parser

ELIXIR_LANGUAGE = get_language('elixir')

parser = get_parser('elixir')


with open('test_elixir.exs', 'rb') as file:
    tree = parser.parse(file.read())

def print_tree(node, indent=0):
    print(' ' * indent + f"{node.type} - {node.text.decode()}")
    for child in node.children:
        print_tree(child, indent + 2)

print_tree(tree.root_node)
