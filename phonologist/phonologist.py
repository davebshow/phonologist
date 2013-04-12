# -*- encoding: utf-8 -*-

import codecs
import re
from fmatrixutils import find_pos, find_neg
from constants import  (IPA_SYMBOLS, STRESS, VOWELS, CONSONANTS, PERIOD, COMMA, SYLLABLE, 
							FMATRIX, GLIDES, VOWELS_GLIDES, LIQUIDS, NASALS, NASALS_LIQUIDS,
							AFFRICATES, LARYNGEALS, NONCORONAL_OBSTRUENTS, PALATAL_OBSTRUENTS,
							CORONAL_OBSTRUENTS, DISTINCTIVE_FEATURES, FEATURE_GROUPS)


class Phonologist(object):
	"""
	Base class with magic methods for all other classes.
	"""
	
	@classmethod
	def loadfile( cls, ipa_textfile ):
		"""
		Load a textfile with IPA symbols
		"""
		f = codecs.open( ipa_textfile, "r", encoding='utf-8' )
		lines = f.readlines()
		words = []
		for line in lines:
			words += line.split()
		f.close()
		return cls(words)

	def __init__(self, tokens):
		self._tokens = tokens
		self.words = Words(InputManager(tokens).words())
		self.syllables = Syllables(InputManager(tokens).syllables())
		self.symbols = Symbols(InputManager(tokens).symbols())

	def _get_tokens(self):
		return self._tokens

	def _set_tokens(self, tokens):
		self._tokens = tokens
		self.phrases = Phrases(InputManager(tokens).words())
		self.words = Words(InputManager(tokens).words())
		self.syllables = Syllables(InputManager(tokens).syllables())
		self.symbols = Symbols(InputManager(tokens).symbols())

	tokens = property(_get_tokens, _set_tokens)

	def syllabify(self):
		"""
		Break a "Words" format object into syllables.
		--------------------
		return - list [ syll, ..., syll ]
		"""
		syllables = []
		for token in self._tokens:
			syllables.append(token.split("."))
		return sum(syllables,[]) # hehe good trick

	def __len__(self):
		return len(self._tokens)

	def __iter__(self):
		return TokenIterator(self._tokens)

	def __getitem__(self, ndx):
		assert ndx >= 0 and ndx < len(self._tokens), "index out of range"
		return self._tokens[ ndx ]

	def __setitem__(self, ndx, token):
		assert ndx >= 0 and ndx < len(self._tokens), "index out of range"
		self._tokens[ ndx ] = token

######################################################
class Token(Phonologist):

	def __init__(self, token):

		self._tokens = InputManager(token).token()
		self.syllables = InputManager(token).syllables()
		self.features = InputManager(token).symbols()

	def stressed(self):
		if STRESS in self._tokens:
			return True
		else:
			return False

	def pretonic_postonic(self, target):
		"""
		find values without changing token format
		"""
		pass

	def preceding_symbol(self, target):
		"""
		find values without changing token format
		"""
		pass

	def posterior_symbol(self, target):
		pass

	def syllabify(self):
		return self._tokens.split(".")

	def token_to_symbols(self):
		return Symbols(self)

	def syllable_position_in_token(self):
		pass

