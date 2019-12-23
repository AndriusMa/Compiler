from ast import *
import sys
<<<<<<< HEAD

def type_error(token, error_code):
	if (token is not None):
		sys.stderr.write(sys.argv[1] + ":" + str(token.line_no)+ ": Error: " + error_code + "\n");
		exit(-1);
	else:
		sys.stderr.write(sys.argv[1] + ": Error: " + error_code + "\n");
		exit(-1);
=======
#TODO error printing with line nums

def type_error(token, error_code):
	if (token is not None):
		sys.stderr.write(sys.argv[1] + ":" + str(token.line_no)+ ": " + error_code + "\n");
	else:
		sys.stderr.write(sys.argv[1] + ": " + error_code + "\n");
>>>>>>> 63feeeb22ce23a725d4aec7035f3098f509ee4d4

def unify_types(type_0, type_1, token = None):
	if not type_0 or not type_1:
		pass;
	elif type(type_0) is not type(type_1):
<<<<<<< HEAD
		type_error(token, "Expected %s, got %s" % (str(type(type_0)), str(type(type_1))));
		
	elif type(type_0) is type(type_1):
		if type_0.kind is not type_1.kind:
			type_error(token, "Expected %s, got %s" % (type_0.kind, type_1.kind));
=======
		type_error(token, "Expected %s, got %s" % (str(type(type_0)), str(type(type_1))))
		
	elif type(type_0) is type(type_1):
		if type_0.kind is not type_1.kind:
	  		type_error(token, "Expected %s, got %s" % (type_0.kind, type_1.kind))
>>>>>>> 63feeeb22ce23a725d4aec7035f3098f509ee4d4
