#!/usr/bin/env python
import sys
import string

letter_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L'
'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '_'];

digit_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'];

class Token:
	def __init__(self, line_no, token_type, value):
		self.line_no = line_no;
		self.token_type = token_type;
		self.token_value = value;
		
	def dump_tokens(self):
		temp = '{0: <4}'.format(str(self.line_no)) + '|' + '{0: <15}'.format(self.token_type);
		print(temp + '| ' + str(self.token_value));

class Lexer:
	def  __init__(self, input_):
		self.start_ln = 1;
		self.current_ln = 1;
		self.buffer = "";
		
		self.keywords = ["while", "if", "else", "return", "continue", "break", "int", "float", "string", "char", "fun", "void", "out", "bool", "true", "false"];
		
		self.tokens = [];
		self.offset = 0;
		self.state = "START";
		self.running = 1;
		self.input = input_;
		self.curr_char = '';
<<<<<<< HEAD
		self.error_counter = 0;
=======
>>>>>>> 63feeeb22ce23a725d4aec7035f3098f509ee4d4
	
	def add(self):
		self.buffer += self.curr_char;
		
	def begin_token(self, new_state):
		self.token_start = self.offset;
		self.start_ln = self.current_ln;
		self.state = new_state;
		
	def complete_token(self, token_type, advance):
		if advance == 0: # if advance is false, return the offset to the position before
			self.offset = self.offset - 1;
			
		self.tokens.append(Token(self.current_ln, token_type, self.buffer));
		
		self.buffer = "";
		self.state = "START";
		self.advance = 1; 
	
	def lex_while(self):
		self.offset = 0;
		self.running = 1;
		while (self.running == 1) and (self.offset < len(self.input)):
			self.curr_char = self.input[self.offset];
			self.lex_all();
			self.offset += 1;
			
		self.curr_char = ' ';
		self.lex_all();
		self.curr_char = 'EOF';
		self.lex_all();
	
	def lex_comment(self):		
		if(self.curr_char == '*'):	
			self.state = "COMMENT_MULTI";
		elif(self.curr_char == '\n'):
			self.current_ln = self.current_ln+1;
			self.state = "START"
		elif(self.curr_char != '*' and self.curr_char != '\n'):
			pass;
		else:
			self.error("Unrecognized comment symbol '" + self.curr_char + "'");
	
	def lex_comment_multi(self):
		if(self.curr_char == '\n'):
			self.current_ln = self.current_ln+1;
		elif (self.curr_char == '*'):
			self.offset += 1;
			self.curr_char = self.input[self.offset];
			if(self.curr_char == "#"):
				self.state = "START";
			else:
				pass;
		elif(self.curr_char != '*' and self.curr_char != '\n'):
			pass;
		else:
			self.error("Unrecognized multi-line comment symbol '" + self.curr_char + "'");			
	
	def lex_lit_int(self):
		if(self.curr_char in digit_list):
			self.add();
		elif(self.curr_char == '.'):
			self.add();
			self.state = "LIT_FLOAT";
		elif(self.curr_char in letter_list):
			self.error("Invalid suffix: '" + self.curr_char + "'");
		else:
			self.complete_token("LIT_INT", 0);
	
	def lex_lit_float(self):
		if(self.curr_char in digit_list):
			self.add();
		elif(self.curr_char == 'e'):
			self.add();
		elif(self.curr_char == '.'):
			self.error("Invalid suffix: '" + self.curr_char + "'");
		elif(self.curr_char in letter_list):
			self.error("Invalid suffix: '" + self.curr_char + "'");
		else:
			self.complete_token("LIT_FLOAT", 0);
	
	def lex_ident(self):
		if(self.curr_char in letter_list):
			self.add();
		elif(self.curr_char in digit_list):
			self.add();
		elif(self.buffer in self.keywords):
			self.lex_keywords();
		elif(self.curr_char == 'EOF'):
			self.complete_token("IDENT", 0);
			self.complete_token("EOF", 0);
		else:
			self.complete_token("IDENT", 0);
	
	def lex_keywords(self):
		if(self.buffer == "while"):
			self.buffer = "";
			self.complete_token("KW_WHILE", 0);
		elif(self.buffer == "if"):
			self.buffer = "";
			self.complete_token("KW_IF", 0);
		elif(self.buffer == "else"):
			self.buffer = "";
			self.complete_token("KW_ELSE", 0);
		elif(self.buffer == "return"):
			self.buffer = "";
			self.complete_token("KW_RETURN", 0);
		elif(self.buffer == "continue"):
			self.buffer = "";
			self.complete_token("KW_CONTINUE", 0);
		elif(self.buffer == "break"):
			self.buffer = "";
			self.complete_token("KW_BREAK", 0);
		elif(self.buffer == "int"):
			self.buffer = "";
			self.complete_token("KW_INT", 0);
		elif(self.buffer == "float"):
			self.buffer = "";
			self.complete_token("KW_FLOAT", 0);
		elif(self.buffer == "string"):
			self.buffer = "";
			self.complete_token("KW_STRING", 0);
		elif(self.buffer == "char"):
			self.buffer = "";
			self.complete_token("KW_CHAR", 0);
		elif(self.buffer == "bool"):
			self.buffer = "";
			self.complete_token("KW_BOOL", 0);
		elif(self.buffer == "true"):
