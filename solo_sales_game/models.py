from otree.api import (
	models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
	Currency as c, currency_range
)
import random
from random import shuffle
import itertools

author = 'Kariyushi'

doc = """
Solo participants play 20-armed bandit game.
"""


class Constants(BaseConstants):
	name_in_url = 'the_sales_game_1A'
	players_per_group = None
	num_rounds = 45
	cnum_rounds = 15

class Subsession(BaseSubsession):
	# all platform dictionaries are pre-populated with a uniform sample of point values from the 
	# medium range [350, 550] 
	def birds_dict(self):
		return [['Canary', 383], ['Cardinal', 486], ['Finch', 523], ['Grackle', 538], ['Jackdaw', 406], 
				['Lark', 475], ['Longspur', 463], ['Magpie', 422], ['Martin', 492], ['Munia', 550],
				['Oriole', 514], ['Pipit', 364], ['Robin', 459], ['Sparrow', 351], ['Starling', 415],
				['Swallow', 507], ['Tanager', 377], ['Thrush', 398], ['Warbler', 439], ['Wren', 444]]

	def spices_dict(self):
		return [['Ajwain', 398], ['Anise', 523], ['Annatto', 422], ['Cardamom', 439], ['Cinnamon', 475],  
				['Cumin', 459], ['Dill', 492], ['Fennel', 463],  ['Fenugreek', 514], ['Galangal', 444],   
				['Ginger', 351], ['Mahleb', 415], ['Mustard', 550], ['Nigella', 538], ['Nutmeg', 383],  
				['Paprika', 507], ['Pepper', 377], ['Saffron', 406], ['Sumac', 364], ['Turmeric', 486]]

	def elements_dict(self):
		return [['Argon', 383], ['Bismuth', 486], ['Bromine', 523], ['Carbon', 538], ['Cobalt', 406],   
				['Copper', 475], ['Gallium', 463], ['Helium', 422], ['Hydrogen', 492], ['Iodine', 550],
				['Iron', 514], ['Mercury', 364], ['Neon', 459], ['Nickel', 351], ['Oxygen', 415],  
				['Tin', 507], ['Radon', 377], ['Rhodium', 398], ['Xenon', 439], ['Zinc', 444]]

	# for Scarcity Condition, substitute these into the elements dictionary; 
	# for Abundance Condition, substitute these into the birds dictionary
	def low_points(self):
		return [133,236,273,288,156,225,213,172,242,300,264,114,209,101,165,257,127,148,189,194]

	# for Scarcity Condition, substitute these into the birds dictionary
	# for Abundance Condition, substitute these into the elements dictionary; 
	def high_points(self):
		return [633,736,773,788,656,725,713,672,742,800,764,614,709,601,665,757,627,648,689,694]

	def med1_points(self):
		return [383,486,523,538,406,475,463,422,492,550,514,364,459,351,415,507,377,398,439,444]

	def med2_points(self):
		return [398,523,422,439,475,459,492,463,514,444,351,415,550,538,383,507,377,406,364,486]


	def creating_session(self):
		print("CREATING ROUND: ", self.round_number)

		for p in self.get_players():
			if self.round_number == 1:
				p.participant.vars['num_timeouts'] = 0 
				p.participant.vars['is_dropout'] = False
				if 'treatment' in self.session.config:
					treatment = self.session.config['treatment']
					p.participant.vars['treatment'] = treatment
					p.treatment = treatment
				else: 
					treatment = p.participant.vars['treatment']
					p.treatment = treatment
			else:
				treatment = p.participant.vars['treatment']
				p.treatment = treatment

			platform_list = []
			points_list = []

			print("PARTICIPANT NO: ", p.id_in_subsession, "CONDITION: ", p.treatment)

			#Phase 1: birds
			if self.round_number < 16:
				# fresh copy of birds dictionary 
				platform_list = self.birds_dict()
				if p.treatment == 'abundance':
					points_list = self.low_points()
				elif p.treatment == 'scarcity':
					points_list = self.high_points()
				else:
					points_list = self.med1_points()
			#Phase 2: spices
			elif self.round_number > 15 and self.round_number < 31:
				# fresh copy of spices dictionary
				platform_list = self.spices_dict()
				points_list = self.med2_points()
			#Phase 3: elements
			else: 
				# fresh copy of elements dictionary
				platform_list = self.elements_dict()
				if p.treatment == 'abundance':
					points_list = self.high_points()
				elif p.treatment == 'scarcity':
					points_list = self.low_points()
				else:
					points_list = self.med1_points()

			# draw point values from normal distro around each platform's mean
			# STANDARD DEVIATION = 20
			for i in range(0, len(platform_list)):
				point_value = round(random.gauss(points_list[i], 20))
				while point_value < 0:
					point_value = round(random.gauss(points_list[i], 20))
				platform_list[i][1] = point_value

			# randomize order of platforms 
			random.shuffle(platform_list)
			p.participant.vars['platforms_list_' + str(self.round_number)] = platform_list

			# flatten nested trees list to string that can be passed to DB
			flattened_list = [",".join([str(pair) for pair in list]) for list in platform_list]
			flattened_list = ','.join(map(str, flattened_list))
			p.p_list_options_values = flattened_list	

