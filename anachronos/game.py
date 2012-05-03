#!/usr/bin/env python
#-*- coding: utf-8 -*-

import logic
import unit
import copy
import fabulous
from copy import deepcopy
from collections import deque

COLORS = logic.load_config("colors.data")
DEFAULTS = logic.load_config("defaults.data")

class GameState(object):

	def __init__(self, game_map=None, players=[]):

		self.map = game_map
		self.players = players
		self.action_stack = deque()
		self.map_stack = {1:deepcopy(self.map.zones)}
		self.move_stack = {1:[]}
		self.attack_stack = {1:[]}
		self.unit_factory = unit.UnitFactory()	
		for player in self.players:
			player.state = self
			for key in DEFAULTS:
				player.undeployed_units[key] = []
				for i in range(0, int(DEFAULTS[key[0]])):
					player.undeployed_units[key] += self.unit_factory.create_unit(key, player)
		
		self.turn_number = 1
		self.copied_map = None

	def run_turn(self):
		for player in self.players:
			for unit in player.units:
				pass

	def locate_unit(self, x,y):
		return self.map.tile(x,y).occupant

	def mark_paths(self):
		for player in self.players:
			for move in player.moves:
				if move.path and move.active:
					for tile in move.path:
						tile.mark('✦ ', (255,0,0))

	def paint_map(self):
		import os
		try:
			os.system("clear")
		except:
			pass
		self.mark_paths()
		self.map.draw()

	def play(self):
		self.map_stack[self.turn_number] = deepcopy(self.map.zones)
		self.move_stack[self.turn_number] = []
		self.attack_stack[self.turn_number] = []

		self.paint_map()

		for player in self.players:
			move_results = []
			for move in player.moves:
				self.move_stack[self.turn_number].append(copy.copy(move))
				move_results = move.play()
				self.paint_map()
				print move
			for result in move_results:
				print result
		for player in self.players:
			attack_results = []
			for attack in player.attacks:
				self.attack_stack[self.turn_number].append(copy.copy(attack))
				attack_results = attack.play()
				self.paint_map()
			for result in attack_results:
				print result
		self.turn_number += 1
		input("Press any key to continue.")

	def undo_move(self, turn_number, move_number):
		move = [move for move in self.move_stack[turn_number] if move.id == move_number][0]
		self.move_stack[turn_number].remove(move)

	def undo_attack(self, turn_number, attack_number):
		attack = [attack for attack in self.attack_stack[turn_number] if attack.id == attack_number][0]
		self.attack_stack[turn_number].remove(attack)

	def replay(self, turn_number):
		self.map.zones = self.map_stack[turn_number]
		for turn in range(turn_number, self.turn_number):
			if turn - 1 > 0:
				self.map_stack[turn] = deepcopy(self.map_stack[turn-1])

			self.paint_map()

			for move in self.move_stack[turn]:
				move_results = []
				move_results = move.play()
				self.paint_map()
				for result in move_results:
					print result
			for attack in self.attack_stack[turn]:
				attack_results = []
				attack_results = attack.play()
				self.paint_map()
				for result in attack_results:
					print result
		print fabulous.color.blue("Temporal reflow complete!")
		input("Press any key to continue.")


class Action(object):
	"""
	Representation of a player's turn.

	"""

	def __init__(self):
		self.path = None
		self.active = True

	def play(self):
		self.active = False
		return ""

class AttackAction(Action):
	"""
	Representation of an attack made by one player's unit.

	"""

	def __init__(self, id, player, unit, unit_pos, tile):
		Action.__init__(self)
		self.id = id
		self.unit = unit
		self.player = player
		self.unitx = unit_pos.x
		self.unity = unit_pos.y
		self.tile = tile
		self.active = True
		self.state = None

	def play(self):
		self.active = False
		u = self.player.state.locate_unit(self.unitx, self.unity)
		return u.attack(self.player.state.map.tile(self.tile.x, self.tile.y))

	def __str__(self):
		u = self.player.state.locate_unit(self.unitx, self.unity)
		return "[%d] %s attacked tile (%d,%d) with %s" % (self.id, u.player.name, self.tile.x, self.tile.y, u.name)


class MoveAction(Action):
	"""
	Representation of a movement made by one player's unit.

	"""

	def __init__(self, id, player, unit, unit_pos, tile, path):
		Action.__init__(self)
		self.id = id
		self.player = player
		self.unit = unit
		self.unitx = unit_pos.x
		self.unity = unit_pos.y
		self.tile = tile
		self.path = path
		self.active = True

	def play(self):
		self.active = False
		u = self.player.state.locate_unit(self.unitx, self.unity)
		return u.move(self.player.state.map.tile(self.tile.x, self.tile.y))
		
	def __str__(self):
		u = self.player.state.locate_unit(self.tile.x, self.tile.y)
		return "[%d] %s moved %s to tile (%d,%d)" % (self.id, u.player.name, u.name, self.tile.x, self.tile.y)