import pygame
import math
import time

# node object

class Node:
	def __init__(self, x, y, is_solid):
		self.x = x
		self.y = y
		self.is_solid = is_solid
		self.previous_node = None
		self.f = None
		self.g = None
		self.h = None

	def set_cost(self, g, h):
		self.g = g
		self.h = h
		self.f = g + h

	def set_parent(self, previous_node):
		self.previous_node = previous_node


# helper methods

def paint_grid(x, y, color):
	pygame.draw.rect(window, color, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def reset_pointers(nodes):	# resets the pointer of every node
	for row in range(len(nodes)):
		for col in range(len(nodes[row])):
			nodes[row][col].set_parent(None)

def reset_grid():	# resets the grid with new nodes
	global grid
	global start
	global end

	grid = []

	for row in range(DIMENSIONS[0]):
		new = []
		for col in range(DIMENSIONS[1]):
			new.append(Node(col, row, False))
		grid.append(new)

	start = None
	end = None

def get_distance(node1, node2):	# calculates the distance between 2 nodes
	distance_x = abs(node1.x - node2.x)
	distance_y = abs(node1.y - node2.y)
	remainder = abs(distance_x - distance_y)

	return (max(distance_x, distance_y) - remainder) * 14 + remainder * 10

def get_lowest_node(nodes):	# gets the node with the lowest f code in a list
	lowest = nodes[0]

	for i in range(len(nodes)):
		if nodes[i].f == lowest.f:
			if nodes[i].h < lowest.h:
				lowest = nodes[i]
		elif nodes[i].f < lowest.f:
			lowest = nodes[i]

	return lowest

# pathfinding algorithm - configures the nodes' pointers

def find_path():
	open_nodes = []		# nodes to be evaluated
	closed_nodes = []	# evaluated nodes
	start_node = grid[start[1]][start[0]]
	end_node = grid[end[1]][end[0]]

	open_nodes.append(start_node) # add start node
	start_node.set_cost(0, get_distance(start_node, end_node))

	while True:
		current = get_lowest_node(open_nodes)
		open_nodes.remove(current)
		closed_nodes.append(current)

		if current == end_node:
			return

		if not current == start_node:
			paint_grid(current.x, current.y, EXPLORED_COLOUR)
			pygame.display.update()
			time.sleep(DELAY)

		for row in range(3):
			y = current.y - 1 + row

			for col in range(3):
				x = current.x - 1 + col

				# for every traversable neighbouring node
				if x < 0 or y < 0 or x >= DIMENSIONS[0] or y >= DIMENSIONS[1]:
					continue

				neighbour = grid[y][x]

				if (neighbour in closed_nodes) or (neighbour.is_solid) or (neighbour == current):
					continue

				# calculate current cost of the route to node
				g = current.g + 10
				if abs(x - current.x) == 1 and abs(y - current.y) == 1:	# if diagonal
					g += 4
				h = get_distance(neighbour, end_node)		
				f = g + h

				if not neighbour in open_nodes or f < neighbour.f:
					neighbour.set_cost(g, h)
					neighbour.set_parent(current)
					if neighbour not in open_nodes:
						open_nodes.append(neighbour)

# variables

GRID_SIZE = 20
DIMENSIONS = 40, 40
WINDOW_WIDTH = DIMENSIONS[0] * GRID_SIZE
WINDOW_HEIGHT = DIMENSIONS[1] * GRID_SIZE
DELAY = 0.01 	# delay between painting nodes in seconds

OBSTACLE_COLOUR = (40, 40, 40)
BLANK_COLOUR = (255, 255, 255)
START_COLOUR = (255, 100, 100)
PATH_COLOUR = (130, 255, 130)
END_COLOUR = (100, 100, 255)
EXPLORED_COLOUR = (255, 255, 150)

start = None	# coordinates of the starting node
end = None		# coordinates of the end node
grid = []		# holds the nodes
ready = True	# boolean for if the program is ready to find_path again
running = True

# pygame
reset_grid()
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("A* Pathfinder")
pygame.draw.rect(window, BLANK_COLOUR, (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if not ready:	# make sure the user is ready to go again if they press space
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					pygame.draw.rect(window, BLANK_COLOUR, (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))

					for row in range(len(grid)):
						for col in range(len(grid[row])):
							if grid[row][col].is_solid:
								paint_grid(col, row, OBSTACLE_COLOUR)

					paint_grid(start[0], start[1], START_COLOUR)
					paint_grid(end[0], end[1], END_COLOUR)
					ready = True
		else:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and not start == None and not end == None:
					try:
						ready = False

						reset_pointers(grid)
						find_path()
						paint_grid(start[0], start[1], START_COLOUR)
						paint_grid(end[0], end[1], END_COLOUR)

						current_node = grid[end[1]][end[0]].previous_node	# backtrack  from end node

						while not current_node.previous_node == None:
							paint_grid(current_node.x, current_node.y, PATH_COLOUR)
							current_node = current_node.previous_node
							pygame.display.update()
							time.sleep(DELAY)
					except:		# usually occurs when a path is not possible
						pass
				if event.key == pygame.K_BACKSPACE:	# clear grid if backspace is pressed
					reset_grid()
					pygame.draw.rect(window, BLANK_COLOUR, (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))

			if event.type == pygame.MOUSEBUTTONDOWN:		# if user presses the scroll wheel
				if event.button == 2:
					x, y = [math.floor(i / GRID_SIZE) for i in pygame.mouse.get_pos()]

					if [x, y] == start or [x, y] == end:	# if user reclick start or end
						paint_grid(x, y, BLANK_COLOUR)

						if [x, y] == start:
							start = None

						if [x, y] == end:
							end = None
					else:	# if its their first first time placing start/end
						if start == None:
							start = [x, y]
							grid[y][x].is_solid = False
							paint_grid(x, y, START_COLOUR)
						elif end == None:
							end = [x, y]
							grid[y][x].is_solid = False
							paint_grid(x, y, END_COLOUR)				

			# if the user presses left or right click
			if pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2]:
				x, y = [math.floor(i / GRID_SIZE) for i in pygame.mouse.get_pos()]

				if not ([x, y] == start or [x, y] == end):
					if pygame.mouse.get_pressed()[0]:
						grid[y][x].is_solid = True
						paint_grid(x, y, OBSTACLE_COLOUR)
					else:
						grid[y][x].is_solid = False
						paint_grid(x, y, BLANK_COLOUR)

	pygame.display.update()

pygame.quit()