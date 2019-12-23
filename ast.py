import copy
import sys
import lexer
from lexer import *
from check_types import *
from code_writer import *
from to_bytes import *

stack_slot_index = 0;
global_stack_slot_index = 0;

class Scope:
	def __init__(self, parent_scope):
		self.parent_scope = parent_scope;
		self.members = {}; #hashmap
		self.error_counter = 0;
	
	def error(self, message, line_no):
		sys.stderr.write(sys.argv[1] + ":" + str(line_no)+ ": Error: " + message + "\n");
		self.error_counter += 1;
		exit(0);
				
	def add(self, name_token, node):
		name = name_token.token_value;
		
		if (name in self.members):
			self.error("Duplicate variable %s" % (name), name_token.line_no);
		
		else:
			self.members[name] = node;
		
	def resolve_name(self, name_token): 
		name = name_token.token_value;
		if(name in self.members):
			node = self.members[name];
			return node;
		if(self.parent_scope is not None):
			return self.parent_scope.resolve_name(name_token);
		
		self.error("Undeclared variable %s" % (name), name_token.line_no);
			
class Node:
	def __init__(self):
		self.parent = None;

	def print_node(self, p):
	  sys.stderr.write("Error: print not implemented for: %s\n" % (self));
	  exit(0);	
	  		
	def resolve_names(self, scope):
		sys.stderr.write("Error: resolve_names not implemented for: %s\n" % (self));
		exit(0);
	
	def check_types(self):
		sys.stderr.write("Error: check_types method not implemented for %s\n" % (self));
		exit(0);
		
	def add_children(self, *children):
		for child in children:
			if(child is None):
				continue;
			child.parent = self;
	
	def find_ancestor(self, node_class):
		current_node = self.parent;
		while (current_node is not None):
			if(isinstance(current_node, node_class)):
				return current_node;
			else:
				current_node = current_node.parent;
	
	def gen_code(self, w):
		sys.stderr.write("Error: gen_code method not implemented for %s\n" % (self));
		exit(0);

class Program(Node):
	def __init__(self, element):
		super().__init__();
		self.add_children(*element);
		self.element = element;
		self.stack_slot = None;
		self.main_label = None;
	
	def print_node(self, p):
		p.display('program_elements', self.element);
	
	def resolve_names(self, scope):
		for fn in self.element:
			scope.add(fn.name, fn);	
			
		for fn in self.element:
			fn.resolve_names(scope);
	
		if (self.main_label is None):
			type_error(None, "Undefined reference to main");
			exit(-1);
	
	def check_types(self):
		for el in self.element:
			el.check_types();
			
	def gen_code(self, w):
		w.write('I_CALL_BEGIN');
		w.write('I_CALL', self.main_label, 0);
		w.write('I_EXIT');
		for d in self.element:
			d.gen_code(w);

class Param_decl(Node):
	def __init__(self, name, t_type):
		super().__init__();
		self.add_children(t_type);
		self.name = name;
		self.type = t_type;
		self.stack_slot = None;
	
	def print_node(self,p):
		p.display('name', self.name);
		p.display('type', self.type);
		
	def resolve_names(self, scope):
		global stack_slot_index;
		self.stack_slot = stack_slot_index;
		stack_slot_index += 1;
		
		scope.add(self.name, self);

class Decl(Node):
	pass

