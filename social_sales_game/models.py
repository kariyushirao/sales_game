from otree.api import (
	models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
	Currency as c, currency_range
)
import random
from random import shuffle
import itertools

author = '© Kariyushi Rao 2022'

doc = """
Groups of 3-6 participants play a 20-armed bandit game with options to share and to view each 
other's choices and results each round.  If participants are left waiting too long to be 
matched into a group, they are allowed to proceed to the solo version of the game. 
"""

class Constants(BaseConstants):
	name_in_url = 'the_sales_game'
	# The maximum number of players that this game can accommodate is 6, and this number cannot
	# be changed in the present version of the program.
	players_per_group = 6
	# The present version of the program has hard-coded event times that assume 45 total trials
	# and 15 trials in each Phase, so these numbers cannot be changed.
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

	# for the Scarcity Condition, these point values will be substituted into the elements dictionary; 
	# for the Abundance Condition, they will be substituted into the birds dictionary
	def low_points(self):
		return [133,236,273,288,156,225,213,172,242,300,264,114,209,101,165,257,127,148,189,194]

	# for the Scarcity Condition, these point values will be substituted into the birds dictionary
	# for the Abundance Condition, they will be substituted into the elements dictionary; 
	def high_points(self):
		return [633,736,773,788,656,725,713,672,742,800,764,614,709,601,665,757,627,648,689,694]

	# for the Control Condition, these point values will be substituted into the birds and elements 
	# dictionaries
	def med1_points(self):
		return [383,486,523,538,406,475,463,422,492,550,514,364,459,351,415,507,377,398,439,444]

	# for all Conditions, these point values will be substituted into the spices dictionary
	def med2_points(self):
		return [398,523,422,439,475,459,492,463,514,444,351,415,550,538,383,507,377,406,364,486]

	# this block of code runs once for each trial at the start of the session - so when you launch
	# the session the program runs through this code block n = Constants.num_rounds times
	def creating_session(self):
		print("CREATING ROUND: ", self.round_number)

		for p in self.get_players():
			if self.round_number == 1:
				p.participant.vars['num_timeouts'] = 0 
				p.participant.vars['is_dropout'] = False
				# in settings.py, you can set up specific versions of the app where the Condition
				# is the same for all participants instead of randomly assigned - this block 
				# checks to see if that's true and assigns the preset Condition if it is present
				if 'treatment' in self.session.config:
					treatment = self.session.config['treatment']
					p.participant.vars['treatment'] = treatment
					p.treatment = treatment
				# if the Condition was not preset in settings.py, this block pulls in the 
				# Condition assigned to the participant in the social_sales_game_instructions app
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

			# draw point values from normal distribution around each platform's mean with
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
	################################################################################
	# List of variables captured in the app database for each player on each trial #
	################################################################################

	# records Condition to which the participant is assigned
	treatment = models.StringField()

	# indicates whether participant was sent to the solo version of the game
	soloplayer = models.BooleanField(initial=False)

	# tracks the realized point value assigned to each platform on each trial
	p_list_options_values = models.StringField()

	# captures the three platforms the participant selected on each trial
	p_list_selected = models.StringField()

	# captures the sum of the points earned on the current trial
	curr_score = models.IntegerField()

	# this block of variables captures the name and realized point value of
	# each platform selected on the current trial
	p_name_0 = models.CharField()
	p_points_0 = models.IntegerField()
	p_name_1 = models.CharField()
	p_points_1 = models.IntegerField()
	p_name_2 = models.CharField()
	p_points_2 = models.IntegerField()

	# this block of variables captures the name and realized point value of
	# the three platforms selected on the trial with the highest total
	# point value (sum of the realized point values for the 3 chosen platforms)
	p_list_best = models.StringField()
	best_score = models.IntegerField()
	best_pname0 = models.CharField()
	best_ppoints0 = models.IntegerField()
	best_pname1 = models.CharField()
	best_ppoints1 = models.IntegerField()
	best_pname2 = models.CharField()
	best_ppoints2 = models.IntegerField()

	# tracks the running cumulative points earned for the current Phase
	# of the experiment
	company_score = models.IntegerField()

	# tracks the running cumulative points earned across all three 
	# Phases of the experiment
	aggregate_score = models.IntegerField()
	
	# this block counts the number of times the participant clicks on each of their peers 
	# to reveal the platforms and point values that peer earned on the previous trial
	alter1_clicks = models.IntegerField()
	alter2_clicks = models.IntegerField()
	alter3_clicks = models.IntegerField()
	alter4_clicks = models.IntegerField()
	alter5_clicks = models.IntegerField()

	# This block captures whether the participant chose to share the results of the
	# current trial with each peer
	alter1_share = models.BooleanField(choices=[[True, "YES, SHARE"], [False, "NO, DON'T SHARE"]],
		widget=widgets.RadioSelect, label="")
	alter2_share = models.BooleanField(choices=[[True, "YES, SHARE"], [False, "NO, DON'T SHARE"]],
		widget=widgets.RadioSelect, label="")
	alter3_share = models.BooleanField(choices=[[True, "YES, SHARE"], [False, "NO, DON'T SHARE"]],
		widget=widgets.RadioSelect, label="")
	alter4_share = models.BooleanField(choices=[[True, "YES, SHARE"], [False, "NO, DON'T SHARE"]],
		widget=widgets.RadioSelect, label="")
	alter5_share = models.BooleanField(choices=[[True, "YES, SHARE"], [False, "NO, DON'T SHARE"]],
		widget=widgets.RadioSelect, label="")
	
	# This block captures whether each of the participant's peers chose to share
	# the results of the current trial with the participant
	alter1_recd = models.BooleanField(initial=False)
	alter2_recd = models.BooleanField(initial=False)
	alter3_recd = models.BooleanField(initial=False)
	alter4_recd = models.BooleanField(initial=False)
	alter5_recd = models.BooleanField(initial=False)

	# This block captures participants' responses to the Feelcheck.html page
	feelcheck_happy = models.IntegerField(widget=widgets.Slider(attrs={'step': '1.00'}, show_value=False))
	feelcheck_frustrated = models.IntegerField(widget=widgets.Slider(attrs={'step': '1.00'}, show_value=False))
	feelcheck_successful = models.IntegerField(widget=widgets.Slider(attrs={'step': '1.00'}, show_value=False))
	feelcheck_friendly = models.IntegerField(widget=widgets.Slider(attrs={'step': '1.00'}, show_value=False))
	feelcheck_hostile = models.IntegerField(widget=widgets.Slider(attrs={'step': '1.00'}, show_value=False))
	feelcheck_anxious = models.IntegerField(widget=widgets.Slider(attrs={'step': '1.00'}, show_value=False))

	# This block captures participants' estimates of each platform value
	# collected on the CheckIn.html page
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

	# This is the confidence rating collected on the Confidence.html page 
	confidence = models.IntegerField(
		widget=widgets.Slider(attrs={'step': '1.00'},
			show_value=False))

	# These variables capture responses to the final questionnaire on Debrief.html
	selfassessment = models.IntegerField(
		widget=widgets.Slider(attrs={'step': '1.00'},
			show_value=False))
	alter1_help = models.IntegerField(widget=widgets.Slider(attrs={'step': '1.00'}, show_value=False))
	alter2_help = models.IntegerField(widget=widgets.Slider(attrs={'step': '1.00'}, show_value=False))
	alter3_help = models.IntegerField(widget=widgets.Slider(attrs={'step': '1.00'}, show_value=False))
	alter4_help = models.IntegerField(widget=widgets.Slider(attrs={'step': '1.00'}, show_value=False))
	alter5_help = models.IntegerField(widget=widgets.Slider(attrs={'step': '1.00'}, show_value=False))
	strategy = models.TextField()
	comments = models.TextField()


	########### THIS BLOCK TRACKS PAGE TIME OUTS #############
	# Total num times participant allowed a page to time out
	num_timeouts = models.IntegerField(initial=0)
	# Matched.html time out
	matched_timeout = models.BooleanField()
	# NewCompany.html time out
	newcomp_timeout = models.BooleanField(initial=False)
	# ChoosePlatforms.html time out
	choose_p_timeout = models.BooleanField(initial=False)
	# CheckIn.html time out
	checkin_timeout = models.BooleanField(initial=False)
	# Confidence.html time out
	confidence_timeout = models.BooleanField(initial=False)
	# CompanySummary.html time out
	companysummary_timeout = models.BooleanField(initial=False)
	results_timeout = models.BooleanField(initial=False)
	feelcheck_timeout = models.BooleanField(initial=False)

	# Marks participant as a dropout if they exceed the time out threshold
	is_dropout = models.BooleanField(initial=False)


	# These are indicators that track whether the participant interacted
	# with each form input slider.  This allows me to display error messages
	# if the participant fails to enter their response on a given slider.
	checkslider_confidence = models.IntegerField(blank=True)
	checkslider_selfassessment = models.IntegerField(blank=True)
	checkslider_alter1_help = models.IntegerField(blank=True)
	checkslider_alter2_help = models.IntegerField(blank=True)
	checkslider_alter3_help = models.IntegerField(blank=True)
	checkslider_alter4_help = models.IntegerField(blank=True)
	checkslider_alter5_help = models.IntegerField(blank=True)
	checkslider_happy = models.IntegerField(blank=True)
	checkslider_frustrated = models.IntegerField(blank=True)
	checkslider_successful = models.IntegerField(blank=True)
	checkslider_friendly = models.IntegerField(blank=True)
	checkslider_hostile = models.IntegerField(blank=True)
	checkslider_anxious = models.IntegerField(blank=True)
	

	# counter that tracks number of times participant tried to submit a pitch with 
	# fewer or more than 3 platforms
	numerrors_choosep = models.IntegerField(initial=0, label="")

	# this is a placeholder value that lets me present a custom error message when the
	# participant doesn't submit exactly 3 platforms in their pitch
	stub_msg = models.IntegerField(blank=True)


	###########################################################################
	# Player model functions that define in-game processes called in views.py #
	###########################################################################
	def stub_msg_error_message(self, value):
		if value != 99:
			self.numerrors_choosep += 1
			return 'MAKE SURE YOU HAVE EXACTLY THREE (3) PLATFORMS IN YOUR PITCH LIST'

	# MAX TIME BEFORE ASSIGNED TO GROUP >=3 - CURRENTLY SET TO 8 MINUTES
	def waiting_too_long(self):
		import time
		return time.time() - self.participant.vars['wait_page_arrival'] >= 8*60

	# MAX TIME BEFORE SENT TO SOLO GAME - CURRENTLY SET TO 10 MINUTES
	def time_to_go(self):
		import time
		return time.time() - self.participant.vars['wait_page_arrival'] >= 10*60

	def update_alter_ids(self):
		alter1_id = 0
		alter2_id = 0
		alter3_id = 0
		alter4_id = 0
		alter5_id = 0

		if self.participant.vars['groupsize'] < 3:
			pass
		elif self.participant.vars['groupsize'] == 3:
			alter1_id = self.get_others_in_group()[0].id_in_group
			alter2_id = self.get_others_in_group()[1].id_in_group
		elif self.participant.vars['groupsize'] == 4:
			alter1_id = self.get_others_in_group()[0].id_in_group
			alter2_id = self.get_others_in_group()[1].id_in_group
			alter3_id = self.get_others_in_group()[2].id_in_group
		elif self.participant.vars['groupsize'] == 5:
			alter1_id = self.get_others_in_group()[0].id_in_group
			alter2_id = self.get_others_in_group()[1].id_in_group
			alter3_id = self.get_others_in_group()[2].id_in_group
			alter4_id = self.get_others_in_group()[3].id_in_group
		else:
			alter1_id = self.get_others_in_group()[0].id_in_group
			alter2_id = self.get_others_in_group()[1].id_in_group
			alter3_id = self.get_others_in_group()[2].id_in_group
			alter4_id = self.get_others_in_group()[3].id_in_group
			alter5_id = self.get_others_in_group()[4].id_in_group

		self.participant.vars['alter1_id'] = alter1_id
		self.participant.vars['alter2_id'] = alter2_id
		self.participant.vars['alter3_id'] = alter3_id
		self.participant.vars['alter4_id'] = alter4_id
		self.participant.vars['alter5_id'] = alter5_id

	def update_share_decisions(self):
		if self.participant.vars['groupsize'] == 3:
			self.alter3_share = False
			self.alter4_share = False
			self.alter5_share = False
		elif self.participant.vars['groupsize'] == 4:
			self.alter4_share = False
			self.alter5_share = False
		elif self.participant.vars['groupsize'] == 5:
			self.alter5_share = False

		alter1_id = self.participant.vars['alter1_id']
		alter2_id = self.participant.vars['alter2_id']
		alter3_id = self.participant.vars['alter3_id']
		alter4_id = self.participant.vars['alter4_id']
		alter5_id = self.participant.vars['alter5_id']

		alter1_share = self.alter1_share
		alter2_share = self.alter2_share
		alter3_share = self.alter3_share
		alter4_share = self.alter4_share
		alter5_share = self.alter5_share

		self.participant.vars['share_decisions'] = {alter1_id: alter1_share, alter2_id: alter2_share, 
													alter3_id: alter3_share, alter4_id: alter4_share, 
													alter5_id: alter5_share}

	def who_shared_with_me(self):
		alter1_id = self.participant.vars['alter1_id']
		alter2_id = self.participant.vars['alter2_id']
		alter3_id = self.participant.vars['alter3_id']
		alter4_id = self.participant.vars['alter4_id']
		alter5_id = self.participant.vars['alter5_id']

		alter1_sent = False
		alter2_sent = False
		alter3_sent = False
		alter4_sent = False
		alter5_sent = False

		if self.participant.vars['groupsize'] < 3:
			pass
		elif self.participant.vars['groupsize'] == 3:
			alter1_sent = self.group.get_player_by_id(alter1_id).participant.vars['share_decisions'][self.id_in_group] 
			alter2_sent = self.group.get_player_by_id(alter2_id).participant.vars['share_decisions'][self.id_in_group]
		elif self.participant.vars['groupsize'] == 4:
			alter1_sent = self.group.get_player_by_id(alter1_id).participant.vars['share_decisions'][self.id_in_group] 
			alter2_sent = self.group.get_player_by_id(alter2_id).participant.vars['share_decisions'][self.id_in_group]
			alter3_sent = self.group.get_player_by_id(alter3_id).participant.vars['share_decisions'][self.id_in_group] 
		elif self.participant.vars['groupsize'] == 5:
			alter1_sent = self.group.get_player_by_id(alter1_id).participant.vars['share_decisions'][self.id_in_group] 
			alter2_sent = self.group.get_player_by_id(alter2_id).participant.vars['share_decisions'][self.id_in_group]
			alter3_sent = self.group.get_player_by_id(alter3_id).participant.vars['share_decisions'][self.id_in_group] 
			alter4_sent = self.group.get_player_by_id(alter4_id).participant.vars['share_decisions'][self.id_in_group] 
		else:
			alter1_sent = self.group.get_player_by_id(alter1_id).participant.vars['share_decisions'][self.id_in_group] 
			alter2_sent = self.group.get_player_by_id(alter2_id).participant.vars['share_decisions'][self.id_in_group]
			alter3_sent = self.group.get_player_by_id(alter3_id).participant.vars['share_decisions'][self.id_in_group] 
			alter4_sent = self.group.get_player_by_id(alter4_id).participant.vars['share_decisions'][self.id_in_group] 
			alter5_sent = self.group.get_player_by_id(alter5_id).participant.vars['share_decisions'][self.id_in_group] 

		alter1_recd = False
		alter2_recd = False
		alter3_recd = False
		alter4_recd = False
		alter5_recd = False

		if alter1_sent == True and self.alter1_share == True:
				alter1_recd = True
		if alter2_sent == True and self.alter2_share == True:
				alter2_recd = True
		if alter3_sent == True and self.alter3_share == True:
				alter3_recd = True
		if alter4_sent == True and self.alter4_share == True:
				alter4_recd = True
		if alter5_sent == True and self.alter5_share == True:
				alter5_recd = True

		self.alter1_recd = alter1_recd
		self.alter2_recd = alter2_recd
		self.alter3_recd = alter3_recd
		self.alter4_recd = alter4_recd
		self.alter5_recd = alter5_recd

	def get_alter_results(self):
		alter_results = {'alter1': {'id': self.participant.vars['alter1_id'], 
								 'recd': self.in_round(self.round_number - 1).alter1_recd, 
								 'score': 0, 'pname0': '', 'ppoints0': 0,
								 'pname1': '', 'ppoints1': 0, 'pname2': '', 'ppoints2': 0},
						'alter2': {'id': self.participant.vars['alter2_id'], 
								 'recd': self.in_round(self.round_number - 1).alter2_recd, 
								 'score': 0, 'pname0': '', 'ppoints0': 0,
								 'pname1': '', 'ppoints1': 0, 'pname2': '', 'ppoints2': 0},
						'alter3': {'id': self.participant.vars['alter3_id'], 
								 'recd': self.in_round(self.round_number - 1).alter3_recd, 
								 'score': 0, 'pname0': '', 'ppoints0': 0,
								 'pname1': '', 'ppoints1': 0, 'pname2': '', 'ppoints2': 0},
						'alter4': {'id': self.participant.vars['alter4_id'], 
								 'recd': self.in_round(self.round_number - 1).alter4_recd, 
								 'score': 0, 'pname0': '', 'ppoints0': 0,
								 'pname1': '', 'ppoints1': 0, 'pname2': '', 'ppoints2': 0},
						'alter5': {'id': self.participant.vars['alter5_id'], 
								 'recd': self.in_round(self.round_number - 1).alter5_recd, 
								 'score': 0, 'pname0': '', 'ppoints0': 0,
								 'pname1': '', 'ppoints1': 0, 'pname2': '', 'ppoints2': 0}}

		for alter in alter_results:
			if alter_results[alter]['recd'] == True:
				lr_player = self.group.get_player_by_id(alter_results[alter]['id']).in_round(self.round_number - 1)
				alter_results[alter]['score'] = lr_player.curr_score
				alter_results[alter]['pname0'] = lr_player.p_name_0
				alter_results[alter]['ppoints0'] = lr_player.p_points_0
				alter_results[alter]['pname1'] = lr_player.p_name_1
				alter_results[alter]['ppoints1'] = lr_player.p_points_1
				alter_results[alter]['pname2'] = lr_player.p_name_2
				alter_results[alter]['ppoints2'] = lr_player.p_points_2

		return alter_results


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

	# capture points earned on the current trial for payment calculation
	def set_payoff(self):
		self.payoff = self.curr_score

	
	
	
