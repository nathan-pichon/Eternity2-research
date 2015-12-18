# class that represent one piece of the puzzle
class piece:
	# Ctor 
	def __init__(self, right, left, top, bottom):
		self.faces = [top, left, bottom, right]