##########################################################
class BaseTokens(Phonologist):
	"""
	This is a base class for Words and Syllables (the "tokens" classes). 
	Words objects should be divided at word boundries.
	Syllables objects should be divided at syllable boundries.
	"""
	def __init__(self, tokens):
		self._tokens = InputManager(tokens).words()
		self.syllables = Syllables(InputManager(tokens).syllables())
		self.symbols = Symbols(InputManager(tokens).symbols())

	def _get_tokens(self):
		return self._tokens
		
	tokens = property(_get_tokens)		

	def count_token(self, target):
		"""
		Count the frequency of target token.
		----------------------
		target - word or syllable
		return - dict { token : frequency }
		"""
		target = InputManager( target ).force_unicode()
		token_dict = {target: 0}
		for token in self._tokens:
			if token == target:
				token_dict[ target ] += 1
		return token_dict

	def preceding_token(self, target):
		"""
		Count the frequency of tokens preceding target token.
		-----------------------
		target - word or syllable
		return - dict { target token : frequency }
		"""
		target = InputManager(target).force_unicode()
		token_dict = {}
		for ndx, token in enumerate(self._tokens[ 1: ]):
			if token == target:
				token_dict.setdefault( self._tokens[ ndx ], 0 )
				token_dict[ self._tokens[ ndx ] ] += 1
		return token_dict 

	def posterior_token( self, target ):
		"""
		Count the frequency of tokens posterior to target token.
		-----------------------
		target - word or syllable
		return - dict { posterior token : frequency }
		"""
		target = InputManager(target).force_unicode()
		token_dict = {}
		ndx = 0
		for i in range( len( self._tokens ) - 1 ):
			if self._tokens[ndx] == target:
				token_dict.setdefault( self._tokens[ ndx + 1], 0 )
				token_dict[ self._tokens[ndx + 1] ] += 1
			ndx += 1
		return token_dict

	def stressed_frequency( self ):
		"""
		Count the frequency of all tokens containing primary stress.
		---------------------
		return - dict { word with primary stress : frequency }
		"""
		stress_dict = {}
		for token in self._tokens:
			if STRESS in token:
				stress_dict.setdefault( token, 0 )
				stress_dict[ token ] += 1
		return stress_dict

	def unstressed_frequency( self ):
		"""
		Count the frequency of all tokens not containing primary stress.
		---------------------
		return - dict { word without primary stress : frequency }
		"""
		stress_dict = {}
		for token in self._tokens:
			if STRESS not in token and token not in [COMMA,PERIOD]:
				stress_dict.setdefault( token, 0 )
				stress_dict[ token ] += 1
		return stress_dict

	def token_by_symbol( self, target ):
		"""
		Count the frequency of all tokens containing a particular syllable.
		---------------------
		target - ipa symbol
		return - dict { token with symbol : frequency }
		"""
		target = InputManager( target ).force_unicode()
		token_dict = {}
		for token in self._tokens:
			if target in token:
				token_dict.setdefault( token, 0 )
				token_dict[ token ] += 1
		return token_dict
	
	def stressed_token_by_symbol( self, target ):
		"""
		Count the frequency of stressed tokens containing a particular symbol.
		---------------------
		target - ipa symbol
		return - dict { stressed token with symbol : frequency }
		"""
		target = InputManager( target ).force_unicode()
		tokens = self.token_by_symbol( target )
		token_dict = {}
		for token in tokens.keys():
			if STRESS in token:
				token_dict.setdefault(token,0)
				token_dict[ token ] += tokens[token]
		return token_dict

	def unstressed_token_by_symbol( self, target ):
		"""
		Count the frequency of unstressed tokens containing a particular symbol.
		---------------------
		target - ipa symbol
		return - dict { unstressed token with symbol : frequency }
		"""
		target = InputManager( target ).force_unicode()
		tokens = self.token_by_symbol( target )
		token_dict = {}
		for token in tokens.keys():
			if STRESS not in token:
				token_dict.setdefault(token,0)
				token_dict[ token ] += tokens[token]
		return token_dict

	def stressed( self, token ):
		if STRESS in token:
			return True
		else:
			return False

######################################################
class Phrases( BaseTokens ):
	"""
	May create Phrases class. 
	"""
	def _get_tokens(self):
		return self._tokens
		
	tokens = property(_get_tokens)

	def unstressed_syllable_sequence(self):
		"""
		Find sequences of unstressed syllables and 
		turn them into tokens for intersyllabic analysis.
		"""
		newtokens = []
		for token in self._tokens:
			syllables = token.split(".")
			newtoken = unicode()
			for syllable in syllables:
				if STRESS not in syllable:
					newtoken = newtoken + syllable + "."
				elif newtoken != u'':
					newtokens.append(newtoken)
					newtoken = unicode()
		return Phrases(newtokens)

	def pretonic_postonic_phrases(self):
		pass

##############################################################
class Words( BaseTokens ):
	"""
	Class for working with tokens divided at word boundries
	"""

	def _get_tokens(self):
		return self._tokens
		
	tokens = property(_get_tokens)

	def pretonic_postonic( self, target ):
		"""
		Currently just counts the occurence of a symbol in a pretonic
		or postonic position taking into account word boundries.
		----------------------
		target - ipa symbol 
		return dict { pretonic : frequency, postonic : frequency }
		"""
		target = InputManager(target).force_unicode()
		count_dict = { "pretonic":0, "postonic":0 }
		for token in self._tokens:
			if target in token:
				token_dict = self._pretonic_postonic_help( target, token )
				count_dict[ "pretonic" ] += token_dict[ "pretonic" ]
				count_dict[ "postonic" ] += token_dict[ "postonic" ]	
		return count_dict

	def _pretonic_postonic_help( self, target, token ):
		"""
		Counts pretonic postonic per token.
		"""
		count_dict = { "pretonic":0, "postonic":0 }
		stoken = token.split( "." )
		if len( stoken ) > 1:
			for ndx, syll in enumerate( stoken ):
				if target in syll and not self.stressed( syll ):
					if ndx > 0 and STRESS in stoken[ ndx-1 ]:
						count_dict[ "pretonic" ] += 1
					if ndx < len( stoken ) - 1 and STRESS in stoken[ ndx+1 ]:
						count_dict[ "postonic" ] += 1			
			return count_dict
		else:
			return count_dict
	