class Func_decl(Decl):
	def __init__(self, ret_type, name, args, body):
		super().__init__();
		self.add_children(*args, ret_type, body);
		self.ret_type = ret_type;
		self.name = name;
		self.args = args;
		self.body = body;
		self.start_label = Label();
		self.num_locals = None;
	
	def print_node(self,p):
		p.display('name', self.name);
		p.display('args', self.args);
		p.display('body', self.body);
		p.display('ret_type', self.ret_type);

	def resolve_names(self, parent_scope):
		if (self.check_main()):
			program = self.find_ancestor(Program);
			program.main_label = self.start_label;
		global stack_slot_index
		stack_slot_index = 0;
		scope = Scope(parent_scope);
		for param in self.args:
			if(not param.type.has_value()):
				type_error(self.name, "Function cannot have a parameter of type '" + param.type.kind + "'");
			else:
				param.resolve_names(scope);
		self.body.resolve_names(scope);
		self.num_locals = stack_slot_index;
	
	def check_main(self):
		valid_main = 0;
		if (self.name.token_value == 'main'):
			valid_main = 1;
			unify_types(Type_prim('int'), self.ret_type, self.name);
			if len(self.args) == 0:
				pass;
			else:
				type_error(self.name, "Wrong number of arguments in main. Instead of none " + str(len(self.args)) + " were given");
					
		return valid_main
		
	def check_types(self):
		self.body.check_types();
		
	def gen_code(self, w):
		w.place_label(self.start_label);
		
		if (self.num_locals > 0):
			w.write("I_ALLOC", self.num_locals)
		
		self.body.gen_code(w);
		w.write("I_RET");
	  
class Global_var_decl(Decl):
	def __init__(self, ret_type, name, value):
		super().__init__();
		self.ret_type = ret_type;
		self.name = name;
		self.value = value;
		self.target_node = None;
		self.start_label = Label();
		self.global_slot = 0;
  
	def print_node(self,p):
		p.display('type', self.ret_type);
		p.display('name', self.name);
		p.display('value', self.value);
  
	def resolve_names(self, scope):
		global global_stack_slot_index;
		self.global_slot = global_stack_slot_index;
		global_stack_slot_index += 1;
		#self.target_node = scope.resolve_name(self.name);
		
	def check_types(self):
		if(not self.ret_type.has_value()):
				type_error(self.name, "Function cannot have a parameter of type '" + param.type.kind + "'");
				
		elif (self.value):
			value_type = self.value.check_types();
			unify_types(self.ret_type, value_type, self.name);
			
	def gen_code(self, w):
		#w.place_label(self.start_label);
		if (self.value is not None):
			self.value.gen_code(w);
			w.write("I_SET_G", self.global_slot);

class Expr(Node):
	pass;

class Expr_fun_call(Expr):
	def __init__(self, name, args):
		super().__init__();
		self.add_children(*args);
		self.name = name;
		self.args = args;
		self.target_node = None;
  
	def print_node(self,p):
		p.display('name', self.name);
		p.display('args', self.args); 
  
	def resolve_names(self, scope):
		self.target_node = scope.resolve_name(self.name);
		for arg in self.args:
			arg.resolve_names(scope);
			
	def check_types(self):
		arg_types = [];
		for arg in self.args:
			arg_types.append(arg.check_types());
			
		if (self.target_node is None):
			return;
		
		elif (not isinstance(self.target_node, Func_decl)):
			type_error(self.target_node, "Call target is not a function");
			return;

		param_types = []
		
		for param in self.target_node.args:
			param_types.append(param.type)

		if (len(param_types) is not len(self.args)):
			type_error(self.target_node, "Invalid argument count")

		param_count = min(len(param_types), len(self.args))
		
		for elem in range(param_count):
			param_type = param_types[elem]
			arg_type = arg_types[elem]
			unify_types(param_type, arg_type, self.name)
		return self.target_node.ret_type
	
	def gen_code(self, w):
		w.write("I_CALL_BEGIN");
		for a in self.args:
			a.gen_code(w);
		w.write("I_CALL", self.target_node.start_label, len(self.args));

class Expr_binary(Expr):
	def __init__(self, token, op, left, right):
		super().__init__();
		self.add_children(left, right);
		self.token = token;
		self.op = op;
		self.left = left;
		self.right = right;
  
	def print_node(self,p):
		p.display('op', self.op);
		p.display('left', self.left);
		p.display('right', self.right);  
  
	def resolve_names(self, scope):
		if(self.left is not None):
			self.left.resolve_names(scope);
		if(self.right is not None):
			self.right.resolve_names(scope);
		
	def check_types(self):
		left_type = self.left.check_types();
		right_type = self.right.check_types();
		unify_types(left_type, right_type, self.token);
		
	def gen_code(self, w):
		self.left.gen_code(w);
		self.right.gen_code(w);
		_type = self.left.check_types(); # since gen_code runs after type check, it's enough to only check one side of expr
		type_instr = None;
		
		if(_type.is_arithmetic() or _type.is_comparable()):
			if (_type.kind is "int"):
				type_instr = "INT";
				w.write("I_" + type_instr + "_" + self.op);
			elif (_type.kind is "float"):
				type_instr = "FLOAT";
				w.write("I_" + type_instr + "_" + self.op);
			else:
				gen_error(self.token, "Couldn't generate binary expression");
				
