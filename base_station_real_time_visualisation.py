import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation 
import random


def animate(i):
	plt.cla()
	
	G = nx.DiGraph()
	G.add_node(0)
	G.add_node(1)
	G.add_node(2)
	G.add_node('M')
	G.add_node('B')
	
	
	# explicitly set positions
	pos = {0: (0, 1.5), 1: (-0.10, 0), 2: (0, -1.5), 'M': (-0.10, -1.5), 'B': (0.10, 0)}

	with open("shared_1.txt", "r") as file_base_station:
		content_bs = file_base_station.read().strip()

	char_list_bs = list(content_bs)
	for x in char_list_bs:
		if x != '4':
			if int(x) == 3:
				G.add_edge('B', 'M')
			else:
				G.add_edge('B', int(x))
			 
	#Badge0		 
	with open("shared_badge_0.txt", "r") as file_badge_0:
		content_b0 = file_badge_0.read().strip()	
	char_list_0 = list(content_b0)
	for x in char_list_0:
		if x != '0':
			if x == '3':
				G.add_edge(0, 'M')
			else:
				G.add_edge(0, int(x))
	
	#Badge1
	with open("shared_badge_1.txt", "r") as file_badge_1:
		content_b1 = file_badge_1.read().strip()	
	char_list_1 = list(content_b1)
	for x in char_list_1:
		if x != '1':
			if x == '3':
				G.add_edge(1, 'M')
			else:
				G.add_edge(1, int(x))
	
	#Badge2
	with open("shared_badge_2.txt", "r") as file_badge_2:
		content_b2 = file_badge_2.read().strip()	
	char_list_2 = list(content_b2)
	for x in char_list_2:
		if x != '2':
			if x == '3':
				G.add_edge(2, 'M')
			else:
				G.add_edge(2, int(x))
	

	options = {
		"font_size": 36,
		"node_size": 3000,
		"node_color": "white",
		"edgecolors": "black",
		"linewidths": 5,
		"width": 5,
	}
	nx.draw_networkx(G, pos, **options)

	# Set margins for the axes so that nodes aren't clipped
	ax = plt.gca()
	ax.margins(0.20)
	plt.axis("off")


if __name__ == "__main__":	
	fig = plt.figure()
	ani = FuncAnimation(fig, animate, interval=0)
	plt.show()
