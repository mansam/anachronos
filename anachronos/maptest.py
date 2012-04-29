import map
import sys
generator = map.MapGenerator()
m = generator.create_map('dirt', int(sys.argv[1]))
m.draw()