#-*- coding: utf-8 -*-

from logic import calculate_distance, get_adjacent_tiles, load_config
import anachronos
import fabulous.color
import logic
import uuid
import random

class Unit(object):

	def __init__(self, name, symbol, life, defense, attack, initiative, speed, armor):
		self.id = str(uuid.uuid4())
		self.name = name
		self.life = life
		self.defense = defense
		self._attack = attack
		self.initiative = initiative
		self.location = None
		self.speed = speed
		self.player = None
		self.symbol = symbol
		self.acted = False
		self.armor = armor

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
	"""
	Represents an attack used by a fighting unit.  Attacks
	target tiles, and can have affects like changing ground color
	in their radius.

	TODO:  Find a way to use this for neat stuff like catapult
	TODO:  craters and blast marks.

	"""

	def __init__(self, name, arange, radius, damage, hitmod):
		self.id = str(uuid.uuid4())
		self.range = arange
		self.radius = radius
		self.damage = damage
		self.hitmod = hitmod
		self.name = name

	def __call__(self, tile):
		roll = random.randint(1, 20) + self.hitmod

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
		return str(fabulous.color.red(self.name)) + " (%d dmg, %d range, %d radius)" % (self.damage, self.range, self.radius)

class UnitFactory(object):
	#REFACTOR COMPLETED.
	"""
	Constructs new units.
	Units are defined in 'units.data'

	"""

	def __init__(self):
		"""
		Load attack prototypes from configuration file.

		"""

		self.attack_config = load_config("attacks.data")
		self.unit_config = load_config("units.data")
		self.units = anachronos.config['units']
		self.attacks = {}
		for entry in anachronos.config['attacks']:
			self.attacks[entry] = Attack(entry['name'],
											entry['range'],
											entry['radius'],
											entry['damage'],
											entry['hitmod'])

	def create_unit(self, unit_name):
		"""
		Create and return a unit.

		"""

		if unit_name in self.units:
			u = Unit(unit_name, 
					symbol=self.units[unit_name]["symbol"],
					life=self.units[unit_name]["life"],
					defense=self.units[unit_name]["defense"],
					attack=self.attacks[self.units[unit_name]["attack"]],
					initiative=self.units[unit_name]["initiative"],
					speed=self.units[unit_name]["speed"],
					armor=self.units[unit_name]["armor"])

			return u

	def give_unit(self, unit_name, player):
		"""
		Create a unit and add it to the player's
		undeployed units dictionary.

		"""

		unit = self.create_unit(unit_name)
		unit.player = player

		if unit_name not in player.undeployed_units:
			player.undeployed_units[unit_name] = []

		player.undeployed_units[unit_name].append(unit)



