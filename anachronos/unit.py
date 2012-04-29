#-*- coding: utf-8 -*-

from logic import calculate_distance, get_adjacent_tiles, load_config
import fabulous.color
import logic

class Unit(object):

	def __init__(self, name, symbol, life, defense, attack, initiative, speed):
		self.name = name
		self.life = life
		self.defense = defense
		self._attack = attack
		self.initiative = initiative
		self.location = None
		self.speed = speed
		self.player = None
		self.symbol = symbol + "-"
		self.acted = False

	def attack(self, tile):
		if self._attack:
			results = self._attack(tile)
		else:
			results = ["%s is unarmed!" % self.name]
		self.acted = True
		return results

	def can_attack(self, tile):
		if not self.acted:
			dist = calculate_distance(tile, self.location)
			if dist <= self._attack.range:
				self.acted = True
				return True
		return False

	def move(self, tile):
		tile.occupant = self
		self.location.occupant = None
		self.location = tile
		self.acted = True
		return ["%s moved to (%d, %d)" % (self.name, tile.x, tile.y)] 

	def can_move(self, tile):
		if not tile.occupant and tile.passable and not self.acted:
			dist = calculate_distance(tile, self.location)
			if dist <= self.speed:
				path = logic.a_star(self.location, tile)
				if path:
					self.acted = True
					return path
		return False

	def receive_attack(self, roll, damage):
		if roll >= self.defense:
			
			if self.life - damage <= 0:
				self.die()
			else:
				self.life -= damage

			return "Attack dealt %d to %s" % (damage, self.name)
		else:
			return "Attack missed %s!" % self.name

	def die(self):
		self.location.occupant = None

	def deploy(self, tile):
		if not tile.occupant and tile.passable:
			self.location = tile
			tile.occupant = self
			return True
		return False

	def __str__(self):
		return "%s with %s life, armed with %s" % (str(fabulous.color.blue(self.name)), 
														str(fabulous.color.green(self.life)), 
														self._attack)

class Attack(object):

	def __init__(self, name, range, radius, damage, modifier):
		self.range = range
		self.radius = radius
		self.damage = damage
		self.modifier = modifier
		self.name = name

	def __call__(self, tile):
		# do something cool at the attacked tile
		import random
		roll = random.randint(1, 20) + self.modifier
		print roll

		if self.radius > 0:
			affected_tiles = get_adjacent_tiles(tile, self.radius) + [tile]
		else:
			affected_tiles = [tile]

		results = []
		for tile in affected_tiles:
			if tile.occupant:
				results.append(tile.occupant.receive_attack(roll, self.damage))
			tile.temp_bg_color = (128, 128, 20)
			tile.temp_fg_color = (255, 0, 0)
		return results

	def __str__(self):
		return str(fabulous.color.red(self.name)) + "(%d dmg, %d range, %d radius)" % (self.damage, self.range, self.radius)

class UnitFactory(object):

	def __init__(self):
		self.attack_config = load_config("attacks.data")
		self.unit_config = load_config("units.data")
		self.units = {}
		self.attacks = {}
		for entry in self.attack_config:
			self.attacks[entry] = Attack(entry,
											int(self.attack_config[entry][0]),
											int(self.attack_config[entry][1]),
											int(self.attack_config[entry][2]),
											int(self.attack_config[entry][3]))

	def create_unit(self, unit_name, player):
		if unit_name in self.unit_config:
			u = Unit(unit_name, 
					self.unit_config[unit_name][0], 
					int(self.unit_config[unit_name][1]), 
					int(self.unit_config[unit_name][2]),
					self.attacks[self.unit_config[unit_name][3]], 
					int(self.unit_config[unit_name][4]),
					int(self.unit_config[unit_name][5]))
			u.player = player
			return u



