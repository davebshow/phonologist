# -*- encoding: utf-8 -*-

import codecs
from fmatrixutils import *
from utils import force_unicode, load_file
from constants import   IPA_SYMBOLS, STRESS, VOWELLS, CONSONANTS, PERIOD, COMMA, SYLLABLE, FMATRIX

#### Object oriented library for working with IPA transcriptions. ####

#### Class to create the Phonetic Transcription Object. ####
class Phonologist( object ):

#### Create object. ####
	def __init__( self, tokens ):
		self.tokens = tokens
	
	@classmethod
	def loadfile( Phonologist, IPA_txtfile ):
		tokens = load_file( IPA_txtfile )
		return Phonologist(tokens)
		
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
	# Returns a dictionary with { target as keys : incidence as value}

	# UNI
	def target_symbols( self, ipa_symbol):
		ipa_symbol = force_unicode(ipa_symbol)
		count_dict = {}
		data = ''.join(self.tokens)
		for symbol in data:
			if symbol == ipa_symbol:
				count_dict.setdefault(symbol,0)
				count_dict[symbol] += 1
		return count_dict



#########################################################################
# Token level methods # # GEN
#########################################################################

	# Count the incidence of any number of the target tokens passed as arguments.
	# Returns a dictionary with { target as keys : incidence as value}
	def target_tokens( self, target_token ):
		target_token = force_unicode( target_token )
		count_dict = {}
		for token in self.tokens:
			if token == target_token:
				count_dict.setdefault( token, 0 )
				count_dict[token] += 1
		return count_dict

	def preceding_tokens( self, target ):
		target = force_unicode( target )
		count_dict = {}
		for ndx, token in enumerate(self.tokens[ 1: ]):
			if token == target:
				print token 
				count_dict.setdefault( self.tokens[ ndx ], 0 )
				count_dict[ self.tokens[ ndx ] ] += 1
		return count_dict 

	def posterior_token( self, target ):
		target = force_unicode( target )
		count_dict = {}
		ndx = 0
		for i in range( len( self.tokens ) - 1 ):
			if self.tokens[ndx] == target:
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
	#GEN
	def syllabify( self ):
		syllables = []
		for token in self.tokens:
			syllables.append(token.split("."))
		return sum(syllables,[]) # hehe good trick

	# GEN
	def _stressed( self, token ):
		if STRESS in token:
			return True
		else:
			return False
		

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

class Phrases( Phonologist ):
	def __init__( self, tokens ):
		self.tokens = tokens
	
	@classmethod
	def loadfile( Phrases, IPA_txtfile ):
		tokens = load_file( IPA_txtfile )
		return Phrases(tokens)

	def preceding_phrase(self,token):
		pass

class Words( Phonologist ):
	def __init__( self, tokens ):
		self.tokens = tokens
	
	@classmethod
	def loadfile( Words, IPA_txtfile ):
		tokens = load_file( IPA_txtfile )
		return Words(tokens)

	# WORD
	def return_tokens_words( self, target ):
		count_dict = {}
		for token in self.tokens:
			for sym in token:
				if sym.encode('utf-8') in target:
					count_dict.setdefault( token, 0 )
					count_dict[token] += 1
					break
		return count_dict
	# WORD
	def stressed_target_words( self, target ):
		### faster if I don't call return tokens
		tokens = self.return_tokens_words( target )
		count_dict = {}
		for token in tokens.keys():
			if STRESS in token:
				count_dict.setdefault(token,0)
				count_dict[ token ] += tokens[token]
		return count_dict

	# WORd
	def unstressed_target_words( self, target ):
		### faster if I don't call return tokens
		tokens = self.return_tokens_words( target )
		count_dict = {}
		for token in tokens.keys():
			if STRESS not in token:
				count_dict.setdefault(token,0)
				count_dict[ token ] += tokens[token]
		return count_dict

	#WORDs
	def pretonic_postonic_words( self, target ):
		target = force_unicode( target )
		count_dict = {"pretonic":0,"postonic":0}
		for token in self.tokens:
			for sym in token:
				if sym == target:
					token_dict = self._pretonic_postonic(target,token)
					count_dict["pretonic"] += token_dict["pretonic"]
					count_dict["postonic"] += token_dict["postonic"]
					break
		return count_dict
	# WORDS
	def _pretonic_postonic( self, target, token ):
		### Don't like all of this trying
		count_dict = {"pretonic":0,"postonic":0}
		stoken = token.split(".")
		if len(stoken) > 1:
			for ndx, syll in enumerate( stoken ):
				if not self._stressed(syll):
					for sym in syll:
						if sym in target:
							if ndx > 0 and STRESS in stoken[ndx-1]:
								count_dict["pretonic"] += 1
							if ndx < len(stoken) - 1 and STRESS in stoken[ndx+1]:
								count_dict["postonic"] += 1			
			return count_dict
		else:
			return count_dict

