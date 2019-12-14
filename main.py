#!/usr/bin/python3
from lexer import *
from parser import *
from ast_printer import *
import sys
import string
from code_writer import *
from instruction import *


def main():
	f = open(sys.argv[1], "r");
	contents = f.read();
	lexer = Lexer(contents);
	lexer.lex_while();
	#lexer.dump_tokens();

	parser = Parser(lexer.tokens);
	root = parser.parse_program();
	printer = AST_printer();
	
	#printer.display('root', root);

	root_scope = Scope(None);
	root.resolve_names(root_scope);
	root.check_types();
	
	writer = CodeWriter();
	root.gen_code(writer);
	writer.dump_code();

if __name__ == '__main__':
	main();
