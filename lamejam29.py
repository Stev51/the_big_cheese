'''
THE BIG CHEESE
Lame Jam 29 entry
a0.1
'''

import simpleguitk as simplegui
import math, random

#Initial sound load gets the pygame message out of the way of the console
snd_garbage = simplegui.load_sound("https://www.dropbox.com/s/xu9tpeuukbphta5/xray.mp3?dl=1")

print("Started loading.")

# Constants
FWIDTH = 1120
FHEIGHT = 630
FWC = FWIDTH/2
FHC = FHEIGHT/2
BACKGROUND_COLOR = "Grey"
GUI_WIDTH = 5
GUI_COLOR = "Silver"
SQUARE_COLOR = "DimGrey"
BUTTON_COLOR = "Silver"
GUI_ROOF_HEIGHT = 175
GUI_SQUARE_SIZE = 400

X_BUF = (FWC - GUI_SQUARE_SIZE) / 2
Y_BUF = (FHEIGHT - GUI_ROOF_HEIGHT - GUI_SQUARE_SIZE) / 2
TYCOON_POINTS = [(X_BUF, GUI_ROOF_HEIGHT + Y_BUF), (FWC - X_BUF, GUI_ROOF_HEIGHT + Y_BUF), (FWC - X_BUF, GUI_ROOF_HEIGHT + Y_BUF + 380), (X_BUF, GUI_ROOF_HEIGHT + Y_BUF + 380)]
PIZZA_POINTS = [(FWC + X_BUF, GUI_ROOF_HEIGHT + Y_BUF), (FWIDTH - X_BUF, GUI_ROOF_HEIGHT + Y_BUF), (FWIDTH - X_BUF, FHEIGHT - Y_BUF), (FWC + X_BUF, FHEIGHT - Y_BUF)]
PW0 = PIZZA_POINTS[0][0]
PW1 = PIZZA_POINTS[1][0]
PWC = (GUI_SQUARE_SIZE / 2) + PW0
PH0 = PIZZA_POINTS[0][1]
PH1 = PIZZA_POINTS[3][1]
PHC = (GUI_SQUARE_SIZE / 2) + PH0

STARTING_MONEY = 10
INCOME_TIME = 60

GOON_INCREASE = 10
GEFF_INCREASE = 10
PIZZA_INCREASE = 1

BREAK_TIME = 120
ORDER_TIME = 299
PIZZA_BASE_REWARD = 15

# Normal variables
timerIncome = 0
flag_business = False
flag_mute = True

money = STARTING_MONEY
goons = 0
goon_efficiency = 1
pizza_multiplier = 1

goon_price = 10
geff_price = 15
business_price = 10
pizza_price = 1

pizza_gamestate = 0
score = 0
timer_break = BREAK_TIME
timer_order = ORDER_TIME
ordered_pizza = [0, 0, 0, 0, 0, 0]
player_pizza = [0, 0, 0, 0, 0, 0]
dummy_list = [0, 1, 2, 3, 4, 5]

# Graphic resources
print("Loading graphic resources...")
img_logo = simplegui.load_image("https://i.imgur.com/XfUa7qn.png")
img_labelDough = simplegui.load_image("https://i.imgur.com/6bhPqYx.png")
img_labelGoons = simplegui.load_image("https://i.imgur.com/05i317b.png")
img_labelCrime = simplegui.load_image("https://i.imgur.com/Q2KlutF.png")
img_labelBusiness = simplegui.load_image("https://i.imgur.com/hxIpu4B.png")
img_sign = simplegui.load_image("https://i.imgur.com/xczaKmo.png")
img_buttonGoon = simplegui.load_image("https://i.imgur.com/sjOPe4h.png")
img_buttonRestaurant = simplegui.load_image("https://i.imgur.com/NmhRRrx.png")
img_buttonEvil = simplegui.load_image("https://i.imgur.com/P6MhUa2.png")
img_pizzaBase = simplegui.load_image("https://i.imgur.com/PtfNkX6.png")
img_iconCheese = simplegui.load_image("https://i.imgur.com/905s2A2.png")
img_iconPepp = simplegui.load_image("https://i.imgur.com/7lAReNE.png")
img_iconMush = simplegui.load_image("https://i.imgur.com/sLMn507.png")
img_iconOlive = simplegui.load_image("https://i.imgur.com/oPJ652R.png")
img_iconBacon = simplegui.load_image("https://i.imgur.com/Rh1Whqc.png")
img_iconBanana = simplegui.load_image("https://i.imgur.com/mcOafIh.png")
img_bell1 = simplegui.load_image("https://i.imgur.com/9V4WWAE.png")
img_bell2 = simplegui.load_image("https://i.imgur.com/jhqd84B.png")
img_bannerBase = simplegui.load_image("https://i.imgur.com/RcG2EdD.png")
img_animSmoke1 = simplegui.load_image("https://i.imgur.com/oyRaeNc.png")
img_animSmoke2 = simplegui.load_image("https://i.imgur.com/ugknTYL.png")
img_goon1 = simplegui.load_image("https://i.imgur.com/6s1MP1Y.png")
img_goon2 = simplegui.load_image("https://i.imgur.com/s6Dk0TO.png")
img_goon3 = simplegui.load_image("https://i.imgur.com/2f9e988.png")

