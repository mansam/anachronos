import curses
import map
import sys
generator = map.MapGenerator()
m = generator.create_map('dirt', int(sys.argv[1]))


myscreen = curses.initscr()
curses.start_color()
colorlist = (("red", curses.COLOR_RED), 
			 ("green", curses.COLOR_GREEN),
			 ("yellow", curses.COLOR_YELLOW),
			 ("blue", curses.COLOR_BLUE),
			 ("cyan", curses.COLOR_CYAN),
			 ("magenta", curses.COLOR_MAGENTA),
			 ("black", curses.COLOR_BLACK),
			 ("white", curses.COLOR_WHITE))
colors = {}
colorpairs = 0
for name, color in colorlist:
	colorpairs += 1 
	curses.init_pair(colorpairs, color, curses.COLOR_BLACK)
	colors[name]=curses.color_pair(color)
myscreen.refresh()

map_window = curses.newwin(61, 150, 0, 0)
#map_window.bkgd(' ', curses.color_pair(1))
map_window.border(0)
map_window.addstr(2,2, str(m))
menu_window = curses.newwin(61, 31, 0, 151)
menu_window.addstr(1,8,"Anachronos Menu")
menu_window.border(0)
map_window.refresh()
menu_window.refresh()

myscreen.getch()

curses.endwin()