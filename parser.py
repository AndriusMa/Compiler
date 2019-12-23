import sys
from ast import *
<<<<<<< HEAD
from lexer import *
=======
>>>>>>> 63feeeb22ce23a725d4aec7035f3098f509ee4d4

class Parser:
	def  __init__(self, tokens):
		self.tokens = tokens;
		self.loop = 0;
		self.ifCounter = 0;
		self.offset = 0;
<<<<<<< HEAD
		self.error_counter = 0;
	
	def error(self, error_code):
		sys.stderr.write(sys.argv[1] + ":" + str(self.tokens[self.offset-1].line_no)+ ": Error: " + error_code + "\n");
		self.error_counter += 1;
=======
	
	def error(self, error_code):
		sys.stderr.write(sys.argv[1] + ":" + str(self.tokens[self.offset-1].line_no)+ ": " + error_code + "\n");
>>>>>>> 63feeeb22ce23a725d4aec7035f3098f509ee4d4
		exit(0);
	
	def accept(self, token_type):
		if (self.tokens[self.offset].token_type == token_type):
			self.offset += 1;
			return token_type;
			
	def expect(self, token_type):
		if(self.tokens[self.offset].token_type == token_type):
			self.offset += 1;
			return self.tokens[self.offset-1];
		else:
			self.error("Expected: %s, got: %s" % (token_type, self.tokens[self.offset].token_type));
	
	def parse_program(self):
		decls = [];
		while(self.tokens[self.offset].token_type != "EOF"):
			parse_decl = self.parse_decl();
			decls.append(parse_decl);
		
		return Program(decls);
	
	def parse_decl(self):
		if self.accept("KW_FUN"):
			return self.parse_decl_fn();
		
		else:
			return self.parse_decl_var();
	
	def parse_decl_fn(self):
		ret_type = self.parse_type();
		params = [];
		name = self.expect("IDENT");
		self.expect("OP_ROUND_OPEN");
		params = self.parse_params();
		self.expect("OP_CURLY_OPEN");
		body = self.parse_stmt_block();
		
		return Func_decl(ret_type, name, params, body);
		
	def parse_decl_var(self):
		var_type = self.parse_type();
		name = self.expect("IDENT");
		if(self.accept("OP_ASSIGN")):
			expr = self.parse_expr();
			self.expect("OP_SEMICOLON");
			return Global_var_decl(var_type, name, expr);
		else:
			self.expect("OP_SEMICOLON");
			return Global_var_decl(var_type, name, None);
		
	def parse_params(self):
		params = [];
		if(self.accept("OP_ROUND_CLOSE") is not None):
			return params;
		else:
			params.append(self.parse_param());
			while(self.accept("OP_COMMA") is not None):		
				params.append(self.parse_param());
			self.expect("OP_ROUND_CLOSE");
			return params;
		
	def parse_param(self):
		ret_type = self.parse_type();
		value = self.expect("IDENT");
		return Param_decl(value, ret_type);
	
	def parse_type(self):
		if(self.tokens[self.offset].token_type == "KW_INT"):
			token = self.expect("KW_INT");
			return Type_prim("int");
		elif(self.tokens[self.offset].token_type == "KW_FLOAT"):
			token =self.expect("KW_FLOAT");
			return Type_prim("float");
		elif(self.tokens[self.offset].token_type == "KW_STRING"):
			token = self.expect("KW_STRING");
			return Type_prim("string");
		elif(self.tokens[self.offset].token_type == "KW_CHAR"):
			token = self.expect("KW_CHAR");
			return Type_prim("char");
		elif(self.tokens[self.offset].token_type == "KW_VOID"):
			token = self.expect("KW_VOID");
			return Type_prim("void");
		elif(self.tokens[self.offset].token_type == "KW_BOOL"):
			token = self.expect("KW_BOOL");
			return Type_prim("bool");
		else:
			return None;
			
	#EXPR BEGIN
	
	def parse_expr(self):
		return self.parse_expr_or();

	def parse_expr_assign(self):
		result = self.expect("IDENT");
		result = Expr_var(result);
		while(1):
			if(self.accept("OP_ASSIGN")is not None):
				result = Stmt_assign(self.tokens[self.offset], "ASSIGN", result, self.parse_expr_or());
			else:
				break;
		
		return result;
		
	def parse_expr_or(self):
		result = self.parse_expr_and();
		
		while(self.accept("OP_OR")is not None):
			result = Expr_binary_logic(self.tokens[self.offset], "LOGICAL_OR", result, self.parse_expr_and());
		return result;
	
	def parse_expr_and(self):
		result = self.parse_expr_equal();
		
		while(self.accept("OP_AND")is not None):
			result = Expr_binary_logic(self.tokens[self.offset], "LOGICAL_AND", result, self.parse_expr_equal());
		return result;
		
	def parse_expr_equal(self):
		result = self.parse_expr_less();
		
		while(1):
			if(self.accept("OP_COMPARE")is not None):
				result = Expr_binary_equal(self.tokens[self.offset], "COMPARE", result, self.parse_expr_less());
			elif(self.accept("OP_NOT_ASSIGN")is not None):
				result = Expr_binary_equal(self.tokens[self.offset], "NOT_ASSIGN", result, self.parse_expr_less());
			else:
				break;
		return result;
		
	def parse_expr_less(self):
		result = self.parse_expr_more();
		
		while(1):
			if(self.accept("OP_L")is not None):
				result = Expr_binary_compr(self.tokens[self.offset], "OP_CMP_L", result, self.parse_expr_more());
			elif(self.accept("OP_LE")is not None):
				result = Expr_binary_compr(self.tokens[self.offset], "OP_CMP_LE", result, self.parse_expr_more());
			else:
				break;
		return result;
	
	def parse_expr_more(self):
		result = self.parse_expr_add();
		
		while(1):
			if(self.accept("OP_G")is not None):
				result = Expr_binary_compr(self.tokens[self.offset], "OP_CMP_G", result, self.parse_expr_add());
			elif(self.accept("OP_GE")is not None):
				result = Expr_binary_compr(self.tokens[self.offset], "OP_CMP_GE", result, self.parse_expr_add());
			else:
				break;
		return result;
	
	def parse_expr_add(self):
		result = self.parse_expr_mult();
		while(1):
			if(self.accept("OP_PLUS")is not None):
				result = Expr_binary_arith(self.tokens[self.offset], "ADD", result, self.parse_expr_mult());
			elif(self.accept("OP_MINUS")is not None):
				result = Expr_binary_arith(self.tokens[self.offset], "SUB", result, self.parse_expr_mult());
			else:
				break;		
		return result;
		
	def parse_expr_mult(self):
		result = self.parse_expr_unary();
		
		while(1):
			if(self.accept("OP_MUL")is not None):
				result = Expr_binary_arith(self.tokens[self.offset], "MUL", result, self.parse_expr_unary());
			elif(self.accept("OP_DIV")is not None):
				result = Expr_binary_arith(self.tokens[self.offset], "DIV", result, self.parse_expr_unary());
			elif(self.accept("OP_MOD")is not None):
				result = Expr_binary_arith(self.tokens[self.offset], "MOD", result, self.parse_expr_unary());
			else:
				break;
		return result;
		
	def parse_expr_unary(self):
		result = self.parse_expr_primary();
	
		if(self.accept("OP_INC")is not None):
			result = Expr_unary("INC", result);
		elif(self.accept("OP_DEC")is not None):
			result = Expr_unary("DEC", result);
		return result;
		
	def parse_expr_primary(self):
		if(self.tokens[self.offset].token_type == "IDENT"):
			return self.parse_expr_ident();
		elif(self.tokens[self.offset].token_type == "LIT_INT"):
			return self.parse_expr_lit_int();
		elif(self.tokens[self.offset].token_type == "LIT_BOOL"):
			return self.parse_expr_lit_bool();
		elif(self.tokens[self.offset].token_type == "LIT_FLOAT"):
			return self.parse_expr_lit_float();