class Expr_binary_arith(Expr_binary):
	def check_types(self):		
		if(None not in [self.left, self.right]):
			left_type = self.left.check_types();
			right_type = self.right.check_types();
			if (left_type.is_arithmetic() and right_type.is_arithmetic()):
				unify_types(left_type, right_type, self.token);
			else:
				type_error(self.token, "Cannot perform arithmetic operations with types '" + str(left_type.kind) + "' and '"  + str(right_type.kind) + "'");
			
			return left_type;
		
		elif(self.left is None):
			left_type = None;
			right_type = self.right.check_types();
			type_error(self.token, "Cannot perform arithmetic operations with types '" + str(left_type) + "' and '"  + str(right_type.kind) + "'");
				
		elif(self.right is None):
			left_type = self.left.check_types();
			right_type = None;
			type_error(self.token, "Cannot perform arithmetic operations with types '" + str(left_type.kind) + "' and '"  + str(right_type) + "'");
			
		else:
			type_error(self.token, "Cannot perform arithmetic operations with types '" + str(left_type) + "' and '"  + str(right_type) + "'");
		
		return None;

class Expr_binary_compr(Expr_binary):
	def check_types(self):
		if(None not in [self.left, self.right]):
			left_type = self.left.check_types();
			right_type = self.right.check_types();
			if (left_type.is_comparable() and right_type.is_comparable()):
				unify_types(left_type, right_type, self.token);
			else:
				type_error(self.token, "The values of types '" + str(left_type.kind) + "' and '"  + str(right_type.kind) + "' cannot be compared");
			return Type_prim('bool');
		
		elif(self.left is None):
			left_type = None;
			right_type = self.right.check_types();
			type_error(self.token, "The values of types '" + str(left_type) + "' and '"  + str(right_type.kind) + "' cannot be compared");
				
		elif(self.right is None):
			left_type = self.left.check_types();
			right_type = None;
			type_error(self.token, "The values of types '" + str(left_type.kind) + "' and '"  + str(right_type) + "' cannot be compared");
			
		else:
			type_error(self.token, "The values of types '" + str(left_type) + "' and '"  + str(right_type) + "' cannot be compared");
		
		return None;

class Expr_binary_equal(Expr_binary):
	def check_types(self):
		if(not None in [self.left, self.right]):
			left_type = self.left.check_types();
			right_type = self.right.check_types();
			if (left_type.has_value() and right_type.has_value()):
				unify_types(left_type, right_type, self.token);
			else:
				type_error(self.token, "Types '" + str(left_type.kind) + "' and '"  + str(right_type.kind) + "' have no value to compare");
			return Type_prim('bool');
		
		elif(self.left is None):
			left_type = None;
			right_type = self.right.check_types();
			type_error(self.token, "Types '" + str(left_type) + "' and '"  + str(right_type.kind) + "' have no value to compare");
				
		elif (self.right is None):
			left_type = self.left.check_types();
			right_type = None;
			type_error(self.token, "Types '" + str(left_type.kind) + "' and '"  + str(right_type) + "' have no value to compare");
			
		else:
			type_error(self.token, "Types '" + str(left_type.kind) + "' and '"  + str(right_type) + "' have no value to compare");
		
		return None;

class Expr_binary_logic(Expr_binary):
	def check_types(self):
		if (None not in [self.left, self.right]):
			left_type = self.left.check_types();
			right_type = self.left.check_types();
			unify_types(left_type, Type_prim('bool'), self.token);
			unify_types(right_type, Type_prim('bool'), self.token);
			return Type_prim('bool')
		else:
			type_error(self.token, "None type cannot be compared");
			
	def gen_code(self, w):
		self.left.gen_code(w);
		self.right.gen_code(w);
		w.write('I_'+self.op);
		

