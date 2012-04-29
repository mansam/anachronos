import anachronos
from logic import *
from map import *
from game import *
generator = MapGenerator()
map = generator.create_map('dirt', 50)
state = GameState(game_map=map)
print a_star(map.tile(0,0), map.tile(1,1))