<<<<<<< HEAD
		elif(self.tokens[self.offset].token_type == "LIT_STR"):
=======
		elif(self.tokens[self.offset].token_type == "LIT_STRING"):
>>>>>>> 63feeeb22ce23a725d4aec7035f3098f509ee4d4
			return self.parse_expr_lit_string();
		elif(self.tokens[self.offset].token_type == "LIT_CHAR"):
			return self.parse_expr_lit_char();
		elif(self.tokens[self.offset].token_type == "OP_ROUND_OPEN"):
			return self.parse_expr_paren();
<<<<<<< HEAD
		elif(self.tokens[self.offset].token_type == "STDIN"):
			return self.parse_expr_stdin();
=======
>>>>>>> 63feeeb22ce23a725d4aec7035f3098f509ee4d4
		else:
			return None;
	
	def parse_expr_ident(self):
		name = self.expect("IDENT");
		if(self.accept("OP_ROUND_OPEN") is not None):
			params = self.parse_call_fn();
			return Expr_fun_call(name, params);
		return Expr_var(name);
		
	def parse_expr_lit_int(self):
		lit = self.expect("LIT_INT");
		return Expr_lit(lit);
	
	def parse_expr_lit_bool(self):
		lit = self.expect("LIT_BOOL");
		return Expr_lit(lit);
		
	def parse_expr_lit_float(self):
		lit = self.expect("LIT_FLOAT");
		return Expr_lit(lit);
		
	def parse_expr_lit_string(self):
