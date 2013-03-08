#!/usr/bin/env python
# THIS ARE REALLY COOL GAMES, GUY.

import fabulous.color
from player import Player
import logic
from map import MapGenerator, Map
from game import GameState
import game
import sys
import os

def get_coords(map):
	coords = None
	while not coords:
		try:
			coords = raw_input(": ").split(',')
			coords[0] = int(coords[0])
			coords[1] = int(coords[1])
			if coords[0] < 0 or coords[0] >= map.size or coords[1] < 0 or coords[1] >= map.size:
				coords = None
		except:
			coords = None
	return coords

def display_map(state, player):
	state.paint_map()
	raw_input()

def display_unit_details(state, player):
	print "\n Enter the coordinates of the unit. (x,y)"
	coords = get_coords(state.map)
	unit = state.locate_unit(coords[0], coords[1])
	if unit:
		print ("%s: " % unit.player.name) + str(unit)
		raw_input()
	else:
		print "There is not a unit at that location."
		raw_input()

def move_unit(state, player):
	print "\nEnter the coordinates of the unit to move. (x,y)"
	coords = get_coords(state.map)
	unit = state.locate_unit(coords[0], coords[1])
	if unit and unit.player.name is player.name:
		print "Enter the coordinates to move to. (x,y)"
		moveto = get_coords(state.map)

		tile = state.map.tile(moveto[0], moveto[1])
		path = unit.can_move(tile)
		if path:
			player.move_number +=1
			player.paradox += logic.calculate_distance(unit.location, tile)/2
			player.moves.append(game.MoveAction(player.move_number, player, unit, unit.location, tile, path))
		if not path:
			print "Couldn't move that unit there."
			raw_input()
	else:
		print "You don't have a unit at that location."
		raw_input()

def deploy_units(state, player):
	raw_input()
	state.paint_map()
	for unit in player.units:
		deployed = False
		while not deployed:
			print "\nEnter coordinates to deploy %s" % unit
			coords = get_coords(state.map)
			unit_at = state.locate_unit(coords[0], coords[1])
			if not unit_at:
				deployed = unit.deploy(state.map.tile(coords[0], coords[1]))
		state.paint_map()

def attack(state, player):
	print "\nEnter the coordinates of the unit to attack with. (x,y)"
	coords = get_coords(state.map)
	unit = state.locate_unit(coords[0], coords[1])
	if unit and unit.player.name is player.name:
		print "Enter the coordinates to attack. (x,y)"
		attackto = get_coords(state.map)
		tile = state.map.tile(attackto[0], attackto[1])
		if unit.can_attack(tile):
			player.attack_number +=1
			player.paradox += logic.calculate_distance(unit.location, tile)/2
			player.attacks.append(game.AttackAction(player.attack_number, player, unit, unit.location, tile))
		else:
			print "Couldn't use that unit to attack there."
			raw_input()
	else:
		print "You don't have a unit at that location."
		raw_input()


def forfeit(state, player):
	over = """
   _____                         ____                  
  / ____|                       / __ \                 
 | |  __  __ _ _ __ ___   ___  | |  | |__   _____ _ __ 
 | | |_ |/ _` | '_ ` _ \ / _ \ | |  | |\ \ / / _ \ '__|
 | |__| | (_| | | | | | |  __/ | |__| | \ V /  __/ |   
  \_____|\__,_|_| |_| |_|\___|  \____/   \_/ \___|_|         
	"""

	print over
	print "\t%s has forfeit the battle.\n" % player.name
	raw_input()
	sys.exit(0)

def previous_moves(state, player):
	print "\nSee moves from which turn? (Current turn is %d) (0 to cancel)" % state.turn_number
	turn = -1
	while turn < 1 or turn > state.turn_number - 1:
		try:
			turn = int(raw_input(": "))
		except:
			pass
		if turn == 0:
			return

	moves = [move for move in state.move_stack[turn] if move.unit.player.name == player.name]
	for move in moves:
		print move
	raw_input()

def previous_attacks(state, player):
	print "\nSee attacks from which turn? (Current turn is %d) (0 to cancel)" % state.turn_number
	turn = -1
	while turn < 1 or turn > state.turn_number - 1:
		try:
			turn = int(raw_input(": "))
		except:
			pass
		if turn == 0:
			return

	attacks = [attack for attack in state.attack_stack[turn] if attack.unit.player.name == player.name]
	for attack in attacks:
		print attack
	raw_input()

def previous_map(state, player):
	print "\nSee map from which turn? (Current turn is %d) (0 to cancel)" % state.turn_number
	turn = -1
	while turn < 1 or turn > state.turn_number - 1:
		try:
			turn = int(raw_input(": "))
		except:
			pass
		if turn == 0:
			return


	oldmap = Map(state.map.size)
	oldmap.zones = state.map_stack[turn]
	oldmap.draw()
	raw_input()

def undo_move(state, player):
	print "\nUndo which move? (turn, id) (0,0 to cancel)"
	move = (-1,-1)
	while move[0] < 1 or move[0] > state.turn_number - 1 or move[1] < 1:
		try:
			move = raw_input(": ").split(',')
			move[0] = int(move[0])
			move[1] = int(move[1])
			if len(move) < 2:
				move.append(0)
		except:
			pass
		if move == (0,0):
			return
		if player.paradox - move[0] < 0:
			print "Insufficient paradox points. You would destabilize the timestream!"
			return

	player.paradox -= move[0]*10
	state.undo_move(move[0], move[1])
	state.replay(move[0])

