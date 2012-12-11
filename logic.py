def calculate_distance(tilea, tileb, ceiling=True):
	"""
	Calculate the distance between two
	tiles on the map. Returns the ceiling
	of the distance by default.


	"""

	import math
	distance = math.sqrt(math.pow(tileb.x - tilea.x, 2) + math.pow(tileb.y - tilea.y, 2))
	if ceiling:
		return math.ceil(distance)
	else:
		return distance

def get_neighbor_tiles(tile, radius=1, check_passable=True):
	"""
	Return the neighbor tiles within a radius surrounding a center tile.
	Optionally considers whether a tile is passable when considering
	whether it is a neighbor.

	"""

	vals = [0]
	for i in range(1, radius+1):
		vals.append(i)
		vals.append(-i)

	adjacent_tiles = []
	for i in vals:
		for j in vals:
			new_x = tile.x+i
			new_y = tile.y+j
			if (new_x >= 0 and new_x < tile.map.size 
				and new_y >= 0 and new_y < tile.map.size 
				and (new_x, new_y) != (tile.x, tile.y)
				and (tile.map.tile(new_x, new_y).passable)):
					adjacent_tiles.append(tile.map.tile(new_x, new_y))
	return adjacent_tiles

def chunks(l, n):
	"""
	Divide map into evenly sized chunks.

	"""

	for i in xrange(0, len(l), n):
		yield l[i:i + n]

def load_config(config_file_name):
	config_dict = {}
	config_file = open(config_file_name).readlines()
	for config_entry in config_file:
		config = config_entry[:-1].split(" ")
		config_dict[config[0]] = config[1:]
	return config_dict

def a_star(start, goal, check_passable=True):
	"""
	Perform an A* search for the best path across a matrix.

	"""

	import operator

	closedset = set()	# The set of nodes already evaluated.
	openset = set([start])	# The set of tentative nodes to be evaluated, initially containing the start node
	came_from = {}   # The map of navigated nodes.
 
	g_score = {}
	h_score = {}
	f_score = {}

	g_score[start] = 0	# Cost from start along best known path.
	h_score[start] = calculate_distance(start, goal)
	f_score[start] = g_score[start] + h_score[start] # Estimated total cost from start to goal through y.

	while openset:
		sorted_fscore = sorted(f_score.iteritems(), key=operator.itemgetter(1))
		current = sorted_fscore[0][0]
		if current == goal:
			return reconstruct_path(came_from, goal)
 
		openset.remove(current)
		del f_score[current]
		closedset.add(current)
		for neighbor in get_neighbor_tiles(current, check_passable=check_passable):
			if neighbor in closedset:
				continue
			tentative_g_score = g_score[current] + calculate_distance(current, neighbor, ceiling=False)
 
			if neighbor not in openset:
				openset.add(neighbor)
				h_score[neighbor] = calculate_distance(neighbor, goal, ceiling=False)
				tentative_is_better = True
			elif tentative_g_score < g_score[neighbor]:
				tentative_is_better = True
			else:
				tentative_is_better = False
 
			if tentative_is_better:
				came_from[neighbor] = current
				g_score[neighbor] = tentative_g_score
				f_score[neighbor] = g_score[neighbor] + h_score[neighbor]
 
	return False
 
def reconstruct_path(came_from, current_node):
	if came_from.has_key(current_node):
		p = reconstruct_path(came_from, came_from[current_node])
		p.append(current_node)
		return p
	else:
		return [current_node]
