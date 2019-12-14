from instruction import *
from lexer import *
import sys

class CodeWriter:
	def __init__(self):
		self.code = [];
		self.labels = [];
		
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
			print("%2i: %02x %-16s %s" % (offset, opcode, instr.name, ','.join(str(op) for op in ops)));
			offset += 1 + instr.num_ops;
			
		print("RAW CODE: %s" % (self.code));
	
	def new_label(self):
		label = Label();
		self.labels.append(label);
		return label;
		
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
					self.code.append("NONE");
				else:
					self.code.append(op); # op_token_value
	
def gen_error(token, error_code):
	if (token is not None):
		sys.stderr.write(sys.argv[1] + ":" + str(token.line_no) + ":" + error_code + "\n");

class Label:
	def __init__(self, value = None):
		self.offsets = [];
		self.value = value;
