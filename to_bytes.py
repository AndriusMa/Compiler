import struct;
		
def int_to_bytes(value: int, size = 4, order = 'big'):
	return list(value.to_bytes(size, order, signed = True));
	
def float_to_bytes(value: float):
	return list(struct.pack('<d', value));
	
def float_from_bytes(code):
	float_bytes = bytes(code[0: 8]);
	value = struct.unpack('<d', float_bytes);
	return value[0];
		
#def str_to_bytes(value: str):
#	bytes_ = int_to_bytes(len(value));
#	bytes_.extend(bytes(value, 'UTF-8'));
#	return bytes_;
	
#def str_from_bytes(code):
#	str_size = len(code);
#	string = str(bytes(code[4: str_size]), 'UTF-8');
#	return string;
	