<<<<<<< HEAD
		lit = self.expect("LIT_STR");
=======
		lit = self.expect("LIT_STRING");
>>>>>>> 63feeeb22ce23a725d4aec7035f3098f509ee4d4
		return Expr_lit(lit);
		
	def parse_expr_lit_char(self):
		lit = self.expect("LIT_CHAR");
		return Expr_lit(lit);
<<<<<<< HEAD
	
	def parse_expr_stdin(self):
		lit = self.expect("STDIN");
		expr = self.parse_expr();
		return Expr_stdin(expr);
=======
>>>>>>> 63feeeb22ce23a725d4aec7035f3098f509ee4d4
		
	def parse_expr_paren(self):
		self.expect("OP_ROUND_OPEN");
		result = self.parse_expr();
		self.expect("OP_ROUND_CLOSE");
		return result;
		
	def parse_call_fn(self):
		args = self.parse_call_args();
		self.expect("OP_ROUND_CLOSE");
		return args;
		
	def parse_call_args(self):
		args = [];
		
		if(self.test_token("OP_ROUND_CLOSE")is not None):
			return args;
			
		args.append(self.parse_expr());
		while(self.accept("OP_COMMA")is not None):
			args.append(self.parse_expr());
		
		return args;	
	
	def test_token(self, token_type):
		if(self.tokens[self.offset].token_type == token_type):
			return token_type;
	
	#EXPR END
	
	def parse_stmt_block(self):
		stmts = [];
		while(1):
			if(self.accept("OP_CURLY_CLOSE")is not None):
				break;
			elif(self.accept("EOF")is not None):
				self.error("Statement block is not terminated. Missing '}'");
			else:
				stmts.append(self.parse_stmt());
				
		return Stmt_block(stmts);

	def parse_stmt(self):
		if (self.test_two_tokens("IDENT", "OP_ASSIGN")   
			or self.test_two_tokens("IDENT", "OP_PLUS_ASSIGN")  
			or self.test_two_tokens("IDENT", "OP_MINUS_ASSIGN") 
			or self.test_two_tokens("IDENT", "OP_MUL_ASSIGN")   
			or self.test_two_tokens("IDENT", "OP_DIV_ASSIGN")   
			or self.test_two_tokens("IDENT", "OP_MOD_ASSIGN")):
			expr = self.parse_expr_assign();
			self.expect("OP_SEMICOLON");
			return expr;
		elif(self.accept("KW_IF") is not None):
			return self.parse_stmt_if();
		elif(self.accept("KW_ELSE") is not None):
			self.error("Else without previous if");
		elif(self.accept("KW_RETURN") is not None):
			return self.parse_stmt_return();
		elif(self.accept("KW_CONTINUE") is not None):
			return self.parse_stmt_continue();
		elif(self.accept("KW_BREAK") is not None):
			return self.parse_stmt_break();
		elif(self.accept("KW_WHILE") is not None):
			return self.parse_stmt_while();