<<<<<<< HEAD
			self.complete_token("LIT_BOOL", 0);
		elif(self.buffer == "false"):
=======
			self.buffer = "";
			self.complete_token("LIT_BOOL", 0);
		elif(self.buffer == "false"):
			self.buffer = "";
>>>>>>> 63feeeb22ce23a725d4aec7035f3098f509ee4d4
			self.complete_token("LIT_BOOL", 0);
		elif(self.buffer == "fun"):
			self.buffer = "";
			self.complete_token("KW_FUN", 0);
		elif(self.buffer == "void"):
			self.buffer = "";
			self.complete_token("KW_VOID", 0);
		else:
			self.error("Unidentified keyword " + "'" + self.buffer + "' ");

	def lex_lit_str(self):
		if(self.curr_char == '"'):
			self.complete_token("LIT_STR", 1);
		elif(self.curr_char == "\\"):
			self.state = "LIT_STR_ESCAPE";
		elif(self.curr_char == "\n"):
			self.add();
			self.current_ln = self.current_ln + 1;
		elif(self.curr_char == 'EOF'):
			self.error("Reached EOF without string termination");
		else:
			self.add();
	
	def lex_lit_str_escape(self):
		if(self.curr_char == '"'):
			self.buffer += '\"';
		elif(self.curr_char == 'n'):
			self.current_ln = self.current_ln + 1;
			self.buffer += "\n"
		elif(self.curr_char == 't'):
			self.buffer += "\t"
		else:
			self.error("String escape not terminated");		
		self.state = "LIT_STR";
	
	def lex_lit_char(self):
		if((self.curr_char >= ' ') and (self.curr_char <= '~') and (self.curr_char != "'")):
			self.add();
			self.offset += 1;
			self.curr_char = self.input[self.offset];
			if(self.curr_char == "'"):
				self.complete_token("LIT_CHAR", 1);
			else:
				self.offset = self.offset - 2;
				self.curr_char = self.input[self.offset];
				self.buffer = "";
				self.add();
				self.complete_token("APOSTROPHE", 1);
		elif(self.curr_char == "'"):
			self.add();
			self.complete_token("APOSTROPHE", 0);
		else:
			self.error("Unrecognized symbol " + " '" + self.curr_char + "' ");
				
	def lex_op_plus(self):
		if(self.curr_char == '+'):
			self.complete_token("OP_INC", 1);
		elif(self.curr_char == '='):
			self.complete_token("OP_PLUS_ASSIGN", 1);
		else:
			self.complete_token("OP_PLUS", 0);
			
	def lex_op_minus(self):
		if(self.curr_char == '-'):
			self.complete_token("OP_DEC", 1);
		elif(self.curr_char == '='):
			self.complete_token("OP_MINUS_ASSIGN", 1);
		elif(self.curr_char == '>'):
			self.complete_token("STDOUT", 1);
