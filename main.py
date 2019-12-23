#!/usr/bin/python3
from lexer import *
from parser import *
from ast_printer import *
import sys
import string
from code_writer import *
from instruction import *
<<<<<<< HEAD
from vm import *
=======
>>>>>>> 63feeeb22ce23a725d4aec7035f3098f509ee4d4


def main():
	f = open(sys.argv[1], "r");
	contents = f.read();
	lexer = Lexer(contents);
	lexer.lex_while();
<<<<<<< HEAD
	lexer.dump_tokens();

	if (lexer.error_counter is 0):
		parser = Parser(lexer.tokens);
		root = parser.parse_program();
		
		if (parser.error_counter is 0):
			printer = AST_printer();
			#printer.display('root', root);
			
			root_scope = Scope(None);
			root.resolve_names(root_scope);
			root.check_types();
			
			writer = CodeWriter();
			root.gen_code(writer);
			writer.dump_code();
			vm = VM(writer.code);
			#start_time = time.time();
			vm.exec();
			#elapsed_time = time.time() - start_time;
			#print(elapsed_time);

		else:
			sys.stderr.write("Cannot check types, there were some errors in parser\n");
		
	else:
		sys.stderr.write("Cannot parse code, there were some errors in lexer\n");
=======
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
>>>>>>> 63feeeb22ce23a725d4aec7035f3098f509ee4d4

if __name__ == '__main__':
	main();
