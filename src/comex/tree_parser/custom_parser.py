import tempfile

from tree_sitter import Language, Parser
import os


class CustomParser:
    """Custom parser for the src_language"""

    def __init__(self, src_language, src_code):
        """Initialize the parser with the language.
        Language options are: python, java, c_sharp, ruby, go, php, javascript"""

        self.src_language = src_language
        self.src_code = src_code
        self.index = {}

        grandparent_folder = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        shared_languages = os.path.join(tempfile.gettempdir(), "comex", "languages.so")

        self.language = Language.build_library(
            # Store the library in the `build` directory
            shared_languages,
            [
                os.path.join(grandparent_folder, "vendor/tree-sitter-java"),
                os.path.join(grandparent_folder, "vendor/tree-sitter-c-sharp"),
                # "vendor/tree-sitter-ruby",
                # "vendor/tree-sitter-go",
                # "vendor/tree-sitter-php",
                # os.path.join(grandparent_folder,"vendor/tree-sitter-python"),
                # "vendor/tree-sitter-javascript",
            ],
        )
        # PYTHON_LANGUAGE = Language("build/my-languages.so", "python")
        JAVA_LANGUAGE = Language(shared_languages, "java")
        C_SHARP_LANGUAGE = Language(shared_languages, "c_sharp")
        # RUBY_LANGUAGE = Language("build/my-languages.so", "ruby")
        # GO_LANGUAGE = Language("build/my-languages.so", "go")
        # PHP_LANGUAGE = Language("build/my-languages.so", "php")
        # JAVASCRIPT_LANGUAGE = Language("build/my-languages.so", "javascript")

        self.language_map = {
            # "python": PYTHON_LANGUAGE,
            "java": JAVA_LANGUAGE,
            "cs": C_SHARP_LANGUAGE,
            # "ruby": RUBY_LANGUAGE,
            # "go": GO_LANGUAGE,
            # "php": PHP_LANGUAGE,
            # "javascript": JAVASCRIPT_LANGUAGE,
        }
        self.root_node, self.tree = self.parse()
        self.all_tokens = []  # list of all tokens in the source code
        self.label = {}  # label for each node in the AST
        self.method_map = []  # list of all methods in the source code
        self.method_calls = []  # list of all method calls in the source code
        self.start_line = {}  # start line number for each toekn (leaf-node) in the AST
        self.declaration = {}  # maps the declaration identifier token's index to the name of the variable/identifier
        self.declaration_map = {}
        self.symbol_table = {
            "scope_stack": [0],
            "scope_map": {},
            "scope_id": 0,
            "data_type": {},
        }  # Stack style symbol table which maps

    def create_AST_id(self, root_node, AST_index, AST_id):
        """Create an id for each node in the AST. This AST id is maintained and used across all code views so that
        it is possible to easily combine graphs"""
        if root_node.is_named:
            current_node_id = AST_id[0]
            AST_id[0] += 1
            AST_index[
                (root_node.start_point, root_node.end_point, root_node.type)
            ] = current_node_id
            for child in root_node.children:
                if child.is_named:
                    self.create_AST_id(child, AST_index, AST_id)
            return

    def parse(self):
        parser = Parser()  # tree-sitter parser
        parser.set_language(self.language_map[self.src_language])
        tree = parser.parse(bytes(self.src_code, "utf8"))
        self.root_node = tree.root_node
        # First few id values are reserved for special nodes such as start and end node
        self.create_AST_id(self.root_node, self.index, [5])
        return self.root_node, tree