class Syllables( Phonologist ):

	def __init__( self, tokens ):
		if type(tokens) != list #untested
			tokens = tokens.syllabify()
		self.tokens = tokens
	
	@classmethod
	def loadfile( Syllables, IPA_txtfile ):
		tokens = load_file( IPA_txtfile )
		return Syllables(tokens)

	# SYL FIX FOR STRESS
	def preceding_symbol( self, target  ):
		target = force_unicode( target )
		count_dict = {}
		data = ''.join( self.tokens )
		for ndx,symbol in enumerate( data[ 1:] ):
			if symbol == target:
				count_dict.setdefault( data[ ndx ],0 )
				count_dict[data[ ndx ]] += 1
		return count_dict

	 # SYL
	def preceding_consonant( self, target ):
		target = force_unicode( target )
		count_dict = {}
		data = ''.join( self.tokens )
		for ndx,symbol in enumerate( data[ 1:] ):
			if symbol == target:
				if STRESS != data[ndx]: 
					if data[ ndx ] in CONSONANTS:
						count_dict.setdefault( data[ ndx ],0 )
						count_dict[data[ ndx ]] += 1
				elif ndx > 0 and data[ ndx - 1 ] in CONSONANTS:
					count_dict.setdefault( data[ ndx - 1 ],0 )
					count_dict[data[ ndx - 1 ]] += 1
		return count_dict
	# SYL
	def preceding_vowell( self, target ):
		target = force_unicode( target )
		count_dict = {}
		data = ''.join( self.tokens )
		for ndx,symbol in enumerate( data[ 1:] ):
			if symbol == target:
				if STRESS != data[ndx]: 
					if data[ ndx ] in VOWELLS:
						count_dict.setdefault( data[ ndx ],0 )
						count_dict[data[ ndx ]] += 1
				elif ndx > 0 and data[ ndx - 1 ] in VOWELLS:
					count_dict.setdefault( data[ ndx - 1 ],0 )
					count_dict[data[ ndx - 1 ]] += 1
		return count_dict

	# SYL fix for stress
	def posterior_symbol( self, target ):
		target = force_unicode( target )
		count_dict = {}
		data = ''.join( self.tokens )
		ndx = 0
		for i in range( len( data ) - 1):
			if data[ndx] == target:
				count_dict.setdefault( data[ ndx + 1 ],0 )
				count_dict[data[ ndx + 1 ]] += 1
			ndx += 1
		return count_dict	

	# SYL
	def posterior_consonant( self, target ):
		target = force_unicode( target )
		count_dict = {}
		data = ''.join( self.tokens )
		ndx = 0
		for i in range( len( data ) - 1):
			if data[ndx] == target:
				### will remove encoding when 
				if STRESS != data[ndx+1]:
					if data[ ndx + 1] in CONSONANTS:
						count_dict.setdefault( data[ ndx + 1 ],0 )
						count_dict[data[ ndx + 1 ]] += 1
				elif data[ndx + 2] in CONSONANTS:
					count_dict.setdefault( data[ ndx + 2 ],0 )
					count_dict[data[ ndx + 2 ]] += 1						
			ndx += 1
		return count_dict	

	#SYL
	def posterior_vowell( self, target ):
		target = force_unicode( target )
		count_dict = {}
		data = ''.join( self.tokens )
		ndx = 0
		for i in range( len( data ) - 1):
			if data[ndx] == target:
				if STRESS == data[ndx+1]:
					if data[ ndx + 1] in VOWELLS:
						count_dict.setdefault( data[ ndx + 1 ],0 )
						count_dict[data[ ndx + 1 ]] += 1
				elif data[ ndx + 2] in VOWELLS:
					count_dict.setdefault( data[ ndx + 2 ],0 )
					count_dict[data[ ndx + 2 ]] += 1
			ndx += 1
		return count_dict	

	# SYL
	def return_tokens_sylls( self, target ):
		targ = force_unicode( target )
		count_dict = {}
		for token in self.tokens:
			print token
			for sym in token:
				if sym == target:
					count_dict.setdefault( token, 0 )
					count_dict[token] += 1
		return count_dict
	
	def stressed_target_sylls( self, target ):
		### faster if I don't call return tokens
		tokens = self.return_tokens_sylls( target )
		count_dict = {}
		for token in tokens.keys():
			if STRESS in token:
				count_dict.setdefault(token,0)
				count_dict[ token ] += tokens[token]
		return count_dict

    #SYL
	def unstressed_target_sylls( self, target ):
		### faster if I don't call return tokens
		tokens = self.return_tokens_sylls( target )
		count_dict = {}
		for token in tokens.keys():
			if STRESS not in token:
				count_dict.setdefault(token,0)
				count_dict[ token ] += tokens[token]
		return count_dict


		
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








 

