######################################################
class Token( Object ):

	def __init__( self, token ):
		self.tokens = token

	def stressed( self ):
		if STRESS in self.tokens:
			return True
		else:
			return False

	def pretonic_postonic( self, target ):
		pass

	def preceding_symbol( self, target ):
		pass

	def posterior_symbol( self, target ):
		pass

	def syllabify( self ):
		return self.tokens.split(".")