def undo_attack(state, player):
	print "\nUndo which attack? (turn, id) (0,0 to cancel)"
	move = (-1,-1)
	while move[0] < 1 or move[0] > state.turn_number - 1 or move[1] < 1:
		try:
			move = raw_input(": ").split(',')
			move[0] = int(move[0])
			move[1] = int(move[1])
			if len(move) < 2:
				move.append(0)
		except:
			pass
		if move == (0,0):
			return
		if player.paradox - move[0] < 0:
			print "Insufficient paradox points. You would destabilize the timestream!"
			return

	player.paradox -= move[0]*10
	state.undo_attack(move[0], move[1])
	state.replay(move[0])

def game_over(state, player):
	over = """
   _____                         ____                  
  / ____|                       / __ \                 
 | |  __  __ _ _ __ ___   ___  | |  | |__   _____ _ __ 
 | | |_ |/ _` | '_ ` _ \ / _ \ | |  | |\ \ / / _ \ '__|
 | |__| | (_| | | | | | |  __/ | |__| | \ V /  __/ |   
  \_____|\__,_|_| |_| |_|\___|  \____/   \_/ \___|_|                                              
	"""

	print over
	print "\t%s ended their turn with no units.\n" % player.name
	raw_input()
	sys.exit(0)


def display_turn_menu(state, player):

	end = False

	state.paint_map()

	commands = {
	"1":display_map,
	"2":display_unit_details,
	"3":move_unit,
	"4":attack,
	"5":previous_moves,
	"6":undo_move,
	"7":previous_attacks,
	"8":undo_attack,
	"9":previous_map,
	"e":None,
	"q":forfeit
	}

	while not end:
		command = ""
		while command not in commands:
			state.paint_map()

			print "\n%s, it is your turn." % player.name
			print "PARADOX (%s)" % str(fabulous.color.cyan(str(player.paradox)))
			print """
		[1] View Map
		[2] View Unit Details
		[3] Move Unit
		[4] Attack
		[5] View Past Moves
		[6] Undo Past Moves
		[7] View Past Attacks
		[8] Undo Past Attacks
		[9] View Past Maps
		[e] End turn
		[q] Forfeit
			""" + "\n"

			command = raw_input(": ")
		if command == "e":
			end = True
		else:
			commands[command](state, player)


anachronos_title = """
      O~                                                                                    
     O~ ~~                               O~~                                                
    O~  O~~    O~~ O~~     O~~       O~~~O~~     O~ O~~~   O~~    O~~ O~~     O~~     O~~~~ 
   O~~   O~~    O~~  O~~ O~~  O~~  O~~   O~ O~    O~~    O~~  O~~  O~~  O~~ O~~  O~~ O~~    
  O~~~~~~ O~~   O~~  O~~O~~   O~~ O~~    O~~  O~~ O~~   O~~    O~~ O~~  O~~O~~    O~~  O~~~ 
 O~~       O~~  O~~  O~~O~~   O~~  O~~   O~   O~~ O~~    O~~  O~~  O~~  O~~ O~~  O~~     O~~
O~~         O~~O~~~  O~~  O~~ O~~~   O~~~O~~  O~~O~~~      O~~    O~~~  O~~   O~~    O~~ O~~
"""
anachronos_subtitle = """
								(c) 2012 Ducks Unlimited
"""

welcome = """

Welcome to Anachronos. 
Anachronos is a turn-based strategy game where the orders you give your units are not final.
By spending your Paradox points wisely, you can turn back the clock, prevent battles from occuring,
or turn the tables on your opponent completely.

... spend your Paradox points carelessly, and you'll wish you'd never tampered with time at all.

"""

players_prompt = "How many players will be engaging in battle: "
name_prompt = "Enter your name: "
color_prompt = "Please enter your prefered army color: "
map_prompt = "Enter the name of a pregenerated map file, else leave your battlefield up to the fickle hand of fate: "

player_deployments = ["%s will deploy in the top left corner of the map.",
						"%s will deploy in the bottom right corner of the map.",
						"%s will deploy in the top left corner of the map.",
						"%s will deploy in the bottom right corner of the map."]

if __name__ == '__main__':

	print fabulous.color.bold(anachronos_title)
	print anachronos_subtitle
	print welcome

	player_num = 0

	while player_num < 2 or player_num > 4:
		try:
			player_num = int(raw_input(players_prompt))
		except:
			print "Please enter a value that makes sense."

	players = []
	for i in range(0, player_num):
		pname = raw_input(name_prompt)
		pcolor = raw_input(color_prompt)
		player = Player(pname, pcolor)
		players.append(player)

	generator = MapGenerator()
	game_map = generator.create_map('dirt', 40)

	state = GameState(game_map=game_map, players=players)

	print "\nBeginning deployment phase"
	for i in range(0, player_num):
		print player_deployments[i] % players[i].name
		deploy_units(state, players[i])

	while True:
		for player in state.players:
			player.begin_turn()
			display_turn_menu(state, player)
			if not player.is_alive():
				game_over(state, player)
		state.play()

