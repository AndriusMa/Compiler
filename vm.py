from instruction import *
from to_bytes import *
import sys

STACK_LOC = 1024

class VM:
	def __init__(self, code):
		self.memory = [0] * 4096
		self.memory[0: len(code)] = code
		self.running = True
		self.ip = 0
		self.fp = STACK_LOC
		self.sp = STACK_LOC

	def exec(self):
		while self.running:
			self.exec_one()
		result = self.pop()
		print('result: %s' % result)

	def exec_call(self, target, num_args):
		new_ip = target
		new_fp = self.sp - num_args
		new_sp = new_fp
		self.memory[new_fp - 3] = self.ip
		self.memory[new_fp - 2] = self.fp
		self.memory[new_fp - 1] = new_fp - 3
		self.ip = new_ip
		self.fp = new_fp
		self.sp = new_sp

	def exec_ret(self, value):
		old_ip = self.memory[self.fp - 3]
		old_fp = self.memory[self.fp - 2]
		old_sp = self.memory[self.fp - 1]
		self.ip = old_ip
		self.fp = old_fp
		self.sp = old_sp
		self.push(value)

	def pop(self):
		self.sp -= 1
		return self.memory[self.sp]

	def push(self, value):
		self.memory[self.sp] = value
		self.sp += 1

	def read_imm(self):
		value = self.memory[self.ip]
		self.ip += 1
		return value

	def exec_one(self):
		opcode = self.read_imm()
		instr_name = name_by_opcode[opcode]
		
		if instr_name in ('I_INT_ADD', 'I_FLOAT_ADD'):
			b = self.pop()
			a = self.pop()
			self.push(a + b)
		elif instr_name in ('I_INT_SUB', 'I_FLOAT_SUB'):
			b = self.pop()
			a = self.pop()
			self.push(a - b)
		elif instr_name in ('I_INT_MUL', 'I_FLOAT_MUL'):
			b = self.pop()
			a = self.pop()
			self.push(a * b)
		elif instr_name in ('I_INT_DIV', 'I_FLOAT_DIV'):
			b = self.pop()
			a = self.pop()
			self.push(a / b)
		elif instr_name in ('I_INT_MOD', 'I_FLOAT_MOD'):
			b = self.pop()
			a = self.pop()
			self.push(a % b)
		elif instr_name in ('I_INT_OP_CMP_L', 'I_FLOAT_OP_CMP_L'):
			b = self.pop()
			a = self.pop()
			if(a or b is str):
				self.push(1 if int(a) < int(b) else 0)
			else:
				self.push(1 if a < b else 0)
		elif instr_name in ('I_INT_OP_CMP_G', 'I_FLOAT_OP_CMP_G'):
			b = self.pop()
			a = self.pop()
			if(a or b is str):
				self.push(1 if int(a) > int(b) else 0)
			else:
				self.push(1 if a > b else 0)
		elif instr_name in ('I_INT_OP_CMP_LE', 'I_FLOAT_OP_CMP_LE'):
			b = self.pop()
			a = self.pop()
			if(a or b is str):
				self.push(1 if int(a) <= int(b) else 0)
			else:
				self.push(1 if a <= b else 0)
		elif instr_name in ('I_INT_OP_CMP_GE', 'I_FLOAT_OP_CMP_GE'):
			b = self.pop()
			a = self.pop()
			if(a or b is str):
				self.push(1 if int(a) >= int(b) else 0)
			else:
				self.push(1 if a >= b else 0)
		elif instr_name in ('I_INT_COMPARE', 'I_FLOAT_COMPARE'):
			b = self.pop()
			a = self.pop()
			if(a or b is str):
				self.push(1 if int(a) == int(b) else 0)
			else:
				self.push(1 if a == b else 0)
		elif instr_name in ('I_INT_NOT_ASSIGN', 'I_FLOAT_NOT_ASSIGN'):
			b = self.pop()
			a = self.pop()
			if(a or b is str):
				self.push(1 if int(a) != int(b) else 0)
			else:
				self.push(1 if a != b else 0)
		elif instr_name in ('I_LOGICAL_AND'):
			b = self.pop()
			a = self.pop()
			self.push(1 if a and b else 0)
		elif instr_name in ('I_LOGICAL_OR'):
			b = self.pop()
			a = self.pop()
			self.push(1 if a or b else 0)
		elif instr_name == 'I_GET_L':
			i = self.read_imm()
			self.push(self.memory[self.fp + i])
		elif instr_name == 'I_SET_L':
			i = self.read_imm()
			self.memory[self.fp + i] = self.pop()
		elif instr_name == 'I_POP':
			self.sp -= 1
		elif instr_name == 'I_INT_PUSH':
			self.push(self.read_imm())
		elif instr_name == 'I_FLOAT_PUSH':
			self.push(float_from_bytes(self.read_imm()))
		elif instr_name == 'I_CHAR_PUSH':
			self.push(chr(self.read_imm()))
		elif instr_name == 'I_BOOL_PUSH':
			self.push('true' if self.read_imm() == 1 else 'false')
		elif instr_name == 'I_STR_PUSH':
			index = self.read_imm()
			self.push(string_list[index])
		elif instr_name == 'I_ALLOC':
			self.sp += self.read_imm()
		elif instr_name == 'I_BR':
			i = self.read_imm()
			self.ip = i
		elif instr_name == 'I_BZ':
			i = self.read_imm()
			if self.pop() == 0:
				self.ip = i
		elif instr_name == 'I_RET':
			self.exec_ret(0)
		elif instr_name == 'I_RET_V':
			self.exec_ret(self.pop())
		elif instr_name == 'I_CALL_BEGIN':
			self.push(0)
			self.push(0)
			self.push(0)
		elif instr_name == 'I_CALL':
			self.exec_call(self.read_imm(), self.read_imm())
		elif instr_name == 'I_EXIT':
			self.running = 0
		elif instr_name == 'I_STDOUT':
			print(self.pop());
		elif instr_name == 'I_STDIN':
			inp = input()
			self.push(inp)
		else:
			sys.stderr.write("Invalid instruction opcode 0x%2x \n Couldn't start VM" % opcode)
			exit(-1);