class Expr_unary(Expr):
	def __init__(self, op, expr):
		super().__init__();
		self.add_children(expr);
		self.op = op;
		self.expr = expr;
	
	def print_node(self,p):
		p.display('op', self.op);
		p.display('expr', self.expr);
		
	def resolve_names(self, scope):
		self.expr.resolve_names(scope);
		
	def check_types(self):
		return self.expr.check_types();
		
	def gen_code(self, w):
		self.expr.gen_code(w);
		
		if (self.op is "INC"):
			w.write("I_INC");
		elif (self.op is "DEC"):
			w.write("I_DEC");	
		else:
			gen_error(self.token, "Incorrect unary operation: " + str(self.op));
	
class Expr_stdin(Expr):
	def __init__(self, args):
		super().__init__();
		self.add_children(args);
		self.args = args;
		
	def print_node(self,p):
		p.display('args', self.args);
	
	def resolve_names(self, scope):
		self.args.resolve_names(scope);
			
	def check_types(self):
		self.args.check_types();
			
	def gen_code(self, w):
		self.args.gen_code(w);
		w.write("I_STDIN");


class Expr_lit(Expr):
	def __init__(self, lit):
		super().__init__();
		self.lit = lit;
		self.type = lit.token_type;
	
	def print_node(self,p):
		p.display('type', self.type);
	
	def resolve_names(self, scope):
		pass; #do nothing

	def check_types(self):
		if self.type is "LIT_INT":
			return Type_prim("int")
		elif self.type is "LIT_BOOL":
			return Type_prim("bool")
		elif self.type is "LIT_FLOAT":
			return Type_prim("float")
		elif self.type is "LIT_CHAR":
			return Type_prim("char")
		elif self.type is "LIT_STR":
			return Type_prim("string")
		else:
			type_error(self.lit, "Type '" + str(self.lit.value) + "'" + " is not implemented");
			
	def gen_code(self, w):
		if(self.type is "LIT_INT"):
			w.write("I_INT_PUSH", int(self.lit.token_value));
		elif(self.type is "LIT_CHAR"):
			w.write("I_CHAR_PUSH", ord(self.lit.token_value));			
		elif(self.type is "LIT_FLOAT"):
			w.write("I_FLOAT_PUSH", float_to_bytes((float(self.lit.token_value))));			
		elif(self.type is "LIT_BOOL"):
			w.write("I_BOOL_PUSH", 1 if self.lit.token_value == 'true' else 0);
		elif(self.type is "LIT_STR"):
			index = len(string_list);
			string_list.append(str(self.lit.token_value));
			w.write("I_STR_PUSH", index);
		else:
			gen_error(self.lit, "Incorrect literal type '" + str(self.lit.token_type) + "'");			
			

class Expr_var(Expr):
	def __init__(self, name):
		super().__init__();	
		self.name = name;
		self.target_node = None;
	
	def print_node(self,p):
		p.display('name', self.name);
	
	def resolve_names(self, scope):
		self.target_node = scope.resolve_name(self.name);
	
	def check_types(self):
		if (self.target_node is not None):
			if (isinstance(self.target_node, Func_decl)):
				type_error(self.name, "Function name cannot be passed as an argument");
				return self.target_node.ret_type;	
			else:
				return self.target_node.type;
		else:
			return None;
		
	def gen_code(self, w):
		if(hasattr(self.target_node, "stack_slot")):
			w.write("I_GET_L", self.target_node.stack_slot);
		elif(hasattr(self.target_node, "global_slot")):
			w.write("I_GET_G", self.target_node.global_slot);	

class Stmt(Node):
	pass;

class Stmt_block(Stmt):
	def __init__(self, stmts):
		super().__init__();
		self.add_children(*stmts);
		self.stmts = stmts;
  
	def print_node(self,p):
		p.display('stmts', self.stmts);

	def resolve_names(self, parent_scope):
		scope = Scope(parent_scope);	
		for stmt in self.stmts:
			stmt.resolve_names(scope);
			
	def check_types(self):
		for stmt in self.stmts:
			stmt.check_types();
			
	def gen_code(self, w):
		for s in self.stmts:
			s.gen_code(w);
  
