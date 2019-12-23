class Instruction:
	def __init__(self, opcode, name, num_ops):
		self.opcode = opcode;
		self.name = name;
		self.num_ops = num_ops;
		
instrs_by_name = {};
instrs_by_opcode = {};
<<<<<<< HEAD
name_by_opcode = {};
string_list = [];
index = 0;
=======
>>>>>>> 63feeeb22ce23a725d4aec7035f3098f509ee4d4

def add_instr(opcode, name, num_ops):
	instr = Instruction(opcode, name, num_ops);
	instrs_by_name[name] = instr;
	instrs_by_opcode[opcode] = instr;
<<<<<<< HEAD
	name_by_opcode[opcode] = name;
=======
>>>>>>> 63feeeb22ce23a725d4aec7035f3098f509ee4d4
	
# Arithmetic instructions
add_instr(0x10, "I_INT_ADD", 0);
add_instr(0x11, "I_INT_SUB", 0);
add_instr(0x12, "I_INT_MUL", 0);
add_instr(0x13, "I_INT_DIV", 0);
add_instr(0x14, "I_INT_MOD", 0);
add_instr(0x15, "I_FLOAT_ADD", 0);
add_instr(0x16, "I_FLOAT_SUB", 0);
add_instr(0x17, "I_FLOAT_MUL", 0);
add_instr(0x18, "I_FLOAT_DIV", 0);
add_instr(0x19, "I_FLOAT_MOD", 0);
add_instr(0x1A, "I_INC", 0);
add_instr(0x1B, "I_DEC", 0);

# Comparison instructions
<<<<<<< HEAD
add_instr(0x20, "I_LOGICAL_OR", 0);
add_instr(0x21, "I_LOGICAL_AND", 0);
add_instr(0x22, "I_INT_COMPARE", 0);
add_instr(0x23, "I_INT_NOT_ASSIGN", 0);
=======
add_instr(0x20, "I_OR", 0);
add_instr(0x21, "I_AND", 0);
add_instr(0x22, "I_COMPARE", 0);
add_instr(0x23, "I_NOT_ASSIGN", 0);
>>>>>>> 63feeeb22ce23a725d4aec7035f3098f509ee4d4
add_instr(0x24, "I_INT_OP_CMP_L", 0);
add_instr(0x25, "I_INT_OP_CMP_LE", 0);
add_instr(0x26, "I_INT_OP_CMP_G", 0);
add_instr(0x27, "I_INT_OP_CMP_GE", 0);
<<<<<<< HEAD
add_instr(0x28, "I_FLOAT_COMPARE", 0);
add_instr(0x29, "I_FLOAT_NOT_ASSIGN", 0);
add_instr(0x2A, "I_FLOAT_OP_CMP_L", 0);
add_instr(0x2B, "I_FLOAT_OP_CMP_LE", 0);
add_instr(0x2C, "I_FLOAT_OP_CMP_G", 0);
add_instr(0x2D, "I_FLOAT_OP_CMP_GE", 0);
=======
add_instr(0x28, "I_FLOAT_OP_CMP_L", 0);
add_instr(0x29, "I_FLOAT_OP_CMP_LE", 0);
add_instr(0x2A, "I_FLOAT_OP_CMP_G", 0);
add_instr(0x2B, "I_FLOAT_OP_CMP_GE", 0);
>>>>>>> 63feeeb22ce23a725d4aec7035f3098f509ee4d4

# Stack instructions
add_instr(0x30, "I_GET_L", 1);
add_instr(0x31, "I_SET_L", 1);
add_instr(0x32, "I_SET_G", 1);
add_instr(0x33, "I_GET_G", 1);
add_instr(0x34, "I_POP", 0);
add_instr(0x35, "I_INT_PUSH", 1);
add_instr(0x36, "I_FLOAT_PUSH", 1);
add_instr(0x37, "I_CHAR_PUSH", 1);
add_instr(0x38, "I_BOOL_PUSH", 1);
<<<<<<< HEAD
add_instr(0x39, "I_STR_PUSH", 1);
add_instr(0x3A, "I_ALLOC", 1);
=======
add_instr(0x39, "I_STRING_PUSH", 1);
>>>>>>> 63feeeb22ce23a725d4aec7035f3098f509ee4d4

# Control instructions
add_instr(0x40, "I_BR", 1);
add_instr(0x41, "I_BZ", 1);
add_instr(0x42, "I_CALL_BEGIN", 0);
add_instr(0x43, "I_CALL", 2);
add_instr(0x44, "I_RET", 0);
add_instr(0x45, "I_RET_V", 0);
<<<<<<< HEAD
add_instr(0x46, "I_EXIT", 0);
add_instr(0x47, "I_STDOUT", 0);
add_instr(0x48, "I_STDIN", 0);
=======
>>>>>>> 63feeeb22ce23a725d4aec7035f3098f509ee4d4