<<<<<<< HEAD
		elif(self.accept("STDOUT") is not None):
			return self.parse_stmt_stdout();
		elif(self.accept("STDIN") is not None):
			return self.parse_stmt_stdin();
=======
>>>>>>> 63feeeb22ce23a725d4aec7035f3098f509ee4d4
		else:
			token_type = self.parse_type();
			if(token_type is not None):
				name, value = self.parse_stmt_dec();
				return Stmt_dec_var(token_type, name, value);
			else:
				expr = self.parse_expr();
				self.expect("OP_SEMICOLON");
				return Stmt_expr(expr);
				
	
	def parse_stmt_dec(self):
		name = self.expect("IDENT");
		value = self.parse_dec_value();
		return name, value;
	
	def parse_dec_value(self):
		value = None;
		if (self.accept("OP_ASSIGN")):
			value = self.parse_expr();
		
		self.expect("OP_SEMICOLON");
		return value;
		
	def parse_stmt_if(self):
		self.expect("OP_ROUND_OPEN");
		cond = self.parse_expr();
		
		if(cond == None):
			self.error("Empty condition in statement");
		
		self.expect("OP_ROUND_CLOSE");
		self.expect("OP_CURLY_OPEN");
		body = self.parse_stmt_block()
		
		else_stmt = None;
		
		if(self.accept("KW_ELSE") is not None):
			if(self.accept("KW_IF") is not None):
				else_stmt = self.parse_stmt_if();
			else:
				self.expect("OP_CURLY_OPEN");
				else_stmt = self.parse_stmt_block();
		
		return Stmt_if(cond, body, else_stmt);
	
	def parse_stmt_continue(self):
		token = self.tokens[self.offset];
		self.expect("OP_SEMICOLON");
		
		return Stmt_continue(token);
	
	def parse_stmt_break(self):
		token = self.tokens[self.offset];
		self.expect("OP_SEMICOLON");
		
		return Stmt_break(token);
	
	def parse_stmt_while(self):
		self.expect("OP_ROUND_OPEN");
		cond = self.parse_expr();
		
		if(cond == None):
			self.error("Empty condition in statement");

		self.expect("OP_ROUND_CLOSE");
		self.expect("OP_CURLY_OPEN");
		body = self.parse_stmt_block();
		
		return Stmt_while(cond, body);
	
	def parse_stmt_stdout(self):
		stmt = self.parse_expr();
		self.expect("OP_SEMICOLON");
		
		return Stmt_stdout(stmt);
		
<<<<<<< HEAD
	def parse_stmt_stdin(self):
		stmt = self.parse_expr();
		self.expect("OP_SEMICOLON");
		
		return Stmt_stdin(stmt);
		
=======
>>>>>>> 63feeeb22ce23a725d4aec7035f3098f509ee4d4
	def parse_stmt_return(self):
		return_kw = self.tokens[self.offset];
		value = self.parse_expr();
		self.expect("OP_SEMICOLON");
		
		return Stmt_return(return_kw, value);
			
	def test_two_tokens(self, token_type_0, token_type_1):
		ok_0 = self.tokens[self.offset + 0].token_type == token_type_0;
		ok_1 = self.tokens[self.offset + 1].token_type == token_type_1;
		return ok_0 and ok_1;