###################################################
class Syllables( BaseTokens ):
	"""
	Class for working with tokens divided at syllable boundries.
	"""
	def _get_tokens(self):
		return self._tokens
		
	tokens = property(_get_tokens)

	def __init__(self, tokens):
		self._tokens = InputManager(tokens).syllables()
		self.symbols = Symbols(InputManager(tokens).symbols())
		
	def pretonic_postonic_syllables(self):
		pass

	#### SYLLABLE NUCLEUS AND EVERYTHING HERE i.e. More Methods Coming

###############################################################
class Symbols( Phonologist ):
	"""
	Class for working with transcriptions at a symbol level.
	Does not take into account syllable or word boundries.
	May be merged with the Features class.
	"""
	### CLASS ATTRIBUTE ###
	# This is a list of groups that can be passed through various methods.
	# Need to change the format for clean passing... 
	groups = FEATURE_GROUPS
	features_dict = DISTINCTIVE_FEATURES
	def _get_tokens(self):
		return self._tokens
		
	tokens = property(_get_tokens)
	
	def __init__(self, tokens):
		self._tokens = InputManager(tokens).symbols()
		
	def count_symbol( self, target ):
		"""
		Count the frequency of a particular symbol.
		---------------------
		target - ipa symbol
		return - dict { symbol : frequency }
		"""
		pass

	def preceding_symbol( self, target  ):
		"""
		Count the frequency of symbols preceding the target.
		---------------------
		target - ipa symbol
		return - dict { symbol : frequency }
		"""
		target = InputManager(target).force_unicode()
		count_dict = {}
		for ndx,symbol in enumerate( self._tokens[ 1:] ):
			if symbol == target:
				if STRESS != self._tokens[ndx]: 
					count_dict.setdefault( self._tokens[ ndx ],0 )
					count_dict[self._tokens[ ndx ]] += 1
				elif ndx > 0:
					count_dict.setdefault( self._tokens[ ndx - 1 ],0 )
					count_dict[self._tokens[ ndx - 1 ]] += 1
		return count_dict

#####################################################################################
# THESE METHODS WILL PROBABLY BE REPLACED BY AN OPTIONAL VARIABLE IN preceding_symbol
# OR A METHOD proceeding_feature_groups
#####################################################################################
	def preceding_group(self, target, group):
		target = InputManager(target).force_unicode()
		count_dict = {}
		for ndx,symbol in enumerate( self._tokens[ 1:] ):
			if symbol == target:
				if STRESS != self._tokens[ndx]: 
					if self._tokens[ ndx ] in group:
						count_dict.setdefault( self._tokens[ ndx ],0 )
						count_dict[self._tokens[ ndx ]] += 1
				elif ndx > 0 and self._tokens[ ndx - 1 ] in group:
					count_dict.setdefault( self._tokens[ ndx - 1 ],0 )
					count_dict[self._tokens[ ndx - 1 ]] += 1
		return count_dict


##########################################################################
	def posterior_symbol( self, target ):
		"""
		Count the frequency of symbols preceding the target.
		---------------------
		target - ipa symbol
		return - dict { symbol : frequency }
		"""
		target = InputManager(target).force_unicode()
		count_dict = {}
		ndx = 0
		for i in range( len( self._tokens ) - 1):
			if self._tokens[ndx] == target:
				if STRESS != self._tokens[ndx+1]:
					count_dict.setdefault( self._tokens[ ndx + 1 ],0 )
					count_dict[self._tokens[ ndx + 1 ]] += 1
				else:
					count_dict.setdefault( self._tokens[ ndx + 2 ],0 )
					count_dict[self._tokens[ ndx + 2 ]] += 1						
			ndx += 1
		return count_dict	

