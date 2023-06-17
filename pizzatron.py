'''
PIZZATRON TEST
Separate dev environment for the pizza minigame in The Big Cheese
'''

import simpleguitk as simplegui
import math, random

# Constants
FWIDTH = 400
FHEIGHT = 400
FWC = FWIDTH/2
FHC = FHEIGHT/2

BREAK_TIME = 120
ORDER_TIME = 299
PIZZA_BASE_REWARD = 15

# Normal variables
pizza_multiplier = 1

gamestate = 0
score = 0
timer_break = BREAK_TIME
timer_order = ORDER_TIME

ordered_pizza = [0, 0, 0, 0, 0, 0]
player_pizza = [0, 0, 0, 0, 0, 0]
dummy_list = [0, 1, 2, 3, 4, 5]

# Bell method
def bell_reset():
	global gamestate, timer_break, player_pizza, ordered_pizza, toppings, score
	
	score = 0
	for i in range(len(player_pizza)):
		if player_pizza[i] == 1 and ordered_pizza[i] == 1:
			score += 1
		elif player_pizza[i] == 1 and ordered_pizza[i] == 0:
			score -= 1
	if score <= 0:
		score = 0
	else:
		score = score / 3
		score = score * PIZZA_BASE_REWARD * pizza_multiplier
	
	gamestate = 0
	timer_break = BREAK_TIME
	player_pizza = [0, 0, 0, 0, 0, 0]
	ordered_pizza = [0, 0, 0, 0, 0, 0]
	
	toppings = random.sample(dummy_list, 3)
	for i in toppings:
		ordered_pizza[i] = 1

# Mouse handler
def m_click(pos):
	global player_pizza
	
	# Pizza buttons and bell
	if gamestate == 1:
		if pos[1] >= FHEIGHT - 140 and pos[1] <= FHEIGHT - 90:
			if pos[0] >= 20 and pos[0] <= 70:
				player_pizza[0] = 1
			elif pos[0] >= 90 and pos[0] <= 140:
				player_pizza[1] = 1
			elif pos[0] >= 160 and pos[0] <= 210:
				player_pizza[2] = 1
		elif pos[1] >= FHEIGHT - 70 and pos[1] <= FHEIGHT - 20:
			if pos[0] >= 20 and pos[0] <= 70:
				player_pizza[3] = 1
			elif pos[0] >= 90 and pos[0] <= 140:
				player_pizza[4] = 1
			elif pos[0] >= 160 and pos[0] <= 210:
				player_pizza[5] = 1
		elif (pos[0] >= 20 and pos[0] <= 70) and (pos[1] >= FHEIGHT - 210 and pos[1] <= FHEIGHT - 160):
			if gamestate == 1:
				bell_reset()

# Draw handler
def draw(canvas):
	global gamestate, timer_break, timer_order
	
	# Timer logic
	if gamestate == 0:
		timer_break -= 1
		if timer_break <= 0:
			gamestate = 1
			timer_order = ORDER_TIME
	elif gamestate == 1:
		if timer_order > 0:
			timer_order -= 1
	else:
		print("ERROR: Broken gamestate for pizza minigame, defaulting to state 0")
		gamestate = 0
	
	# Buttons
	canvas.draw_polygon([(20, FHEIGHT - 140), (70, FHEIGHT - 140), (70, FHEIGHT - 90), (20, FHEIGHT - 90)], 1, "Grey", "Grey")
	canvas.draw_polygon([(90, FHEIGHT - 140), (140, FHEIGHT - 140), (140, FHEIGHT - 90), (90, FHEIGHT - 90)], 1, "Grey", "Grey")
	canvas.draw_polygon([(160, FHEIGHT - 140), (210, FHEIGHT - 140), (210, FHEIGHT - 90), (160, FHEIGHT - 90)], 1, "Grey", "Grey")
	canvas.draw_polygon([(20, FHEIGHT - 70), (70, FHEIGHT - 70), (70, FHEIGHT - 20), (20, FHEIGHT - 20)], 1, "Grey", "Grey")
	canvas.draw_polygon([(90, FHEIGHT - 70), (140, FHEIGHT - 70), (140, FHEIGHT - 20), (90, FHEIGHT - 20)], 1, "Grey", "Grey")
	canvas.draw_polygon([(160, FHEIGHT - 70), (210, FHEIGHT - 70), (210, FHEIGHT - 20), (160, FHEIGHT - 20)], 1, "Grey", "Grey")
	
	# Temp text labels -- Cheese, Pepperoni, Mushroom, Olive, Bacon, Banana Pepper
	# Also temp pizza contents
	canvas.draw_text("C", (20, FHEIGHT - 90), 30, "White")
	canvas.draw_text("P", (90, FHEIGHT - 90), 30, "White")
	canvas.draw_text("M", (160, FHEIGHT - 90), 30, "White")
	canvas.draw_text("O", (20, FHEIGHT - 20), 30, "White")
	canvas.draw_text("B", (90, FHEIGHT - 20), 30, "White")
	canvas.draw_text("N", (160, FHEIGHT - 20), 30, "White")
	canvas.draw_text(str(player_pizza), (10, 120), 20, "White")
	
	# Bell
	bell_color = "Red"
	if gamestate == 1:
		bell_color = "Yellow"
	canvas.draw_polygon([(20, FHEIGHT - 210), (70, FHEIGHT - 210), (70, FHEIGHT - 160), (20, FHEIGHT - 160)], 1, bell_color, bell_color)
	
	# Order display
	if gamestate == 1 and timer_order > 0:
		canvas.draw_text(str(math.floor(timer_order/60)+1), (10, 40), 20, "White")
		canvas.draw_text(str(ordered_pizza), (10, 80), 20, "White")
	
	# Final result display
	if gamestate == 0:
		canvas.draw_text("You earned $" + str(round(score)) + "!", (10, 80), 20, "White")
	
	# Borders to accurately display size
	canvas.draw_polygon([(0, 0), (FWIDTH, 0), (FWIDTH, FHEIGHT), (0, FHEIGHT)], 5, "Grey")

# Game frame setup
frame = simplegui.create_frame("Pizzatron Test", FWIDTH, FHEIGHT)
frame.set_mouseclick_handler(m_click)
frame.set_draw_handler(draw)

bell_reset()
frame.start()