class Stmt_dec_var(Stmt):
	def __init__(self, type_, name, value):
		super().__init__();
		self.add_children(type_, value);
		self.type = type_;
		self.name = name;
		self.value = value;
		self.stack_slot = None;
	
	def print_node(self,p):
		p.display('type', self.type);
		p.display('name', self.name);
		p.display('value', self.value);
	
	def resolve_names(self, scope):
		global stack_slot_index;
		self.stack_slot = stack_slot_index;
		stack_slot_index += 1;
		
		scope.add(self.name, self);
		self.type.resolve_names(scope);
		if (self.value is not None):
			self.value.resolve_names(scope);
			
	def check_types(self):
		if self.value:
			value_type = self.value.check_types();
			unify_types(self.type, value_type, self.name);
			
	def gen_code(self, w):
		if(self.value):
			self.value.gen_code(w);
			w.write("I_SET_L", self.stack_slot);

class Stmt_expr(Stmt):
	def __init__(self, expr):
		super().__init__();
		self.add_children(expr);
		self.expr = expr;
	
	def print_node(self,p):
		p.display('expr', self.expr);
		
	def resolve_names(self, scope):
		if(self.expr is not None):
			self.expr.resolve_names(scope);
			
	def check_types(self):
		if self.expr:
			self.expr.check_types();
			
	def gen_code(self, w):
		self.expr.gen_code(w);
		w.write("I_POP");

class Stmt_assign(Stmt):
	def __init__(self, token, op, target, value):
		super().__init__();
		self.add_children(value);
		self.token = token;
		self.op = op;
		self.target = target;
		self.value = value;
		self.target_node = None;
	
	def print_node(self,p):
		p.display('target', self.target);
		p.display('op', self.op);
		p.display('value', self.value);
	
	def resolve_names(self, scope):
		self.target_node = scope.resolve_name(self.target.name);
		self.value.resolve_names(scope);
		
	def check_types(self):
		#target_type = self.target.check_types();
		value_type = self.value.check_types();
		if (self.target_node):
			unify_types(self.target_node.type, value_type, self.token);
			return self.target_node.type;
		else:
			type_error(self.token, "Cannot perform arithmetic operations with type '" + str(target_type.kind) + "'");
		
	def gen_code(self, w):
		self.value.gen_code(w);
		if(hasattr(self.target_node, "stack_slot")):
				w.write("I_SET_L", self.target_node.stack_slot);
		elif(hasattr(self.target_node, "global_slot")):
			w.write("I_SET_G", self.target_node.global_slot);
		else:
			gen_error(self.token, "Incorrect assignment ");	

class Stmt_stdout(Stmt):
	def __init__(self, args):
		super().__init__();
		self.add_children(args);
		self.args = args;
		
	def print_node(self,p):
		p.display('args', self.args);
	
	def resolve_names(self, scope):
		self.args.resolve_names(scope);
			
	def check_types(self):
		self.args.check_types();
			
	def gen_code(self, w):
		self.args.gen_code(w);
		w.write("I_STDOUT");

class Stmt_if(Stmt):
	def __init__(self, cond, body, else_stmt):
		super().__init__();
		self.add_children(cond, body, else_stmt);
		self.condition = cond;
		self.body = body;
		self.else_stmt = else_stmt;
		self.end_l = None;

	def print_node(self,p):
		p.display('condition', self.condition);
		p.display('body', self.body);
		p.display('else_stmt', self.else_stmt);

	def resolve_names(self, scope):
		if(self.condition is not None):
			self.condition.resolve_names(scope);
		self.body.resolve_names(scope);
		if (self.else_stmt is not None):
			self.else_stmt.resolve_names(scope);
			
	def check_types(self):
		cond_type = self.condition.check_types();
		unify_types(Type_prim('bool'), cond_type, self.condition);
		self.body.check_types();
		if self.else_stmt:
			self.else_stmt.check_types();
			
	def gen_code(self, w):
		else_l = Label();
		end_l = Label();
		self.condition.gen_code(w);
		w.write("I_BZ", else_l);
		self.body.gen_code(w);
		w.write("I_BR", end_l);
		w.place_label(else_l);
		if (self.else_stmt):
			self.else_stmt.gen_code(w);
		w.place_label(end_l)
  