<<<<<<< HEAD
		elif(self.curr_char == '<'):
			self.complete_token("STDIN", 1);
=======
>>>>>>> 63feeeb22ce23a725d4aec7035f3098f509ee4d4
		else:
			self.complete_token("OP_MINUS", 0);
			
	def lex_op_mul(self):
		if(self.curr_char == '='):
			self.complete_token("OP_MUL_ASSIGN", 1);
		else:
			self.complete_token("OP_MUL", 0);
			
	def lex_op_div(self):
		if(self.curr_char == '='):
			self.complete_token("OP_DIV_ASSIGN", 1);
		else:
			self.complete_token("OP_DIV", 0);
			
	def lex_op_mod(self):
		if(self.curr_char == '='):
			self.complete_token("OP_MOD_ASSIGN", 1);
		else:
			self.complete_token("OP_MOD", 0);
		
	def lex_op_l(self):
		if(self.curr_char == '='):
			self.complete_token("OP_LE", 1);
		else:
			self.complete_token("OP_L", 0);
		
	def lex_op_g(self):
		if(self.curr_char == '='):
			self.complete_token("OP_GE", 1);
		else:
			self.complete_token("OP_G", 0);
	
	def lex_op_assign(self):
		if(self.curr_char == '='):
			self.complete_token("OP_COMPARE", 1);
		else:
			self.complete_token("OP_ASSIGN", 0);
			
	def lex_op_not(self):
		if(self.curr_char == '='):
			self.complete_token("OP_NOT_ASSIGN", 1);
		else:
			self.complete_token("OP_NOT", 1);
			
	def lex_op_and(self):
		if(self.curr_char == '&'):
			self.complete_token("OP_AND", 1);
		else:
			self.error("Unrecognized symbol: %s" % (self.curr_char));
			
	def lex_op_or(self):
		if(self.curr_char == '|'):
			self.complete_token("OP_OR", 1);
		else:
			self.error("Unrecognized symbol: %s" % (self.curr_char));
		
	def lex_all(self):		
		if(self.state == "COMMENT"):
			self.lex_comment();
		elif(self.state == "COMMENT_MULTI"):
			self.lex_comment_multi();
		elif(self.state == "IDENT"):
			self.lex_ident();
		elif(self.state == "LIT_INT"):
			self.lex_lit_int();
		elif(self.state == "LIT_FLOAT"):
			self.lex_lit_float();
		elif(self.state == "LIT_STR"):
			self.lex_lit_str();
		elif(self.state == "LIT_CHAR"):
			self.lex_lit_char();
		elif(self.state == "LIT_STR_ESCAPE"):
			self.lex_lit_str_escape();
		elif(self.state == "OP_PLUS"):
			self.lex_op_plus();
		elif(self.state == "OP_MINUS"):
			self.lex_op_minus();
		elif(self.state == "OP_MUL"):
			self.lex_op_mul();
		elif(self.state == "OP_DIV"):
			self.lex_op_div();
		elif(self.state == "OP_MOD"):
			self.lex_op_mod();
		elif(self.state == "OP_G"):
			self.lex_op_g();
		elif(self.state == "OP_L"):
			self.lex_op_l();
		elif(self.state == "OP_ASSIGN"):
			self.lex_op_assign();
		elif(self.state == "OP_NOT"):
			self.lex_op_not();
		elif(self.state == "OP_AND"):
			self.lex_op_and();
		elif(self.state == "OP_OR"):
			self.lex_op_or();
		elif(self.state == "START"):
			self.lex_start();
		else:
			self.error("Unrecognized token " + self.state);
	
	
	def lex_start(self):
		if(self.curr_char == '#'):
			self.begin_token("COMMENT");	
		
		elif(self.curr_char in letter_list):
			self.add();
			self.begin_token("IDENT");
		elif(self.curr_char in digit_list):
			self.add();
			self.begin_token("LIT_INT");
			
		elif(self.curr_char == '+'):
			self.begin_token("OP_PLUS");
		elif(self.curr_char == '-'):
			self.begin_token("OP_MINUS");
		elif(self.curr_char == '*'):
			self.begin_token("OP_MUL");
		elif(self.curr_char == '/'):
			self.begin_token("OP_DIV");
		elif(self.curr_char == '%'):
			self.begin_token("OP_MOD");
			
		elif(self.curr_char == '('):
			self.begin_token("START");
			self.complete_token("OP_ROUND_OPEN", 1);
		elif(self.curr_char == ')'):
			self.begin_token("START");
			self.complete_token("OP_ROUND_CLOSE", 1);
		elif(self.curr_char == '{'):
			self.begin_token("START");
			self.complete_token("OP_CURLY_OPEN", 1);
		elif(self.curr_char == '}'):
			self.begin_token("START");
			self.complete_token("OP_CURLY_CLOSE", 1);
			
		elif(self.curr_char == '^'):
			self.begin_token("START");
			self.complete_token("OP_POW", 1);
		
		elif(self.curr_char == ';'):
			self.begin_token("START");
			self.complete_token("OP_SEMICOLON", 1);
		elif(self.curr_char == ','):
			self.begin_token("START");
			self.complete_token("OP_COMMA", 1);		
			
		elif(self.curr_char == '"'):
			self.begin_token("LIT_STR");
		elif(self.curr_char == "'"):
			self.begin_token("LIT_CHAR");
		elif(self.curr_char == '\n'):
			self.current_ln = self.current_ln + 1;
		elif(self.curr_char == ' '):
			pass;
		elif(self.curr_char == '	'):
			pass;
		
		elif(self.curr_char == '<'):
			self.begin_token("OP_L");
		elif(self.curr_char == '>'):
			self.begin_token("OP_G");
		elif(self.curr_char == '='):
			self.begin_token("OP_ASSIGN");
		elif(self.curr_char == '!'):
			self.begin_token("OP_NOT");	
			
		elif(self.curr_char == '|'):
			self.begin_token("OP_OR");
		elif(self.curr_char == '&'):
			self.begin_token("OP_AND");
		
		elif(self.curr_char == 'EOF'):
			self.start_ln = self.current_ln;
			self.complete_token("EOF", 1);
			self.running = 0; # stopping main while, since it's the EOF
		
		else:
			self.error("Unrecognized symbol found: " + self.curr_char);
	
	def dump_tokens(self):
		print('{0: <4}'.format('LINE') + '|' + ' {0: <14}'.format('TYPE') + '| VALUE');
		print('{0: <4}'.format('----') + '+' + '{0: <14}'.format('-' * 15) + '+' + '-' * 20);
		for i in self.tokens:
			i.dump_tokens(); 
	
	def error(self, error_code):
		self.buffer = "";
<<<<<<< HEAD
		#sys.stderr.write("LEXER ERROR: " + error_code + " on line "  + str(self.current_ln) + " in file: " + sys.argv[1] + "\n"); 
		sys.stderr.write(sys.argv[1] + ":" + str(self.current_ln)+ ": Error: " + error_code + "\n");
		self.error_counter += 1;
=======
		sys.stderr.write("LEXER ERROR: " + error_code + " on line "  + str(self.current_ln) + " in file: " + sys.argv[1] + "\n"); 
>>>>>>> 63feeeb22ce23a725d4aec7035f3098f509ee4d4
		self.running = 0;
