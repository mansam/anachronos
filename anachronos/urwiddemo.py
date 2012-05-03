import urwid
import map
import sys

table = {
	"[0":'default',
	"[31":'redfg',
	"[32":'greenfg',
	"[33":'yellowfg',
	"[34":'bluefg',
	"[35":'magentafg',
	"[36":'cyanfg',
	"[37":'whitefg',
	"[40":'blackbg',
	"[41":'redbg',
	"[42":"greenbg",
	"[43":"yellowbg",
	"[44":"bluebg",
	"[45":"magentabg",
	"[46":"cyanbg",
	"[47":"whitebg"
}


palette = [
	('tree', 'light green', 'dark green', ('bold'), "#000", "#090"),
	('grass', "light green", "dark green", '', '#050', '#090'),
	('dirt', "dark gray", "light gray", '', '#550', '#440'),
	('hill', "dark gray", "light gray", '', '#333', ''),
	('water', "dark cyan", "dark blue", '', 'h12', '#00c')
]


markup = []


generator = map.MapGenerator()
new_map = generator.create_map('dirt', 50)

# for att in new_map).split("\033")[1:]:
# 	attr, text = att.split("m", 1)
# 	try:
# 		markup.append((table[attr], text))
# 	except:
# 		markup.append(('', text))
#print markup
# for tup in markup:
# 	sys.stdout.write(tup[1])

txt = urwid.Text(new_map.char())
fill = urwid.Filler(txt)
loop = urwid.MainLoop(fill, palette)
loop.screen.set_terminal_properties(colors=256)
loop.run()