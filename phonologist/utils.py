import codecs

def force_unicode( input ):
	if type(input) == str:
		return input.decode('utf-8')
	else:
		return input


def load_file( IPA_txtfile ):
	f = codecs.open(IPA_txtfile,"r",encoding='utf-8')
	text = f.readline()
	tokens = text.split()
	f.close()
	return tokens