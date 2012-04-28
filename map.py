import fabulous.color
import random
import sys

sys.setrecursionlimit(10000)

terrain_types = {
	"tree":[(0,75,0), (0,255,0), '^^', True],
	"hill":[(75,75,75),(0,0,0), '@@', False],
	"water":[(0,0,65), (0,0,255), '  ', False],
	"dirt":[(155,125,99), (200,200,200), '  ', True],
	"grass":[(10,100,0), (0,200,0), '..', True],
	"wall":[(20,20,20), (200,200,200), "##", False],
	"road":[(30,30,30), (255,255,0), "| ", True],
	"marker":[(0,0,0), (200,0,0), "..", True]
}

passable_types = {
	"dirt":[(155,125,99), (200,200,200), '  '],
	"grass":[(10,100,0), (0,200,0), '..']
}

regional_probabilities = {
	"water":[("water", .3), ("dirt", .35), ("tree", .2), ("grass", .1), ("hill", .05)],
	"dirt":[("dirt", .4), ("grass", .25), ("hill", .2), ("water", .1), ("tree", .05)],
	"grass":[("tree", .4), ("grass", .25), ("dirt", .2), ("water", .1), ("hill", .05)],
	"hill":[("tree", .5), ("hill", .15), ("dirt", .2), ("water", .1), ("grass", .05)],
	"tree":[("tree", .4), ("hill", .25), ("grass", .2), ("water", .1), ("dirt", .05)]
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

def paint(map, terrain, x, y):
	tile = map.tile(x,y)
	tile.bg_color = terrain_types[terrain][0]
	tile.fg_color = terrain_types[terrain][1]
	tile.fg_symbol = terrain_types[terrain][2]

class MapGenerator(object):


	def create_map(self, starting_terrain, size):
		"""
		Holy shit this sucks.

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

		def paint(array, tile, terrain, prob, mod, queue=[], visited=[]):
			if random.random() <= prob:
				rows[tile[0]][tile[1]] = terrain
				prob -= mod
				mod += .01
				if mod < 0:
					mod = 0
			else:
				terrain = weighted_choice(regional_probabilities[terrain])
				rows[tile[0]][tile[1]] = terrain
				prob = 4
				mod = .01
			tiles = get_adjacent(tile[0], tile[1], size)
			random.shuffle(tiles)
			for t in tiles:
				if not rows[t[0]][t[1]]:
					paint(array, t, terrain, prob, mod)		

		paint(rows, curr_tile, starting_terrain, draw_prob, modifier)
		new_map = Map(size)
		for x in range(0, size):
			for y in range(0, size):
				new_map.zones[x].tiles[y].bg_color = terrain_types[rows[x][y]][0]
				new_map.zones[x].tiles[y].fg_color = terrain_types[rows[x][y]][1]
				new_map.zones[x].tiles[y].fg_symbol = terrain_types[rows[x][y]][2]
				new_map.zones[x].tiles[y].passable = terrain_types[rows[x][y]][3]
		return new_map


class Zone(object):

	def __init__(self, tiles):
		self.tiles = tiles
		self.defender = None
		self.attacker = None

class Map(object):

	def __init__(self, size):
		self.zones = []
		self.size = size
		for x in range(0, size):
			tiles = []
			for y in range(0, size):
				tiles.append(Tile(x, y, self, terrain_types['dirt']))
			self.zones.append(Zone(tiles))
		self.p1_deployment = ((0,0), (0, size/2), (size/2, 0), (size/2, size/2))
		self.p2_deployment = ((size/2,size/2), (size/2, size), (size, size/2), (size, size))
		self.p3_deployment = ((size/2,0), (size/2, size/2), (size/2, 0), (size, size/2))
		self.p4_deployment = ((0,size/2), (0, size), (size/2, size/2), (size/2, size))


	def draw(self):
		sys.stdout.write("   ")
		for j in range(0, len(self.zones)):
			if j % 2 == 0:
				if j < 10:
					num = "0%d" % j
				else:
					num = str(j)
			else:
				num = "  "
			sys.stdout.write(num)
		for i in range(0, len(self.zones)):
			sys.stdout.write("\n" + str(i).zfill(2) + " ")
			for tile in self.zones[i].tiles:
				tile.draw()
		sys.stdout.write("\n")

	def tile(self, x, y):
		return self.zones[x].tiles[y]

class Tile(object):

	def __init__(self, x, y, map=None, terrain_type=[None, None, None, True]):
		self.occupant = None
		self.x = x
		self.y = y
		self.map = map
		self.bg_color = terrain_type[0]
		self.fg_color = terrain_type[1]
		self.fg_symbol = terrain_type[2]
		self.passable = terrain_type[3]
		self.temp_fg_symbol = None
		self.temp_fg_color = None
		self.temp_bg_color = None

	def __repr__(self):
		return "%d,%d" % (self.x, self.y)

	def mark(self, marker, color):
		self.temp_fg_symbol = marker
		self.temp_fg_color = color

	def draw(self):
		if self.occupant and self.occupant.life > 0:
			symbol = self.occupant.symbol
			fg_color = self.occupant.player.color
			bg_color = (75,75,75)
		elif self.temp_fg_symbol:
			symbol = self.temp_fg_symbol
			fg_color = self.temp_fg_color
			bg_color = self.bg_color
		else:
			symbol = self.fg_symbol
			fg_color = self.fg_color
			bg_color = self.bg_color
		if self.temp_bg_color:
			bg_color = self.temp_bg_color

		sys.stdout.write(str(fabulous.color.bg256(bg_color, fabulous.color.fg256(fg_color, symbol))))
		self.temp_fg_symbol = None
		self.temp_fg_color = None
		self.temp_bg_color = None

