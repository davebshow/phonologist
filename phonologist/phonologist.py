# -*- encoding: utf-8 -*-

import codecs
from fmatrixutils import *
from constants import  ( IPA_SYMBOLS, STRESS, COMMA, PERIOD, SYLLABLE )

#### Object oriented library for working with IPA transcriptions. ####

#### Class to create the Phonetic Transcription Object. ####
class Phonologist( object ):

#### Create object. ####
	def __init__( self, IPA_txtfile ):
		self.tokens = self.load_file( IPA_txtfile )

	def load_file( self, IPA_txtfile ):
		f = codecs.open(IPA_txtfile,"r",encoding='utf-8')
		text = f.readline()
		tokens = text.split()
		f.close()
		return tokens

	#### Basic methods. ####
	def __len__( self ):
		return len(self.tokens)

	def __iter__( self ):
		return TokenIterator( self.tokens )

	def __getitem__( self, ndx ):
		assert ndx >= 0 and ndx < len( self.tokens ), "index out of range"
		return self.tokens[ ndx ]

	def __setitem__( self, ndx, token ):
		assert ndx >= 0 and ndx < len( self.tokens ), "index out of range"
		self.tokens[ ndx ] = token

#################################################################
# Symbol level methods
#################################################################

	# Count the incidence of any number of taret symbols passed as arguments.
	# Returns a dictionary with { targets as keys : incidence as value}

	def target_symbols( self, *ipa_symbols):
		count_dict = {}
		data = ''.join(self.tokens)
		for symbol in data:
			if symbol.encode('utf-8') in ipa_symbols:
				count_dict.setdefault(symbol,0)
				count_dict[symbol] += 1
		return count_dict

	def preceding_symbol( self, *targets  ):
		count_dict = {}
		data = ''.join( self.tokens )
		for ndx,symbol in enumerate( data[ 1:] ):
			if symbol.encode('utf-8') in targets:
				count_dict.setdefault( data[ ndx ],0 )
				count_dict[data[ ndx ]] += 1
		return count_dict

	def posterior_symbol( self, *targets ):
		count_dict = {}
		data = ''.join( self.tokens )
		ndx = 0
		for i in range( len( data ) - 1):
			if data[ndx].encode( 'utf-8' ) in targets:
				count_dict.setdefault( data[ ndx + 1 ],0 )
				count_dict[data[ ndx + 1 ]] += 1
			ndx += 1
		return count_dict	

#########################################################################
# Token level methods #
#########################################################################

	# Count the incidence of any number of the target tokens passed as arguments.
	# Returns a dictionary with { targets as keys : incidence as value}
	def target_tokens( self, *target_tokens ):
		count_dict = {}
		for token in self.tokens:
			if token.encode('utf-8') in target_tokens:
				count_dict.setdefault( token, 0 )
				count_dict[token] += 1
		return count_dict

	def preceding_tokens( self, *targets ):
		count_dict = {}
		for ndx, token in enumerate(self.tokens[ 1: ]):
			if token.encode( 'utf-8' ) in targets:
				print token 
				count_dict.setdefault( self.tokens[ ndx ], 0 )
				count_dict[ self.tokens[ ndx ] ] += 1
		return count_dict 

	def posterior_token( self, *targets ):
		count_dict = {}
		ndx = 0
		for i in range( len( self.tokens ) - 1 ):
			if self.tokens[ndx].encode( 'utf-8' ) in targets:
				count_dict.setdefault( self.tokens[ ndx + 1], 0 )
				count_dict[ self.tokens[ndx + 1] ] += 1
			ndx += 1
		return count_dict

	def stressed_frequency( self ):
		stress_dict = {}
		for token in self.tokens:
			for char in token:
				if char == STRESS:
					stress_dict.setdefault( token, 0 )
					stress_dict[ token ] += 1
		return stress_dict

	def unstressed_frequency( self ):
		stress_dict = {}
		for token in self.tokens:
			if STRESS not in token:
				stress_dict.setdefault( token, 0 )
				stress_dict[ token ] += 1
		return stress_dict

	# Count stress in a token
	def stressed_per_token(self):
		return 

	def unstressed_per_token(self):
		return 

	#### Methods for working with the Phrases and Words classes###
	#### Divide the tokens based on syllable boundries ####

	def syllabify( self ):
		syllables = []
		for token in self.tokens:
			syllables.append(token.split("."))
		self.tokens = sum(syllables,[]) # hehe good trick

##############################################################
##############################################################
###FEATURE THEORY#############################################

	def features(self, posfeatures=None, negfeatures=None ):
		return posfeatures,negfeatures
	def vowels( self ):
		return 
	def glides( self ):
		return 
	def nasals( self ):
		return 
	def liquids( self ):
		return 
	def affricates( self ):
		return 
	def laryngeals( self ):
		return 
	def noncoronal_obstruents( self ):
		return 
	def palatal_obstruents( self ):
		return 
	def coronal_obstruents( self ):
		return 
		
#### Iterator class. ####
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






 

