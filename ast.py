import copy
import sys
from lexer import *
from check_types import *
from code_writer import *

stack_slot_index = 0;

class Scope:
	def __init__(self, parent_scope):
		self.parent_scope = parent_scope;
		self.members = {}; #hashmap
	
	def error(self, message, line_no):
		sys.stderr.write("SCOPE ERROR: " + message + " on line " + str(line_no) + " in file " + sys.argv[1] + '\n');
				
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
	  sys.stderr.write("print not implemented for: %s\n" % (self));	
	  		
	def resolve_names(self, scope):
		sys.stderr.write("resolve_names not implemented for: %s\n" % (self));
	
	def check_types(self):
		sys.stderr.write("check_types method not implemented for %s\n" % (self));
		
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
		sys.stderr.write("gen_code method not implemented for %s\n" % (self));

class Program(Node):
	def __init__(self, element):
		super().__init__();
		self.add_children(*element);
		self.element = element;
		self.stack_slot = None;
	
	def print_node(self, p):
		p.display('program_elements', self.element);
	
	def resolve_names(self, scope):
		for fn in self.element:
			scope.add(fn.name, fn);	
		
		self.check_main();
			
		for fn in self.element:
			fn.resolve_names(scope);
			
	def check_main(self):
		valid_main = 0;
		line_no = 0;
		for prog_elem in self.element:
			if (isinstance(prog_elem, Func_decl)) and prog_elem.name.token_value == 'main':
				line_no = prog_elem.name.line_no;
				valid_main = 1;
				unify_types(Type_prim('int'), prog_elem.ret_type, prog_elem.name);
				if len(prog_elem.args) == 0:
					break;
				elif len(prog_elem.args) == 1:
					unify_types(Type_prim('int'), prog_elem.args[0].type, prog_elem.name);
					break;
				else:
					type_error(prog_elem.name, "Wrong number of arguments in main. Instead of one or none " + str(len(prog_elem.args)) + " were given");
				return prog_elem;
				
		if(valid_main == 0):	
			type_error(None, "Undefined reference to main");
			return None;
	
	def check_types(self):
		for el in self.element:
			el.check_types();
			
	def gen_code(self, w):
		for d in self.element:
			d.gen_code(w);

class Param_decl(Node):
	def __init__(self, name, t_type):
		super().__init__();
		self.add_children(t_type);
		self.name = name;
		self.type = t_type;
	
	def print_node(self,p):
		p.display('name', self.name);
		p.display('type', self.type);
		
	def resolve_names(scope):
		scope.add(self.name, self);
		global stack_slot_index;
		self.stack_slot = stack_slot_index;
		stack_slot_index += 1;

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
	
	def print_node(self,p):
		p.display('name', self.name);
		p.display('args', self.args);
		p.display('body', self.body);
		p.display('ret_type', self.ret_type);

	def resolve_names(self, parent_scope):
		stack_slot_index = 0;
		scope = Scope(parent_scope);
		scope.members = copy.deepcopy(parent_scope.members); # copy all members
		for param in self.args:
			if(not param.type.has_value()):
				type_error(self.name, "Function cannot have a parameter of type " + param.type.kind);
			scope.add(param.name, param);
		self.body.resolve_names(scope);
		
	def check_types(self):
		self.body.check_types();
		
	def gen_code(self, w):
		w.place_label(self.start_label);
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
		self.target_node = scope.resolve_name(self.name);
		
	def check_types(self):
		if(not self.ret_type.has_value()):
				type_error(self.name, "Function cannot have a parameter of type " + param.type.kind);
				
		elif (self.value):
			value_type = self.value.check_types();
			unify_types(self.ret_type, value_type, self.name);
			
	def gen_code(self, w):
		w.place_label(self.start_label);
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
		self.target = None;
  
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
			type_error(self.target, "Call target is not a function");
			return;

		param_types = []
		
		for param in self.target_node.args:
			param_types.append(param.type)

		if (len(param_types) is not len(self.args)):
			type_error(self.target, "Invalid argument count")

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
				type_error(self.token, "Cannot perform arithmetic operations with types " + str(left_type.kind) + " and "  + str(right_type.kind));
			
			return left_type;
		
		elif(self.left is None):
			left_type = None;
			right_type = self.right.check_types();
			type_error(self.token, "Cannot perform arithmetic operations with types " + str(left_type) + " and "  + str(right_type.kind));
				
		elif(self.right is None):
			left_type = self.left.check_types();
			right_type = None;
			type_error(self.token, "Cannot perform arithmetic operations with types " + str(left_type.kind) + " and "  + str(right_type));
			
		else:
			type_error(self.token, "Cannot perform arithmetic operations with types " + str(left_type) + " and "  + str(right_type));
		
		return None;

