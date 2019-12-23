from ast import *
import sys

def type_error(token, error_code):
	if (token is not None):
		sys.stderr.write(sys.argv[1] + ":" + str(token.line_no)+ ": Error: " + error_code + "\n");
		exit(-1);
	else:
		sys.stderr.write(sys.argv[1] + ": Error: " + error_code + "\n");
		exit(-1);

def unify_types(type_0, type_1, token = None):
	if not type_0 or not type_1:
		pass;
	elif type(type_0) is not type(type_1):
		type_error(token, "Expected %s, got %s" % (str(type(type_0)), str(type(type_1))));
		
	elif type(type_0) is type(type_1):
		if type_0.kind is not type_1.kind:
			type_error(token, "Expected %s, got %s" % (type_0.kind, type_1.kind));
