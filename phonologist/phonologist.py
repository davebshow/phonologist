# -*- encoding: utf-8 -*-

import codecs
from fmatrixutils import *
from constants import   IPA_SYMBOLS, STRESS, VOWELLS, CONSONANTS, PERIOD, COMMA, SYLLABLE

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
	# Returns a dictionary with { target as keys : incidence as value}

	# UNI
	def target_symbols( self, *ipa_symbols):
		count_dict = {}
		data = ''.join(self.tokens)
		for symbol in data:
			if symbol.encode('utf-8') in ipa_symbols:
				count_dict.setdefault(symbol,0)
				count_dict[symbol] += 1
		return count_dict

	# GEN
	def _stressed( self, token ):
		if STRESS in token:
			return True
		else:
			return False

#########################################################################
# Token level methods # # GEN
#########################################################################

	# Count the incidence of any number of the target tokens passed as arguments.
	# Returns a dictionary with { target as keys : incidence as value}
	def target_tokens( self, *target_tokens ):
		count_dict = {}
		for token in self.tokens:
			if token.encode('utf-8') in target_tokens:
				count_dict.setdefault( token, 0 )
				count_dict[token] += 1
		return count_dict

	def preceding_tokens( self, target ):
		count_dict = {}
		for ndx, token in enumerate(self.tokens[ 1: ]):
			if token.encode( 'utf-8' ) in target:
				print token 
				count_dict.setdefault( self.tokens[ ndx ], 0 )
				count_dict[ self.tokens[ ndx ] ] += 1
		return count_dict 

	def posterior_token( self, target ):
		count_dict = {}
		ndx = 0
		for i in range( len( self.tokens ) - 1 ):
			if self.tokens[ndx].encode( 'utf-8' ) in target:
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
	def __init__( self, IPA_txtfile ):
		self.tokens = self.load_file( IPA_txtfile )
	def preceding_phrase(self,token):
		pass

class Words( Phonologist ):
	def __init__( self, IPA_txtfile ):
		self.tokens = self.load_file( IPA_txtfile )

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
		count_dict = {"pretonic":0,"postonic":0}
		for token in self.tokens:
			for sym in token:
				if sym.encode('utf-8') in target:
					print token
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
		print stoken
		if len(stoken) > 1:
			for ndx, syll in enumerate( stoken ):
				if not self._stressed(syll):
					for sym in syll:
						if sym in target:
							if ndx > 0:
								if STRESS in stoken[ndx-1]:
									count_dict["pretonic"] += 1
							if ndx < len(stoken) - 1:
								if STRESS in stoken[ndx+1]:
									count_dict["postonic"] += 1			
			return count_dict
		else:
			return count_dict

class Syllables( Phonologist ):

	def __init__( self, IPA_txtfile ):
		self.tokens = self.load_file( IPA_txtfile )

	# SYL FIX FOR STRESS
	def preceding_symbol( self, target  ):
		count_dict = {}
		data = ''.join( self.tokens )
		for ndx,symbol in enumerate( data[ 1:] ):
			if symbol.encode('utf-8') in target:
				count_dict.setdefault( data[ ndx ],0 )
				count_dict[data[ ndx ]] += 1
		return count_dict

	 # SYL
	def preceding_consonant( self, target ):
		count_dict = {}
		data = ''.join( self.tokens )
		for ndx,symbol in enumerate( data[ 1:] ):
			if symbol.encode('utf-8') in target:
				if STRESS not in data[ndx]:
				### will remove encoding later
					if data[ ndx ].encode('utf-8') in CONSONANTS:
						count_dict.setdefault( data[ ndx ],0 )
						count_dict[data[ ndx ]] += 1
				else:
					if ndx > 0:
						if data[ ndx ].encode('utf-8') in CONSONANTS:
							count_dict.setdefault( data[ ndx - 1 ],0 )
							count_dict[data[ ndx - 1 ]] += 1
		return count_dict
	# SYL
	def preceding_vowell( self, target ):
		count_dict = {}
		data = ''.join( self.tokens )
		for ndx,symbol in enumerate( data[ 1:] ):
			if symbol.encode('utf-8') in target:
				if STRESS not in data[ndx]:
				### will remove encoding later
					if data[ ndx ].encode('utf-8') in VOWELLS:
						count_dict.setdefault( data[ ndx ],0 )
						count_dict[data[ ndx ]] += 1
				else:
					if ndx > 0:
						if data[ ndx ].encode('utf-8') in VOWELLS:
							count_dict.setdefault( data[ ndx - 1 ],0 )
							count_dict[data[ ndx - 1 ]] += 1
		return count_dict

	# SYL fix for stress
	def posterior_symbol( self, target ):
		count_dict = {}
		data = ''.join( self.tokens )
		ndx = 0
		for i in range( len( data ) - 1):
			if data[ndx].encode( 'utf-8' ) in target:
				count_dict.setdefault( data[ ndx + 1 ],0 )
				count_dict[data[ ndx + 1 ]] += 1
			ndx += 1
		return count_dict	

	# SYL
	def posterior_consonant( self, target ):
		count_dict = {}
		data = ''.join( self.tokens )
		ndx = 0
		for i in range( len( data ) - 1):
			if data[ndx].encode( 'utf-8' ) in target:
				### will remove encoding when 
				if STRESS not in data[ndx+1]:
					if data[ ndx + 1].encode('utf-8') in CONSONANTS:
						print "cons",data[ndx + 1]
						count_dict.setdefault( data[ ndx + 1 ],0 )
						count_dict[data[ ndx + 1 ]] += 1
				else:
					if data[ndx + 2].encode('utf-8') in CONSONANTS:
						print "cons",data[ndx + 2]
						count_dict.setdefault( data[ ndx + 2 ],0 )
						count_dict[data[ ndx + 2 ]] += 1						
			ndx += 1
		return count_dict	

	#SYL
	def posterior_vowell( self, target ):
		count_dict = {}
		data = ''.join( self.tokens )
		ndx = 0
		for i in range( len( data ) - 1):
			if data[ndx].encode( 'utf-8' ) in target:
				if STRESS not in data[ndx+1]:
					if data[ ndx + 1].encode('utf-8') in VOWELLS:
						count_dict.setdefault( data[ ndx + 1 ],0 )
						count_dict[data[ ndx + 1 ]] += 1
				else:
					if data[ ndx + 2].encode('utf-8') in VOWELLS:
						count_dict.setdefault( data[ ndx + 2 ],0 )
						count_dict[data[ ndx + 2 ]] += 1
			ndx += 1
		return count_dict	

	# SYL
	def return_tokens_sylls( self, target ):
		count_dict = {}
		for token in self.tokens:
			print token
			for sym in token:
				if sym.encode('utf-8') in target:
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

class Nsyllables( Syllables ):

	def __init__( self, ph_inst ):
		syllables = ph_inst.syllabify()
		self.tokens = syllables
		
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








 