#####################################################################################
# THESE METHODS WILL PROBABLY BE REPLACED BY AN OPTIONAL VARIABLE IN posterior_symbol
# OR A METHOD posterior_feature_groups
#####################################################################################
	def posterior_group( self, target, group ):
		target = InputManager(target).force_unicode()
		count_dict = {}
		ndx = 0
		for i in range( len( self._tokens ) - 1):
			if self._tokens[ndx] == target:
				if STRESS != self._tokens[ndx+1]:
					if self._tokens[ ndx + 1] in group:
						count_dict.setdefault( self._tokens[ ndx + 1 ],0 )
						count_dict[self._tokens[ ndx + 1 ]] += 1
				elif self._tokens[ndx + 2] in group:
					count_dict.setdefault( self._tokens[ ndx + 2 ],0 )
					count_dict[self._tokens[ ndx + 2 ]] += 1						
			ndx += 1
		return count_dict	

	def digram( self, target ):
		target = InputManager(target).force_unicode()
		count_dict = { target : 0 }
		for ndx in range(len(self._tokens)-1):
			if self._tokens[ndx] == target[ 0 ]:
				sym1 = self._tokens[ndx]
				if self._tokens[ ndx + 1 ] != STRESS:
					if self._tokens[ ndx + 1 ] == target[ 1 ]:
						count_dict[ target ] += 1
				else:
					if self._tokens[ ndx + 2 ] == traget[ 1 ]:
						count_dict[ target ] += 1
		return count_dict

	def features( self, plus=None, minus=None ):
		"""
		Find all symbols with a series of feature characteristics as 
		defined by plus and minus.
		--------------------------
		plus - a list of distinctive features with positive value
		minus - a list of distinctive features with negative value
		return set ([ sym, ..., sym ])
		"""
		if plus:
			if minus:
				data = self.find_plus( plus )
				return self.find_minus( minus, data_arg=data )
			else:
				return self.find_plus( plus )
		else:
			return self.find_minus( minus )

	def find_plus( self, plus, data_arg=None ):
		"""
		Find all symbols with a series of feature characteristics as 
		defined by plus.
		--------------------------
		plus - a list of distinctive features with positive value
		return set ([ sym, ..., sym ])
		"""
		assert type( plus ) == list, "plus must be passed as list [ ] "
		ndx = len( plus ) - 1
		if data_arg:
			data = list( data_args )
		else:
			data = self._tokens
		for feature in plus:
			n_data = find_pos( feature, data ) #from fmatrix_utils
			data = n_data
		output = set( data )
		return output

	def find_minus( self, minus, data_arg=None ):
		"""
		Find all symbols with a series of feature characteristics as 
		defined by minus.
		--------------------------
		minus - a list of distinctive features with positive value
		return set ([ sym, ..., sym ])
		"""
		assert type( minus ) == list, "minus must be passed as list [ ] "
		ndx = len( minus ) - 1
		if data_arg:
			data = list( data_arg )
		else:
			data = self._tokens
		for feature in minus:
			n_data = find_neg( feature, data ) #from fmatrix_utils
			data = n_data
		output = set( data )
		return output

	def feature_group( self, group ): #INVENTORY
		"""
		Count the frequency of all symbols in transcription 
		based on their distinctive feature grouping.
		---------------------
		group - a distinctive features group
		return - dict { symbol : frequency }
		"""
		symbol_dict = {}
		for symbol in self._tokens:
			if symbol in group:
				symbol_dict.setdefault( symbol, 0 )
				symbol_dict[ symbol ] += 1
		return symbol_dict

	def features_in_common( self, *targets ):
		"""
		Determine what features two or more have in
		common.
		"""
		pass 

class Vowels( Symbols ):
	"""
	Probably be part of features. Vowel featurmatrix etc.
	"""
	pass

#######################################################
class TokenIterator( object ):
	def __init__( self, phon_trans  ):
		self.current = 0
		self._token_ref = phon_trans

	def __iter__( self ):
		return self

	def next( self ):
		if self.current < len( self._token_ref ):
			token = self._token_ref[ self.current ]
			self.current += 1
			return token
		else:
			raise StopIteration

class InputManager( object ):
	"""
	Strange class. I don't know if this is out of the
	ordinary. I want to make sure user input comes in 
	the right format so I made a class to deal with it.
	"""

	def __init__(self, input, tokens=True):
		self.input = input

	def force_unicode(self):
		if type(self.input) == str:
			return self.input.decode('utf-8')
		else:
			return self.input

	def token(self):
		if type(self.input) == str:
			return self.input.decode('utf-8')
		if type(self.input) == unicode:
			return self.input
		else:
			raise TypeError, "Token must be str or unicode"

	def words( self ):
		if type(self.input) == list:
			return self.input
		elif type(self.input) == unicode:
			return self.input.split()
		elif type(self.input) == str:
			uinput = self.input.decode('utf-8')
			return uinput.split()
		else:
			raise TypeError

	def syllables( self ):
		if type(self.input) == Words or type(self.input) == Phonologist \
				or type(self.input) == Token or type(self.input) == Phrases: 
			return self.input.syllabify()
		elif type(self.input) == list:
			syllables = []
			for token in self.input:
				syllables.append(token.split("."))
			return sum(syllables,[])
		elif type(self.input) == unicode:
			return self.input.split(".")
		elif type(self.input) == str:
			uinput = self.input.decode('utf-8')
			return uinput.split(".")
		else:
			raise TypeError

	def symbols( self ):
		if type(self.input) == Words or type(self.input) == Phrases \
				or type(self.input) == Token:
			output = ''.join(self.input)
			return re.sub('[\s.]','',output)
		elif type(self.input) == Syllables:
			return ''.join( self.input.tokens )
		elif type(self.input) == unicode:
			output = re.sub('[\s.]','', self.input)
			return output
		if type(self.input) == str:
			output = re.sub('[\s.]','', self.input)
			return output.decode('utf-8')
		elif type(self.input) == list:
			return ''.join(self.input)
		else:
			raise TypeError




	