class Expr_binary_compr(Expr_binary):
	def check_types(self):
		if(None not in [self.left, self.right]):
			left_type = self.left.check_types();
			right_type = self.right.check_types();
			if (left_type.is_comparable() and right_type.is_comparable()):
				unify_types(left_type, right_type, self.token);
			else:
				type_error(self.token, "The values of types cannot be compared " + str(left_type.kind) + " and "  + str(right_type.kind));
			return Type_prim('bool');
		
		elif(self.left is None):
			left_type = None;
			right_type = self.right.check_types();
			type_error(self.token, "The values of types cannot be compared " + str(left_type) + " and "  + str(right_type.kind));
				
		elif(self.right is None):
			left_type = self.left.check_types();
			right_type = None;
			type_error(self.token, "The values of types cannot be compared " + str(left_type.kind) + " and "  + str(right_type));
			
		else:
			type_error(self.token, "The values of types cannot be compared " + str(left_type) + " and "  + str(right_type));
		
		return None;

class Expr_binary_equal(Expr_binary):
	def check_types(self):
		if(None not in [self.left, self.right]):
			left_type = self.left.check_types();
			right_type = self.right.check_types();
			if (left_type.has_value() and right_type.has_value()):
				unify_types(left_type, right_type, self.token);
			else:
				type_error(self.token, "Types " + str(left_type.kind) + " and "  + str(right_type.kind) + " have no value to compare");
			return Type_prim('bool');
		
		elif(self.left is None):
			left_type = None;
			right_type = self.right.check_types();
			type_error(self.token, "Types " + str(left_type) + " and "  + str(right_type.kind) + " have no value to compare");
				
		elif (self.right is None):
			left_type = self.left.check_types();
			right_type = None;
			type_error(self.token, "Types " + str(left_type.kind) + " and "  + str(right_type) + " have no value to compare");
			
		else:
			type_error(self.token, "Types " + str(left_type.kind) + " and "  + str(right_type) + " have no value to compare");
		
		return None;

class Expr_binary_logic(Expr_binary):
	def check_types(self):
		if (None not in [self.left, self.right]):
			left_type = self.left.check_types();
			right_type = self.left.check_types();
			unify_types(left_type, TYPE_BOOL, self.token);
			unify_types(right_type, TYPE_BOOL, self.token);
			return Type_prim('bool')
		else:
			type_error(self.token, "None type cannot be compared");
		

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
		elif self.type is "LIT_STRING":
			return Type_prim("string")
		else:
			type_error(self.lit, "Type ' " + str(self.lit.value) + "'" + "is not implemented");
			
	def gen_code(self, w):
		if(self.type is "LIT_INT"):
			w.write("I_INT_PUSH", self.lit.token_value);
		elif(self.type is "LIT_CHAR"):
			w.write("I_CHAR_PUSH", ord(self.lit.token_value));			
		elif(self.type is "LIT_FLOAT"):
			w.write("I_FLOAT_PUSH", int(float(self.lit.token_value)));			
		elif(self.type is "LIT_BOOL"):
			w.write("I_BOOL_PUSH", 1 if self.lit.token_value == 'true' else 0);
		elif(self.type is "LIT_STRING"):
			w.write("I_STRING_PUSH", self.lit);
		else:
			gen_error(self.lit, "Incorrect literal type " + str(self.lit.token_type));			
			

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
		else:
			w.write("I_GET_G");	

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
		target_type = self.target.check_types();
		value_type = self.value.check_types();
		if target_type:
			if target_type.has_value():
				unify_types(target_type, value_type, self.token);
			else:
				type_error(self.token, "Cannot perform arithmetic operations with this type: " + str(target_type.kind));
		return target_type;
		
	def gen_code(self, w):
		if(hasattr(self.target_node, "stack_slot")):
				w.write("I_SET_L", self.target_node.stack_slot);
		else:
			gen_error(self.token, "Incorrect assignment ");	

class Stmt_if(Stmt):
	def __init__(self, cond, body, else_stmt):
		super().__init__();
		self.add_children(cond, body);
		self.condition = cond;
		self.body = body;
		self.else_stmt = else_stmt;

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
		end_l = w.new_label();
		self.condition.gen_code(w);
		w.write("I_BZ", end_l);
		self.body.gen_code(w);
		w.place_label(end_l);
  
class Stmt_while(Stmt):
	def __init__(self, cond, body):
		super().__init__();
		self.add_children(cond, body);
		self.condition = cond;
		self.body = body;
	
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
		start_l = w.new_label();
		w.place_label(start_l)
		end_l = w.new_label();
		self.condition.gen_code(w);
		w.write("I_BZ", end_l);
		self.body.gen_code(w);
		w.write("I_BR", start_l);
		w.place_label(end_l);

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
		unify_types(ret_type, value_type, self.value);
		
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
			sys.stderr.write("Continue is not in a while statement on line: %i\n" % (self.kw_continue.line_no));
			exit(0);
			
	def check_types(self):
		pass;
			
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
			sys.stderr.write("Break is not in a while statement on line: %i\n" % (self.kw_break.line_no));
			exit(0);
			
	def check_types(self):
		pass;
		
	def gen_code(self, w):
		w.write("I_BR", "LOOP_END");

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