class Stmt_while(Stmt):
	def __init__(self, cond, body):
		super().__init__();
		self.add_children(cond, body);
		self.condition = cond;
		self.body = body;
		self.start_l = Label();
		self.end_l = Label();
	
	def print_node(self,p):
		p.display('condition', self.condition);
		p.display('body', self.body);
	  
	def resolve_names(self, scope):
		self.condition.resolve_names(scope);
		self.body.resolve_names(scope);
		
	def check_types(self):
		cond_type = self.condition.check_types();
		unify_types(Type_prim('bool'), cond_type, self.condition);
		self.body.check_types();
	
	def gen_code(self, w):
		w.place_label(self.start_l);
		self.condition.gen_code(w);
		w.write("I_BZ", self.end_l);
		self.body.gen_code(w);
		w.write("I_BR", self.start_l);
		w.place_label(self.end_l);

class Stmt_return(Stmt):
	def __init__(self, kw_return, value):
		super().__init__();
		self.add_children(value);
		self.kw_return = kw_return;
		self.value = value;
	
	def print_node(self, p):
		p.display('kw_return', self.kw_return);
		p.display('value', self.value);
	  
	def resolve_names(self, scope):
		if(self.value is not None):
			self.value.resolve_names(scope);
			
	def check_types(self):
		ret_type = self.find_ancestor(Func_decl).ret_type;
		value_type = Type_prim('void');
		if self.value:
			value_type = self.value.check_types();
		unify_types(ret_type, value_type, self.kw_return);
		
	def gen_code(self, w):
		if(self.value):
			self.value.gen_code(w);
			w.write("I_RET_V");
		else:
			w.write("I_RET");

class Stmt_continue(Stmt):
	def __init__(self, kw_continue):		
		super().__init__();
		self.kw_continue = kw_continue;
		self.target_node = None;
	
	def print_node(self,p):
		p.display('kw_continue', self.kw_continue);
	  
	def resolve_names(self, scope):
		curr_node = self.parent;
		while curr_node:
			if (isinstance(curr_node, Stmt_while)):
				self.target_node = curr_node;
				break;
			curr_node = curr_node.parent;
			
		if (self.target_node is None):
			sys.stderr.write(sys.argv[1] + ":" + str(self.kw_continue.line_no)+ ": Error: " + "Continue is not in a while statement" + "\n");
			exit(0);
			
	def check_types(self):
		pass;
		
	def gen_code(self, w):
		w.write("I_BR", self.target_node.start_l);
			
class Stmt_break(Stmt):
	def __init__(self, kw_break):
		super().__init__();
		self.kw_break = kw_break;
		self.target_node = None;

	def print_node(self,p):
		p.display('kw_break', self.kw_break);
	  
	def resolve_names(self, scope):
		curr_node = self.parent;
		while curr_node:
			if (isinstance(curr_node, Stmt_while)):
				self.target_node = curr_node;
				break;
			curr_node = curr_node.parent;
			
		if (self.target_node is None):
			sys.stderr.write(sys.argv[1] + ":" + str(self.kw_break.line_no)+ ": Error: " + "Break is not in a while statement" + "\n");
			exit(0);
			
	def check_types(self):
		pass;
		
	def gen_code(self, w):
		w.write("I_BR", self.target_node.end_l);

class Type(Node):
	def is_arithmetic(self):
		return false;

	def is_comparable(self):
		return false;

	def has_value(self):
		return false;

class Type_prim(Type):
	def __init__(self, kind):
		super().__init__();
		self.kind = kind;

	def print_node(self, p):
		p.display('kind', self.kind);

	def is_arithmetic(self):
		return self.kind == 'float' or self.kind == 'int';

	def is_comparable(self):
		return self.kind == 'float' or self.kind == 'int';

	def has_value(self):
		return self.kind != 'void';
		
	def resolve_names(self, scope):
		pass;
		
	def check_types(self):
		pass;

