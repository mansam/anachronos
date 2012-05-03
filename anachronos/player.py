class Player(object):

	def __init__(self, name, color):
		self.units = []
		self.deployed_units = {}
		self.undeployed_units = {}
		self.color = color
		self.name = name
		self.actions = []
		self.paradox = 100
		self.orders = []
		self.moves = []
		self.attacks = []
		self.move_number = 0
		self.attack_number = 0

	def begin_turn(self):
		self.actions = []
		self.moves = []
		self.attacks = []
		for unit in self.units:
			unit.acted = False

	def is_alive(self):
		alive = False
		for unit in self.deployed_units:
			if unit.life > 0:
				return True
		return alive