print("Done.")

# Audio resources
print("Loading sound resources...")
###
print("Done.")
sounds = [(snd_garbage, 0.1)]

# Toggle sound method
def mute():
	global flag_mute
	flag_mute = not flag_mute
	if flag_mute == True:
		for sound in sounds:
			sound[0].set_volume(0)
	else:
		for sound in sounds:
			sound[0].set_volume(sound[1])

# Crime button methods
def buy_goon():
	global money, goons, goon_price
	if money >= goon_price:
		money -= goon_price
		goons += 1
		goon_price += GOON_INCREASE

def buy_goon_efficiency():
	global money, goon_efficiency, geff_price
	if money >= geff_price:
		money -= geff_price
		goon_efficiency += 1
		geff_price += GEFF_INCREASE

def buy_business():
	global money, flag_business
	if money >= business_price and flag_business == False:
		flag_business = True
		money -= business_price
		bell_reset() #<-- Don't know if we need this

def buy_pizza_efficiency():
	global goons, pizza_multiplier, pizza_price
	if goons > pizza_price:
		goons -= pizza_price
		pizza_multiplier += 1
		pizza_price += PIZZA_INCREASE

# Pizza game bell method
def bell_reset():
	global pizza_gamestate, timer_break, player_pizza, ordered_pizza, toppings, score, money
	
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
	money += int(score)
	
	pizza_gamestate = 0
	timer_break = BREAK_TIME
	player_pizza = [0, 0, 0, 0, 0, 0]
	ordered_pizza = [0, 0, 0, 0, 0, 0]
	
	toppings = random.sample(dummy_list, 3)
	for i in toppings:
		ordered_pizza[i] = 1

# Mouse handler
def m_click(pos):
	global player_pizza
	
	if pos[0] >= TYCOON_POINTS[0][0] + 20 and pos[0] <= TYCOON_POINTS[0][0] + GUI_SQUARE_SIZE/2 - 10:
		if pos[1] >= TYCOON_POINTS[0][1] + 20 and pos[1] <= TYCOON_POINTS[0][1] + 60:
			buy_goon()
		elif pos[1] >= TYCOON_POINTS[0][1] + 80 and pos[1] <= TYCOON_POINTS[0][1] + 120:
			buy_goon_efficiency()
	elif pos[0] >= TYCOON_POINTS[1][0] - GUI_SQUARE_SIZE/2 + 10 and pos[0] <= TYCOON_POINTS[1][0] - 20:
		if pos[1] >= TYCOON_POINTS[1][1] + 20 and pos[1] <= TYCOON_POINTS[1][1] + 60:
			buy_business()
		elif pos[1] >= TYCOON_POINTS[1][1] + 80 and pos[1] <= TYCOON_POINTS[1][1] + 120:
			buy_pizza_efficiency()
	
	if flag_business == True:
		if pizza_gamestate == 1:
			if pos[1] >= PH1 - 140 and pos[1] <= PH1 - 90:
				if pos[0] >= PW0 + 20 and pos[0] <= PW0 + 70:
					player_pizza[0] = 1
				elif pos[0] >= PW0 + 90 and pos[0] <= PW0 + 140:
					player_pizza[1] = 1
				elif pos[0] >= PW0 + 160 and pos[0] <= PW0 + 210:
					player_pizza[2] = 1
			elif pos[1] >= PH1 - 70 and pos[1] <= PH1 - 20:
				if pos[0] >= PW0 + 20 and pos[0] <= PW0 + 70:
					player_pizza[3] = 1
				elif pos[0] >= PW0 + 90 and pos[0] <= PW0 + 140:
					player_pizza[4] = 1
				elif pos[0] >= PW0 + 160 and pos[0] <= PW0 + 210:
					player_pizza[5] = 1
			elif (pos[0] >= PW0 + 20 and pos[0] <= PW0 + 70) and (pos[1] >= PH1 - 210 and pos[1] <= PH1 - 160):
				if pizza_gamestate == 1:
					bell_reset()