class Group(BaseGroup):
	pass

class Player(BasePlayer):
	browser_innerh = models.IntegerField()
	browser_innerw = models.IntegerField()

	treatment = models.StringField()
	is_dropout = models.BooleanField(initial=False)
	num_timeouts = models.IntegerField(initial=0)
	
	# this is just a placeholder value that lets me present a custom
	# error message when the participant doesn't submit exactly 3
	# platforms in their pitch
	stub_msg = models.IntegerField(blank=True)

	def stub_msg_error_message(self, value):
		if value != 99:
			self.numerrors_choosep += 1
			return 'MAKE SURE YOU HAVE EXACTLY THREE (3) PLATFORMS IN YOUR PITCH LIST'

	newcomp_timeout = models.BooleanField(initial=False)
	
	choose_p_timeout = models.BooleanField(initial=False)
	numerrors_choosep = models.IntegerField(initial=0, label="")

	p_list_options_values = models.StringField()
	p_list_selected = models.StringField()
	curr_score = models.IntegerField()
	p_name_0 = models.CharField()
	p_points_0 = models.IntegerField()
	p_name_1 = models.CharField()
	p_points_1 = models.IntegerField()
	p_name_2 = models.CharField()
	p_points_2 = models.IntegerField()

	p_list_best = models.StringField()
	best_score = models.IntegerField()
	best_pname0 = models.CharField()
	best_ppoints0 = models.IntegerField()
	best_pname1 = models.CharField()
	best_ppoints1 = models.IntegerField()
	best_pname2 = models.CharField()
	best_ppoints2 = models.IntegerField()

	company_score = models.IntegerField()
	aggregate_score = models.IntegerField()

	results_timeout = models.BooleanField(initial=False)

	feelcheck_timeout = models.BooleanField(initial=False)
	checkslider_happy = models.IntegerField(blank=True)
	checkslider_frustrated = models.IntegerField(blank=True)
	checkslider_successful = models.IntegerField(blank=True)
	checkslider_friendly = models.IntegerField(blank=True)
	checkslider_hostile = models.IntegerField(blank=True)
	checkslider_anxious = models.IntegerField(blank=True)
	
	feelcheck_happy = models.IntegerField(
		widget=widgets.Slider(attrs={'step': '1.00'},
			show_value=False))

	feelcheck_frustrated = models.IntegerField(
		widget=widgets.Slider(attrs={'step': '1.00'},
			show_value=False))

	feelcheck_successful = models.IntegerField(
		widget=widgets.Slider(attrs={'step': '1.00'},
			show_value=False))

	feelcheck_friendly = models.IntegerField(
		widget=widgets.Slider(attrs={'step': '1.00'},
			show_value=False))

	feelcheck_hostile = models.IntegerField(
		widget=widgets.Slider(attrs={'step': '1.00'},
			show_value=False))

	feelcheck_anxious = models.IntegerField(
		widget=widgets.Slider(attrs={'step': '1.00'},
			show_value=False))

	checkin_timeout = models.BooleanField(initial=False)
	plat1_guess = models.IntegerField(label="")
	plat2_guess = models.IntegerField(label="")
	plat3_guess = models.IntegerField(label="")
	plat4_guess = models.IntegerField(label="")
	plat5_guess = models.IntegerField(label="")
	plat6_guess = models.IntegerField(label="")
	plat7_guess = models.IntegerField(label="")
	plat8_guess = models.IntegerField(label="")
	plat9_guess = models.IntegerField(label="")
	plat10_guess = models.IntegerField(label="")
	plat11_guess = models.IntegerField(label="")
	plat12_guess = models.IntegerField(label="")
	plat13_guess = models.IntegerField(label="")
	plat14_guess = models.IntegerField(label="")
	plat15_guess = models.IntegerField(label="")
	plat16_guess = models.IntegerField(label="")
	plat17_guess = models.IntegerField(label="")
	plat18_guess = models.IntegerField(label="")
	plat19_guess = models.IntegerField(label="")
	plat20_guess = models.IntegerField(label="")

	confidence_timeout = models.BooleanField(initial=False)
	checkslider_confidence = models.IntegerField(blank=True)
	confidence = models.IntegerField(
		widget=widgets.Slider(attrs={'step': '1.00'},
			show_value=False))

	companysummary_timeout = models.BooleanField(initial=False)

	strategy = models.TextField()
	checkslider_selfassessment = models.IntegerField(blank=True)
	selfassessment = models.IntegerField(
		widget=widgets.Slider(attrs={'step': '1.00'},
			show_value=False))
	comments = models.TextField()

	def update_best_score(self):
		start_rounds = [1, 16, 31]
		if self.round_number in start_rounds:
			self.best_score = self.curr_score
		else:
			if self.curr_score >= self.in_round(self.round_number - 1).best_score:
				self.best_score = self.curr_score
			else: 
				self.best_score = self.in_round(self.round_number - 1).best_score

	def update_best_pitch(self):
		start_rounds = [1, 16, 31]
		if self.round_number in start_rounds:
			self.p_list_best = self.p_list_selected
			self.best_pname0 = self.p_name_0
			self.best_ppoints0 = self.p_points_0
			self.best_pname1 = self.p_name_1
			self.best_ppoints1 = self.p_points_1
			self.best_pname2 = self.p_name_2
			self.best_ppoints2 = self.p_points_2
		else:
			if self.curr_score >= self.in_round(self.round_number - 1).best_score:
				self.p_list_best = self.p_list_selected
				self.best_pname0 = self.p_name_0
				self.best_ppoints0 = self.p_points_0
				self.best_pname1 = self.p_name_1
				self.best_ppoints1 = self.p_points_1
				self.best_pname2 = self.p_name_2
				self.best_ppoints2 = self.p_points_2
			else:
				self.p_list_best = self.in_round(self.round_number - 1).p_list_best
				self.best_pname0 = self.in_round(self.round_number - 1).best_pname0
				self.best_ppoints0 = self.in_round(self.round_number - 1).best_ppoints0
				self.best_pname1 = self.in_round(self.round_number - 1).best_pname1
				self.best_ppoints1 = self.in_round(self.round_number - 1).best_ppoints1
				self.best_pname2 = self.in_round(self.round_number - 1).best_pname2
				self.best_ppoints2 = self.in_round(self.round_number - 1).best_ppoints2

	def update_company_score(self):
		start_rounds = [1, 16, 31]
		if self.round_number in start_rounds:
			self.company_score = self.curr_score
		else:
			self.company_score = self.in_round(self.round_number - 1).company_score + self.curr_score

	def update_aggregate_score(self):
		if self.round_number == 1:
			self.aggregate_score = self.curr_score
		else:
			self.aggregate_score = self.in_round(self.round_number - 1).aggregate_score + self.curr_score

	def set_payoff(self):
		self.payoff = self.curr_score
