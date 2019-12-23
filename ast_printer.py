from lexer import *
from ast import Node

class AST_printer:
    def __init__(self):
        self.ident = 0

    def display(self, title, obj):
        o_type = type(obj)
        if o_type is list:
            self.print_list(title, obj)
        elif o_type is str:
            self.print_text(title, obj)
        elif o_type is int:
            self.print_text(title, obj)
        elif o_type is Token:
            self.print_token(title, obj)
        else:
            self.print_node(title, obj)


    def print_list(self, title, obj):
        if not obj:
            return self.print_text(title, '[]')

        obj_size = len(obj)
        for i in range(0, obj_size):
            elem_title = title + '[' + str(i) + ']'
            self.display(elem_title, obj[i])

    def print_node(self, title, node):
        if node is not None:
            self.print_text(title, type(node).__name__)
            self.ident += 1
            node.print_node(self)
            self.ident -= 1

    def print_text(self, title, text):
        prefix = '  ' * self.ident
        print(prefix + str(title) + ': ' + str(text))

    def print_token(self, title, token):
        self.print_text(title, token.token_value + ' ');
