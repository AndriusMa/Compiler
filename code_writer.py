from instruction import *
from lexer import *
<<<<<<< HEAD
from ast import *
=======
>>>>>>> 63feeeb22ce23a725d4aec7035f3098f509ee4d4
import sys

class CodeWriter:
	def __init__(self):
		self.code = [];
<<<<<<< HEAD
		#self.labels = [];
=======
		self.labels = [];
>>>>>>> 63feeeb22ce23a725d4aec7035f3098f509ee4d4
		
	def complete_label(self, label, value):
		label.value = value;
		for offset in label.offsets:
			self.code[offset] = value;
			
	def dump_code(self):
		offset = 0;
		while (offset < len(self.code)):
			opcode = self.code[offset];
			instr = instrs_by_opcode[opcode];
			ops = self.code[offset + 1: offset + 1 + instr.num_ops];
<<<<<<< HEAD
			print("%2i: 0x%2x %-16s %s" % (offset, opcode, instr.name, ','.join(str(op) for op in ops)));
=======
			print("%2i: %02x %-16s %s" % (offset, opcode, instr.name, ','.join(str(op) for op in ops)));
>>>>>>> 63feeeb22ce23a725d4aec7035f3098f509ee4d4
			offset += 1 + instr.num_ops;
			
		print("RAW CODE: %s" % (self.code));
	
<<<<<<< HEAD
	#def new_label(self):
	#	label = Label();
	#	self.labels.append(label);
	#	return label;
=======
	def new_label(self):
		label = Label();
		self.labels.append(label);
		return label;
>>>>>>> 63feeeb22ce23a725d4aec7035f3098f509ee4d4
		
	def place_label(self, label):
		self.complete_label(label, len(self.code));
		
	def write(self, instr_name, *ops):
		instr = instrs_by_name[instr_name];
		if (len(ops) != instr.num_ops):
			sys.stderr.write("Invalid operand count\n");
		self.code.append(instr.opcode);
		for op in ops:
			if(op is None):
				continue;
			else:
				if (not isinstance(op, Label)):
					self.code.append(op);
				elif(op.value is None):
					op.offsets.append(len(self.code));
<<<<<<< HEAD
					self.code.append(666);
				else:
					self.code.append(op.value); # op
				
def gen_error(token, error_code):
	if (token is not None):
		sys.stderr.write(sys.argv[1] + ":" + str(token.line_no) + ":" + error_code + "\n");
		exit(-1);
=======
					self.code.append("NONE");
				else:
					self.code.append(op); # op_token_value
	
def gen_error(token, error_code):
	if (token is not None):
		sys.stderr.write(sys.argv[1] + ":" + str(token.line_no) + ":" + error_code + "\n");
>>>>>>> 63feeeb22ce23a725d4aec7035f3098f509ee4d4

class Label:
	def __init__(self, value = None):
		self.offsets = [];
		self.value = value;
