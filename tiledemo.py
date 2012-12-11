
import pygame
import pygame.locals
import random
import sys

sys.setrecursionlimit(10000)

def load_tile_table(filename, width, height):
	image = pygame.image.load(filename).convert()
	image_width, image_height = image.get_size()
	tile_table = []
	for tile_x in range(0, image_width/width):
		#line = []
		#tile_table.append(line)
		for tile_y in range(0, image_height/height):
			rect = (tile_x*width, tile_y*height, width, height)
			tile_table.append(image.subsurface(rect))
	return tile_table

regional_probabilities = {
	"water":[("water", .3), ("dirt", .35), ("tree", .2), ("grass", .1), ("hill", .05)],
	"dirt":[("dirt", .4), ("grass", .25), ("hill", .2), ("water", .1), ("tree", .05)],
	"grass":[("tree", .4), ("grass", .25), ("dirt", .2), ("water", .1), ("hill", .05)],
	"hill":[("tree", .5), ("hill", .15), ("dirt", .2), ("water", .1), ("grass", .05)],
	"tree":[("tree", .3), ("hill", .25), ("grass", .3), ("water", .1), ("dirt", .05)]
}

def get_adjacent(x, y, size):
	"""

	"""

	coords = []
	for tuple in ((-1, 0), (0, -1), (1, 0), (0, 1)):
			new_x = tuple[0]+x
			new_y = tuple[1]+y
			if new_x >= 0 and new_x < size and new_y >= 0 and new_y < size and (new_x, new_y) != (x, y):
				coords.append((new_x, new_y))
	return coords

def weighted_choice(lst):
	n = random.uniform(0, 1)
	for item, weight in lst:
		if n < weight:
			break
		n = n - weight
	return item

def create_map(starting_terrain, size, tileset="default"):
	"""
	Holy shit this sucks less now.

	"""
	

	rows = []
	for x in range(0, size):
		row = []
		for y in range(0, size):
			row.append(None)
		rows.append(row)

	modifier = .10
	curr_tile = (0,0)
	draw_prob = 4

	def paint(tile, terrain, prob, mod, iteration=0, queue=[], visited=[]):
		if random.random() <= prob:
			rows[tile[0]][tile[1]] = 1
			terrain_to_paint = terrain_types['default'][terrain][0]
			if isinstance(terrain_to_paint, list):
				terrain_to_paint = random.choice(terrain_to_paint)
			screen.blit(terrain_to_paint, (tile[0]*16, tile[1]*16))
			prob -= mod
			mod += .01
			if mod < 0:
				mod = 0
		else:
			terrain = weighted_choice(regional_probabilities[terrain])
			rows[tile[0]][tile[1]] = 1
			terrain_to_paint = terrain_types['default'][terrain][0]
			if isinstance(terrain_to_paint, list):
				terrain_to_paint = random.choice(terrain_to_paint)
			screen.blit(terrain_to_paint, (tile[0]*16, tile[1]*16))
			prob = 4
			mod = .01
		tiles = get_adjacent(tile[0], tile[1], size)
		random.shuffle(tiles)
		iteration += 1
		for t in tiles:
			if not rows[t[0]][t[1]]:
				paint(t, terrain, prob, mod, iteration)

	paint(curr_tile, starting_terrain, draw_prob, modifier)

if __name__=='__main__':
	pygame.init()
	screen = pygame.display.set_mode((1000,950))
	menu = pygame.Surface((200,800))
	bottom = pygame.Surface((1000, 150))
	menu.fill((255,0,0))
	bottom.fill((0,0,255))
	screen.fill((255, 255, 255))
	tile_table = load_tile_table("tiles.png", 16, 16)
	grass_table = load_tile_table("grass.bmp", 16, 16)
	mountain_table = load_tile_table("mountain.png", 16, 16)
	terrain_types = {

	"default":{
		"tree":[tile_table[3], True],
		"hill":[mountain_table, False],
		"water":[tile_table[4], False],
		"dirt":[tile_table[0], True],
		"grass":[grass_table, True],
	}
}
	create_map('dirt', 50)
	screen.blit(menu, (800, 0))
	screen.blit(bottom, (0, 800))
	pygame.display.flip()
	print terrain_types
	while pygame.event.wait().type != pygame.locals.QUIT:
		pass