# Draw handler
def draw(canvas):
	global money, timerIncome, pizza_gamestate, timer_break, timer_order
	
	# Manage money/income
	timerIncome += 1
	if timerIncome >= INCOME_TIME:
		money += goons * goon_efficiency
		timerIncome = 0
	
	# Banner graphics
	canvas.draw_image(img_bannerBase, (560, 87.5), (1120, 175), (FWC, 87), (1120, 175))
	
	if timerIncome >= INCOME_TIME/2:
		canvas.draw_image(img_animSmoke1, (42.5, 42.5), (85, 85), (500, 90), (85, 85))
	else:
		canvas.draw_image(img_animSmoke2, (42.5, 42.5), (85, 85), (500, 90), (85, 85))
	
	# Tycoon GUI
	canvas.draw_polygon(TYCOON_POINTS, 1, SQUARE_COLOR, SQUARE_COLOR)
	
	canvas.draw_image(img_buttonGoon, (125, 20), (250, 40), (185, 243), (170, 40))
	canvas.draw_text("Buy Goon - " + str(goon_price), (100, 263), 12, "White")
	
	canvas.draw_image(img_buttonGoon, (125, 20), (250, 40), (185, 303), (170, 40))
	canvas.draw_text("Upgrade Goons - " + str(geff_price), (100, 323), 12, "White")
	
	canvas.draw_image(img_buttonEvil, (125, 20), (250, 40), (185, 363), (170, 40))
	canvas.draw_image(img_buttonEvil, (125, 20), (250, 40), (185, 423), (170, 40))
	canvas.draw_image(img_buttonEvil, (125, 20), (250, 40), (185, 483), (170, 40))
	canvas.draw_image(img_buttonEvil, (125, 20), (250, 40), (185, 543), (170, 40))
	
	canvas.draw_image(img_buttonRestaurant, (125, 20), (250, 40), (375, 243), (170, 40))
	if flag_business == False:
		canvas.draw_text("Purchase Legitimate Business - " + str(business_price), (290, 263), 12, "White")
	else:
		canvas.draw_text("---", (290, 263), 12, "White")
	
	canvas.draw_image(img_buttonRestaurant, (125, 20), (250, 40), (375, 303), (170, 40))
	canvas.draw_text("Upgrade Restaurant - " + str(pizza_price), (290, 323), 12, "White")
	
	canvas.draw_image(img_buttonEvil, (125, 20), (250, 40), (375, 363), (170, 40))
	canvas.draw_image(img_buttonEvil, (125, 20), (250, 40), (375, 423), (170, 40))
	canvas.draw_image(img_buttonEvil, (125, 20), (250, 40), (375, 483), (170, 40))
	canvas.draw_image(img_buttonEvil, (125, 20), (250, 40), (375, 543), (170, 40))
	
	# Pizzatron code
	if flag_business == True:
		
		# Timer logic
		if pizza_gamestate == 0:
			timer_break -= 1
			if timer_break <= 0:
				pizza_gamestate = 1
				timer_order = ORDER_TIME
		elif pizza_gamestate == 1:
			if timer_order > 0:
				timer_order -= 1
		else:
			print("ERROR: Broken pizza_gamestate for pizza minigame, defaulting to state 0")
			pizza_gamestate = 0
		
		# Base
		canvas.draw_image(img_pizzaBase, (200, 200), (400, 400), (PWC, PHC), (400, 400))
		
		# Buttons
		canvas.draw_polygon([(660, 463), (710, 463), (710, 513), (660, 513)], 1, BUTTON_COLOR, BUTTON_COLOR)
		canvas.draw_polygon([(730, 463), (780, 463), (780, 513), (730, 513)], 1, BUTTON_COLOR, BUTTON_COLOR)
		canvas.draw_polygon([(800, 463), (850, 463), (850, 513), (800, 513)], 1, BUTTON_COLOR, BUTTON_COLOR)
		canvas.draw_polygon([(660, 533), (710, 533), (710, 583), (660, 583)], 1, BUTTON_COLOR, BUTTON_COLOR)
		canvas.draw_polygon([(730, 533), (780, 533), (780, 583), (730, 583)], 1, BUTTON_COLOR, BUTTON_COLOR)
		canvas.draw_polygon([(800, 533), (850, 533), (850, 583), (800, 583)], 1, BUTTON_COLOR, BUTTON_COLOR)
		
		# Pizza button labels
		# Also temp pizza contents
		canvas.draw_image(img_iconCheese, (50, 50), (100, 100), (685, 488), (50, 50))
		canvas.draw_image(img_iconPepp, (50, 50), (100, 100), (755, 488), (50, 50))
		canvas.draw_image(img_iconMush, (50, 50), (100, 100), (825, 488), (50, 50))
		canvas.draw_image(img_iconOlive, (50, 50), (100, 100), (685, 558), (50, 50))
		canvas.draw_image(img_iconBacon, (50, 50), (100, 100), (755, 558), (50, 50))
		canvas.draw_image(img_iconBanana, (50, 50), (100, 100), (825, 558), (50, 50))
		canvas.draw_text(str(player_pizza), (650, 323), 20, "White") #<-- Temporary
		
		# Bell
		if pizza_gamestate == 1:
			canvas.draw_image(img_bell2, (25, 25), (50, 50), (685, 418), (50, 50))
		else:
			canvas.draw_image(img_bell1, (25, 25), (50, 50), (685, 418), (50, 50))
		
		# Order display
		if pizza_gamestate == 1 and timer_order > 0:
			canvas.draw_text(str(math.floor(timer_order/60)+1), (650, 243), 20, "White")
			canvas.draw_text(str(ordered_pizza), (650, 283), 20, "White")
		
		# Final result display
		if pizza_gamestate == 0:
			canvas.draw_text("You earned $" + str(round(score)) + "!", (650, 283), 20, "White")
	
	else:
		canvas.draw_image(img_sign, (100, 100), (200, 200), (PWC, PHC), (200, 200))
	
	# Meta GUI
	canvas.draw_line((0, GUI_ROOF_HEIGHT), (FWIDTH, GUI_ROOF_HEIGHT), GUI_WIDTH, GUI_COLOR)
	canvas.draw_line((0, FHEIGHT), (FWIDTH, FHEIGHT), GUI_WIDTH, GUI_COLOR)
	
	canvas.draw_polygon(TYCOON_POINTS, GUI_WIDTH, GUI_COLOR)
	canvas.draw_polygon(PIZZA_POINTS, GUI_WIDTH, GUI_COLOR)
	
	canvas.draw_image(img_labelCrime, (94, 14), (188, 28), (174, 189), (188, 28))
	canvas.draw_image(img_labelBusiness, (94, 14), (188, 28), (970, 189), (188, 28))
	
	canvas.draw_image(img_labelDough, (125, 75), (250, 150), (75, 45), (150, 90))
	canvas.draw_polygon([(137, 22), (151 + frame.get_canvas_textwidth(str(money), 24), 22), (151 + frame.get_canvas_textwidth(str(money), 24), 66), (137, 66)], 1, "Black", "Black")
	canvas.draw_polygon([(141, 26), (147 + frame.get_canvas_textwidth(str(money), 24), 26), (147 + frame.get_canvas_textwidth(str(money), 24), 62), (141, 62)], 1, "White", "White")
	canvas.draw_text(str(money), (144, 62), 24, "Black")
	
	canvas.draw_image(img_labelGoons, (125, 75), (250, 150), (1045, 45), (150, 90))
	canvas.draw_polygon([(950 - frame.get_canvas_textwidth(goons, 24), 22), (964, 22), (964, 66), (950 - frame.get_canvas_textwidth(goons, 24), 66)], 1, "Black", "Black")
	canvas.draw_polygon([(954 - frame.get_canvas_textwidth(goons, 24), 26), (960, 26), (960, 62), (954 - frame.get_canvas_textwidth(goons, 24), 62)], 1, "White", "White")
	canvas.draw_text(str(goons), (957 - frame.get_canvas_textwidth(goons, 24), 62), 24, "Black")
	
	canvas.draw_text("Pizza Earnings: $" + str(pizza_multiplier * PIZZA_BASE_REWARD) + "/P", (10, 120), 16, "White")
	
	tempeff = "Goon Efficiency: $" + str(goon_efficiency) + "/s"
	canvas.draw_text(tempeff, (1110 - frame.get_canvas_textwidth(tempeff, 16), 120), 16, "White")

# Game frame setup
frame = simplegui.create_frame("The Big Cheese", FWIDTH, FHEIGHT)
frame.set_canvas_background(BACKGROUND_COLOR)
frame.set_mouseclick_handler(m_click)
frame.set_draw_handler(draw)

for i in range(25):
	frame.add_label("")
frame.add_label("↓ Ignore this stuff ↓")

print("Done loading, starting game.")

mute()
frame.start()
