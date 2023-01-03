from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
from collections import defaultdict

import random
from random import shuffle

class ArrivalWaitPage(WaitPage):
	def is_displayed(self):
		return self.round_number == 1

	template_name = 'social_sales_game/ArrivalWaitPage.html'

	group_by_arrival_time = True

	def get_players_for_group(self, waiting_players):
		# Print statements are sent to the terminal if you are running the program from
		# your local machine.  If you are running the program from a cloud server, these
		# print statements are recorded in the server log.  They can be removed or altered
		# as desired and just serve as a tool to help debug code and also to monitor live
		# sessions.
		print("STARTING GET PLAYERS FOR GROUP")

		# this is a dictionary that will hold the lists of participants assigned to each
		# Condition 
		d = defaultdict(list)

		# otree's built-in WaitPage functions recognize that 'waiting_players' is a list
		# of participants who are active on the WaitPage 
		for p in waiting_players:
			# identify the Condition assigned to the current participant in the 
			# 'social_sales_game_instructions' app
			treatment = p.participant.vars['treatment']
			# append the current participant to the list of waiting participants
			# assigned to the same Condition
			players_in_treatment = d[treatment]
			players_in_treatment.append(p)

		# for each Condition in the dictionary that holds the lists of participants assigned
		# to each Condition
		for treatment in d:
			players_in_treatment = d[treatment]
			print("CONDITION", treatment, "PLAYERS IN CONDITION", players_in_treatment)

			# The waiting_too_long function is defined in the Player block of models.py
			# and keeps track of how long a participant has been waiting to be matched
			# to a group. The 'wtl' list keeps track of all the waiting participants who
			# have exceeded the maximum wait time thresholds.
			wtl = [p for p in players_in_treatment if p.waiting_too_long()]
			print("WAITING TOO LONG", wtl)

			# if there are at least 6 waiting participants who share the present Condition,
			# they are assigned to a group together 
			if len(players_in_treatment) >= 6:
				newgroup = players_in_treatment[:6]
				print('FORMING GROUP', newgroup)
				for p in newgroup:
					p.participant.vars['groupsize'] = len(newgroup)
				return newgroup

			# if at least one participant has exceeded the maximum wait time for 6-person  
			# group matching, and there are at least two other participants who share that
			# participant's Condition, they are assigned to a group together
			elif len(wtl) >= 1 and len(players_in_treatment) >=3:
				newgroup = players_in_treatment
				print('FORMING GROUP', newgroup)
				for p in newgroup:
					p.participant.vars['groupsize'] = len(newgroup)
				return newgroup

		# if any waiting players have exceeded the maximum wait time for smaller group
		# matching, they are allowed to proceed to the solo version of the experiment
		for p in waiting_players:
			if p.time_to_go():
				p.soloplayer = True
				p.participant.vars['groupsize'] = 1
				print('PLAYING SOLO', p.id_in_subsession, p.participant.code, p.treatment)
				return [p]

	# each time a group is formed, a summary of the group assignment is printed to the terminal 
	# and the IDs of each participant's peers are recorded in that participant's variables
	def after_all_players_arrive(self):
		print('PLAYERS IN GROUP ', self.group.id_in_subsession)
		for p in self.group.get_players():
			print('PLAYER NO ', p.id_in_group, 'SUB NO', p.id_in_subsession, 'CODE', p.participant.code)
			# the 'update_alter_ids' function is defined in the Player block of models.py
			p.update_alter_ids()

class SoloPlayer(Page):
	# if a participants is sent to the solo version of the experiment, they are shown this
	# information page that explains what happened
	def is_displayed(self):
		return self.round_number == 1 and self.player.soloplayer == True

class Matched(Page):
	def is_displayed(self):
		return self.round_number == 1 and self.player.soloplayer == False

	timeout_seconds = 20

	def vars_for_template(self):
		return{'playerid': self.player.id_in_group, 'groupsize': self.participant.vars['groupsize'] - 1}

	def before_next_page(self):
		if self.timeout_happened:
			self.player.matched_timeout = True

class NewCompany(Page):
	def is_displayed(self):
		start_rounds = [1, 16, 31]
		return self.round_number in start_rounds 

	def get_timeout_seconds(self):
		# if a participant is marked as a dropout at any point during the experiment, they are 
		# automatically pushed through each remaining page of the experiment, with each page timing
		# out after only 1 second - this is done because the group dynamics of the app require that
		# each participant in a given group passes through each page in order for the rest of the
		# group to move on
		if self.participant.vars['is_dropout'] == True:
			return 1 
		else:
			return 60

	def vars_for_template(self):
		if self.round_number == 1: 
			return{'company_name': 'Company B', 'platform_types': 'bird', 
			'groupsize': self.participant.vars['groupsize'], 'is_dropout': self.participant.vars['is_dropout'], 
			'otherps': self.participant.vars['groupsize'] - 1}
		elif self.round_number == 16:
			return{'company_name': 'Company S', 'platform_types': 'spice', 
			'groupsize': self.participant.vars['groupsize'],'is_dropout': self.participant.vars['is_dropout'], 
			'otherps': self.participant.vars['groupsize'] - 1}
		else:
			return{'company_name': 'Company E', 'platform_types': 'element', 
			'groupsize': self.participant.vars['groupsize'], 'is_dropout': self.participant.vars['is_dropout'],
			 'otherps': self.participant.vars['groupsize'] - 1}

	def before_next_page(self):
		# If the participant fails to submit a response before the time limit, this block records the
		# timeout.
		if self.timeout_happened:
			self.player.newcomp_timeout = True
			self.participant.vars['num_timeouts'] += 1
			self.player.num_timeouts = self.participant.vars['num_timeouts']
			# This block checks the number of times a participant has allowed a page to time out. 
			# If the number of time outs passes a threshold, the participant is marked as a dropout
			# and sent to the end of the procedure.  The threshold for marking the participant as
			# a dropout increases across Phases to give participants some flexibility in case they
			# make a few honest mistakes or experience technical issues during the procedure.
			if self.round_number < 16: 
				if self.participant.vars['num_timeouts'] > 6:
					self.participant.vars['is_dropout'] = True
					self.player.is_dropout == True
					print("DROPOUT", self.player.id_in_subsession, 
						  "code", self.player.participant.code,
						  "num_timeouts", self.participant.vars['num_timeouts'], 
						  "round", self.round_number)
			elif self.round_number > 15 and self.round_number < 31:
				if self.participant.vars['num_timeouts'] > 8:
					self.participant.vars['is_dropout'] = True
					self.player.is_dropout == True
					print("DROPOUT", self.player.id_in_subsession, 
						  "code", self.player.participant.code,
						  "num_timeouts", self.participant.vars['num_timeouts'], 
						  "round", self.round_number)
			else:
				if self.participant.vars['num_timeouts'] > 10:
					self.participant.vars['is_dropout'] = True
					self.player.is_dropout == True
					print("DROPOUT", self.player.id_in_subsession, 
						  "code", self.player.participant.code,
						  "num_timeouts", self.participant.vars['num_timeouts'], 
						  "round", self.round_number)

class NewCompanyWaitPage(WaitPage):
	def is_displayed(self):
		start_rounds = [1, 16, 31]
		return self.round_number in start_rounds and self.participant.vars['is_dropout'] == False and self.participant.vars['groupsize'] > 1

	template_name = 'social_sales_game/GroupWaitPage.html'

class ChoosePlatforms(Page):
	def get_timeout_seconds(self):
		if self.participant.vars['is_dropout'] == True:
			return 1
		else:
			return 60

	form_model = models.Player

	def get_form_fields(self):
		if self.participant.vars['groupsize'] == 1:
			return ['p_name_0','p_points_0', 'p_name_1','p_points_1', 'p_name_2','p_points_2', 
				   'p_list_selected', 'curr_score', 'stub_msg']
		else:
			return ['p_name_0','p_points_0', 'p_name_1','p_points_1', 'p_name_2','p_points_2', 
				   'p_list_selected', 'curr_score', 'stub_msg', 'alter1_clicks', 'alter2_clicks',  
				   'alter3_clicks', 'alter4_clicks', 'alter5_clicks']

	def vars_for_template(self):
		start_rounds = [1, 16, 31]
		alter_results = []
		company_name = ''
		company_round = 0

		if self.round_number not in start_rounds:
			# 'get_alter_results' is defined in the Player block of models.py
			alter_results = self.player.get_alter_results()

		if self.round_number < 16:
			company_round = self.round_number
			company_name = 'Company B'
		elif self.round_number > 15 and self.round_number < 31:
			company_round = self.round_number - 15
			company_name = 'Company S'
		else:
			company_round = self.round_number - 30
			company_name = 'Company E'

		if self.round_number in start_rounds:
			# on the first trial of each Phase, no historical information is pulled in - the 
			# participant starts "fresh" at the start of each new Phase (Company)
			return{'platform_list': self.participant.vars['platforms_list_' + str(self.round_number)], 
				   'start_rounds': start_rounds, 'curr_round': self.round_number,
				   'company_name': company_name, 'company_round': company_round,
				   'groupsize': self.participant.vars['groupsize'],
				   'is_dropout': self.participant.vars['is_dropout']}
		elif self.participant.vars['groupsize'] > 1:
			# this block pulls in information from the preceding trial, so we can display the
			# participant's choices/outcomes from the preceding trial, as well as the participant's 
			# best performing trial so far, and the participant's peers' choices/outcomes from the
			# preceding trial
			lr_player = self.player.in_round(self.round_number - 1)
			return{'platform_list': self.participant.vars['platforms_list_' + str(self.round_number)], 
			       'curr_round': self.round_number, 'start_rounds': start_rounds, 
				   'company_name': company_name, 'company_round': company_round,
				   'lastround_score': lr_player.curr_score, 
				   'lastround_pname0': lr_player.p_name_0,
				   'lastround_ppoints0': lr_player.p_points_0, 
				   'lastround_pname1': lr_player.p_name_1,
				   'lastround_ppoints1': lr_player.p_points_1, 
				   'lastround_pname2': lr_player.p_name_2,
				   'lastround_ppoints2': lr_player.p_points_2,
				   'best_score': lr_player.best_score,
				   'best_pitch': lr_player.p_list_best.split(","), 
				   'best_pname0': lr_player.best_pname0,
				   'best_ppoints0': lr_player.best_ppoints0,
				   'best_pname1': lr_player.best_pname1,
				   'best_ppoints1': lr_player.best_ppoints1,
				   'best_pname2': lr_player.best_pname2,
				   'best_ppoints2': lr_player.best_ppoints2,
				   'company_score': lr_player.company_score,
				   'company_bonus': c(lr_player.company_score).to_real_world_currency(self.session),
				   # to avoid code duplication, we pull in information for 5 peers, even if the
				   # participant is in a smaller group - for smaller-group participants, these
				   # variables will be empty, and we won't display them 
				   'alter1_id': alter_results['alter1']['id'],
				   'alter1_recd': alter_results['alter1']['recd'],
				   'alter1_score': alter_results['alter1']['score'],
				   'alter1_pname0': alter_results['alter1']['pname0'],
				   'alter1_ppoints0': alter_results['alter1']['ppoints0'],
				   'alter1_pname1': alter_results['alter1']['pname1'],
				   'alter1_ppoints1': alter_results['alter1']['ppoints1'],
				   'alter1_pname2': alter_results['alter1']['pname2'],
				   'alter1_ppoints2': alter_results['alter1']['ppoints2'],
				   'alter2_id': alter_results['alter2']['id'],
				   'alter2_recd': alter_results['alter2']['recd'],
				   'alter2_score': alter_results['alter2']['score'],
				   'alter2_pname0': alter_results['alter2']['pname0'],
				   'alter2_ppoints0': alter_results['alter2']['ppoints0'],
				   'alter2_pname1': alter_results['alter2']['pname1'],
				   'alter2_ppoints1': alter_results['alter2']['ppoints1'],
				   'alter2_pname2': alter_results['alter2']['pname2'],
				   'alter2_ppoints2': alter_results['alter2']['ppoints2'],
				   'alter3_id': alter_results['alter3']['id'],
				   'alter3_recd': alter_results['alter3']['recd'],
				   'alter3_score': alter_results['alter3']['score'],
				   'alter3_pname0': alter_results['alter3']['pname0'],
				   'alter3_ppoints0': alter_results['alter3']['ppoints0'],
				   'alter3_pname1': alter_results['alter3']['pname1'],
				   'alter3_ppoints1': alter_results['alter3']['ppoints1'],
				   'alter3_pname2': alter_results['alter3']['pname2'],
				   'alter3_ppoints2': alter_results['alter3']['ppoints2'],
				   'alter4_id': alter_results['alter4']['id'],
				   'alter4_recd': alter_results['alter4']['recd'],
				   'alter4_score': alter_results['alter4']['score'],
				   'alter4_pname0': alter_results['alter4']['pname0'],
				   'alter4_ppoints0': alter_results['alter4']['ppoints0'],
				   'alter4_pname1': alter_results['alter4']['pname1'],
				   'alter4_ppoints1': alter_results['alter4']['ppoints1'],
				   'alter4_pname2': alter_results['alter4']['pname2'],
				   'alter4_ppoints2': alter_results['alter4']['ppoints2'],
				   'alter5_id': alter_results['alter5']['id'],
				   'alter5_recd': alter_results['alter5']['recd'],
				   'alter5_score': alter_results['alter5']['score'],
				   'alter5_pname0': alter_results['alter5']['pname0'],
				   'alter5_ppoints0': alter_results['alter5']['ppoints0'],
				   'alter5_pname1': alter_results['alter5']['pname1'],
				   'alter5_ppoints1': alter_results['alter5']['ppoints1'],
				   'alter5_pname2': alter_results['alter5']['pname2'],
				   'alter5_ppoints2': alter_results['alter5']['ppoints2'],
				   'groupsize': self.participant.vars['groupsize'],
				   'is_dropout': self.participant.vars['is_dropout']}
		else:
			# this block is for solo players
			lr_player = self.player.in_round(self.round_number - 1)
			return{'platform_list': self.participant.vars['platforms_list_' + str(self.round_number)], 
			       'curr_round': self.round_number, 'start_rounds': start_rounds, 
				   'company_name': company_name, 'company_round': company_round,
				   'lastround_score': lr_player.curr_score, 
				   'lastround_pname0': lr_player.p_name_0,
				   'lastround_ppoints0': lr_player.p_points_0, 
				   'lastround_pname1': lr_player.p_name_1,
				   'lastround_ppoints1': lr_player.p_points_1, 
				   'lastround_pname2': lr_player.p_name_2,
				   'lastround_ppoints2': lr_player.p_points_2,
				   'best_score': lr_player.best_score,
				   'best_pitch': lr_player.p_list_best.split(","), 
				   'best_pname0': lr_player.best_pname0,
				   'best_ppoints0': lr_player.best_ppoints0,
				   'best_pname1': lr_player.best_pname1,
				   'best_ppoints1': lr_player.best_ppoints1,
				   'best_pname2': lr_player.best_pname2,
				   'best_ppoints2': lr_player.best_ppoints2,
				   'company_score': lr_player.company_score,
				   'company_bonus': c(lr_player.company_score).to_real_world_currency(self.session),
				   'groupsize': self.participant.vars['groupsize'],
				   'is_dropout': self.participant.vars['is_dropout']}

	def before_next_page(self):
		# If the participant fails to submit a response before the time limit, this block records the
		# timeout, and sets special values for the participant's current trial that indicate a time out
		# has occurred.
		if self.timeout_happened:
			self.player.choose_p_timeout = True
			self.player.p_list_selected = "Timed Out:, No Pitch, Submitted"
			self.player.curr_score = 0
			self.player.p_name_0 = "timed_out"
			self.player.p_points_0 = 0
			self.player.p_name_1 = "timed_out"
			self.player.p_points_1 = 0
			self.player.p_name_2 = "timed_out"
			self.player.p_points_2 = 0
			self.participant.vars['num_timeouts'] += 1
			self.player.num_timeouts = self.participant.vars['num_timeouts']

			# This block checks the number of times a participant has allowed a page to time out. 
			# If the number of time outs passes a threshold, the participant is marked as a dropout
			# and sent to the end of the procedure.  The threshold for marking the participant as
			# a dropout increases across Phases to give participants some flexibility in case they
			# make a few honest mistakes or experience technical issues during the procedure.
			if self.round_number < 16:
				if self.participant.vars['num_timeouts'] > 6:
					self.participant.vars['is_dropout'] = True
					self.player.is_dropout == True
					print("DROPOUT", self.player.id_in_subsession, 
						  "code", self.player.participant.code,
						  "num_timeouts", self.participant.vars['num_timeouts'], 
						  "round", self.round_number)
			elif self.round_number > 15 and self.round_number < 31:
				if self.participant.vars['num_timeouts'] > 8:
					self.participant.vars['is_dropout'] = True
					self.player.is_dropout == True
					print("DROPOUT", self.player.id_in_subsession, 
						  "code", self.player.participant.code,
						  "num_timeouts", self.participant.vars['num_timeouts'], 
						  "round", self.round_number)
			else:
				if self.participant.vars['num_timeouts'] > 10:
					self.participant.vars['is_dropout'] = True
					self.player.is_dropout == True
					print("DROPOUT", self.player.id_in_subsession, 
						  "code", self.player.participant.code,
						  "num_timeouts", self.participant.vars['num_timeouts'], 
						  "round", self.round_number)

		# These functions are all defined in the Player block of models.py
		self.player.update_aggregate_score()
		self.player.update_company_score()
		self.player.update_best_score()
		self.player.update_best_pitch()
		self.player.set_payoff()

class Results(Page):
	def get_timeout_seconds(self):
		if self.participant.vars['is_dropout'] == True:
			return 1
		else:
			return 60

	form_model = models.Player

	def get_form_fields(self):
		end_rounds = [15, 30, 45]
		# this block flexibly pulls in form elements that record the participant's decisions
		# (not) to share their results with each peer, depending on the size of the
		# participant's group
		if self.round_number in end_rounds or self.participant.vars['groupsize'] == 1:
			return []
		elif self.participant.vars['groupsize'] == 3:
			return ['alter1_share', 'alter2_share']
		elif self.participant.vars['groupsize'] == 4:
			return ['alter1_share', 'alter2_share', 'alter3_share']
		elif self.participant.vars['groupsize'] == 5:
			return ['alter1_share','alter2_share', 'alter3_share', 'alter4_share']
		else:
			return ['alter1_share', 'alter2_share', 'alter3_share', 'alter4_share', 'alter5_share']

	def vars_for_template(self):
		end_rounds = [15, 30, 45]
		company_name = ''

		if self.round_number < 16:
			company_name = 'Company B'
			company_round = self.round_number
		elif self.round_number > 15 and self.round_number < 31:
			company_name = 'Company S'
			company_round = self.round_number - 15
		else:
			company_name = 'Company E'
			company_round = self.round_number - 30

		if self.participant.vars['groupsize'] == 1:
			# this block is for solo players
			return{'curr_score': self.player.curr_score, 'curr_pitch': self.player.p_list_selected.split(","),
			   'p_name_0': self.player.p_name_0, 'p_points_0': self.player.p_points_0, 
			   'p_name_1': self.player.p_name_1, 'p_points_1': self.player.p_points_1, 
			   'p_name_2': self.player.p_name_2, 'p_points_2': self.player.p_points_2,
			   'company_score': self.player.company_score, 'company_name': company_name,
			   'company_bonus': c(self.player.company_score).to_real_world_currency(self.session),
			   'company_round': company_round, 
			   'end_rounds': end_rounds, 'groupsize': self.participant.vars['groupsize'],
			   'is_dropout': self.participant.vars['is_dropout']}
		else:
			# this block pulls in the participant's own results from the current trial, as well as the IDs for
			# each of the participant's groupmates so we can associate the participant's share decisions with
			# the correct peer
			return{'curr_score': self.player.curr_score, 'curr_pitch': self.player.p_list_selected.split(","),
				   'p_name_0': self.player.p_name_0, 'p_points_0': self.player.p_points_0, 
				   'p_name_1': self.player.p_name_1, 'p_points_1': self.player.p_points_1, 
				   'p_name_2': self.player.p_name_2, 'p_points_2': self.player.p_points_2,
				   'company_score': self.player.company_score, 'company_name': company_name,
				   'company_bonus': c(self.player.company_score).to_real_world_currency(self.session),
				   'company_round': company_round, 
				   'alter1_id': self.participant.vars['alter1_id'], 
				   'alter2_id': self.participant.vars['alter2_id'],
				   'alter3_id': self.participant.vars['alter3_id'],
				   'alter4_id': self.participant.vars['alter4_id'],
				   'alter5_id': self.participant.vars['alter5_id'],
				   'end_rounds': end_rounds, 'groupsize': self.participant.vars['groupsize'],
				   'is_dropout': self.participant.vars['is_dropout']}

	def before_next_page(self):
		if self.timeout_happened:
			self.player.results_timeout = True
			self.participant.vars['num_timeouts'] += 1
			self.player.num_timeouts = self.participant.vars['num_timeouts']
			if self.round_number < 16:
				if self.participant.vars['num_timeouts'] > 6:
					self.participant.vars['is_dropout'] = True
					self.player.is_dropout == True
					print("DROPOUT", self.player.id_in_subsession, 
						  "code", self.player.participant.code,
						  "num_timeouts", self.participant.vars['num_timeouts'], 
						  "round", self.round_number)
			elif self.round_number > 15 and self.round_number < 31:
				if self.participant.vars['num_timeouts'] > 8:
					self.participant.vars['is_dropout'] = True
					self.player.is_dropout == True
					print("DROPOUT", self.player.id_in_subsession, 
						  "code", self.player.participant.code,
						  "num_timeouts", self.participant.vars['num_timeouts'], 
						  "round", self.round_number)
			else:
				if self.participant.vars['num_timeouts'] > 10:
					self.participant.vars['is_dropout'] = True
					self.player.is_dropout == True
					print("DROPOUT", self.player.id_in_subsession, 
						  "code", self.player.participant.code,
						  "num_timeouts", self.participant.vars['num_timeouts'], 
						  "round", self.round_number)

class ResultsWaitPage(WaitPage):
	def is_displayed(self):
		return self.participant.vars['is_dropout'] == False and self.participant.vars['groupsize'] > 1

	template_name = 'social_sales_game/GroupWaitPage.html'

	def after_all_players_arrive(self):
		for player in self.group.get_players():
			player.update_share_decisions()
			
		for player in self.group.get_players():
			player.who_shared_with_me()

class Feelcheck(Page):
	def is_displayed(self):
		feelcheck_rounds = [8, 15, 23, 30, 38, 45]
		return self.round_number in feelcheck_rounds

	def get_timeout_seconds(self):
		if self.participant.vars['is_dropout'] == True:
			return 1
		else:
			return 30

	def vars_for_template(self):
		return {'is_dropout': self.participant.vars['is_dropout']}

	form_model = models.Player
	form_fields = []

	def get_form_fields(self):
		fields = self.form_fields
		fields = ['feelcheck_happy','feelcheck_frustrated', 'feelcheck_successful', 
				  'feelcheck_friendly', 'feelcheck_hostile', 'feelcheck_anxious',
				  'checkslider_happy','checkslider_frustrated', 'checkslider_successful', 
				  'checkslider_friendly', 'checkslider_hostile', 'checkslider_anxious']
		random.shuffle(fields)
		return fields

	# this block of functions defines specific error messages that display when a
	# participant fails to interact with a given slider form input
	def checkslider_happy_error_message(self, value):
			if not value:
				return 'Please indicate your response on the happy scale'
	def checkslider_frustrated_error_message(self, value):
			if not value:
				return 'Please indicate your response on the frustrated scale'
	def checkslider_successful_error_message(self, value):
			if not value:
				return 'Please indicate your response on the successful scale'
	def checkslider_friendly_error_message(self, value):
			if not value:
				return 'Please indicate your response on the friendly scale'
	def checkslider_hostile_error_message(self, value):
			if not value:
				return 'Please indicate your response on the hostile scale'
	def checkslider_anxious_error_message(self, value):
			if not value:
				return 'Please indicate your response on the anxious scale'

	def before_next_page(self):
		if self.timeout_happened:
			self.player.feelcheck_timeout = True
			self.participant.vars['num_timeouts'] += 1
			self.player.num_timeouts = self.participant.vars['num_timeouts']
			if self.round_number < 16:
				if self.participant.vars['num_timeouts'] > 6:
					self.participant.vars['is_dropout'] = True
					self.player.is_dropout == True
					print("DROPOUT", self.player.id_in_subsession, 
						  "code", self.player.participant.code,
						  "num_timeouts", self.participant.vars['num_timeouts'], 
						  "round", self.round_number)
			elif self.round_number > 15 and self.round_number < 31:
				if self.participant.vars['num_timeouts'] > 8:
					self.participant.vars['is_dropout'] = True
					self.player.is_dropout == True
					print("DROPOUT", self.player.id_in_subsession, 
						  "code", self.player.participant.code,
						  "num_timeouts", self.participant.vars['num_timeouts'], 
						  "round", self.round_number)
			else:
				if self.participant.vars['num_timeouts'] > 10:
					self.participant.vars['is_dropout'] = True
					self.player.is_dropout == True
					print("DROPOUT", self.player.id_in_subsession, 
						  "code", self.player.participant.code,
						  "num_timeouts", self.participant.vars['num_timeouts'], 
						  "round", self.round_number)

class FeelCheckWaitPage(WaitPage):
	def is_displayed(self):
		feelcheck_rounds = [8, 15, 23, 30, 38, 45]
		return self.round_number in feelcheck_rounds and self.participant.vars['is_dropout'] == False and self.participant.vars['groupsize'] > 1

	template_name = 'social_sales_game/GroupWaitPage.html'

class CheckIn(Page):
	def is_displayed(self):
		checkin_rounds = [8, 15, 23, 30, 38, 45]
		return self.round_number in checkin_rounds

	def get_timeout_seconds(self):
		if self.participant.vars['is_dropout'] == True:
			return 1
		else:
			return 120

	form_model = models.Player
	form_fields = []

	def get_form_fields(self):
		fields = self.form_fields
		fields = ['plat1_guess','plat2_guess','plat3_guess','plat4_guess','plat5_guess',
				  'plat6_guess','plat7_guess','plat8_guess','plat9_guess','plat10_guess',
				  'plat11_guess','plat12_guess','plat13_guess','plat14_guess','plat15_guess',
				  'plat16_guess','plat17_guess','plat18_guess','plat19_guess','plat20_guess']
		random.shuffle(fields)
		return fields

	def vars_for_template(self):
		if self.round_number < 16:
			return{'company_name': 'Company B', 'is_dropout': self.participant.vars['is_dropout']}
		elif self.round_number > 15 and self.round_number < 31:
			return{'company_name': 'Company S', 'is_dropout': self.participant.vars['is_dropout']}
		else:
			return{'company_name': 'Company E', 'is_dropout': self.participant.vars['is_dropout']}

	def before_next_page(self):
		if self.timeout_happened:
			self.player.checkin_timeout = True	
			self.participant.vars['num_timeouts'] += 1
			self.player.num_timeouts = self.participant.vars['num_timeouts']
			if self.round_number < 16:
				if self.participant.vars['num_timeouts'] > 6:
					self.participant.vars['is_dropout'] = True
					self.player.is_dropout == True
					print("DROPOUT", self.player.id_in_subsession, 
						  "code", self.player.participant.code,
						  "num_timeouts", self.participant.vars['num_timeouts'], 
						  "round", self.round_number)
			elif self.round_number > 15 and self.round_number < 31:
				if self.participant.vars['num_timeouts'] > 8:
					self.participant.vars['is_dropout'] = True
					self.player.is_dropout == True
					print("DROPOUT", self.player.id_in_subsession, 
						  "code", self.player.participant.code,
						  "num_timeouts", self.participant.vars['num_timeouts'], 
						  "round", self.round_number)
			else:
				if self.participant.vars['num_timeouts'] > 10:
					self.participant.vars['is_dropout'] = True
					self.player.is_dropout == True
					print("DROPOUT", self.player.id_in_subsession, 
						  "code", self.player.participant.code,
						  "num_timeouts", self.participant.vars['num_timeouts'], 
						  "round", self.round_number)

class Confidence(Page):
	def is_displayed(self):
		checkin_rounds = [8, 15, 23, 30, 38, 45]
		return self.round_number in checkin_rounds

	def get_timeout_seconds(self):
		if self.participant.vars['is_dropout'] == True:
			return 1
		else:
			return 30

	form_model = models.Player
	form_fields = ['confidence','checkslider_confidence']

	def vars_for_template(self):
		if self.round_number < 16:
			estimates = [['Canary', self.player.plat1_guess],['Cardinal', self.player.plat2_guess],
						['Finch', self.player.plat3_guess],['Grackle', self.player.plat4_guess],
						['Jackdaw', self.player.plat5_guess],['Lark', self.player.plat6_guess],
						['Longspur', self.player.plat7_guess],['Magpie', self.player.plat8_guess],
						['Martin', self.player.plat9_guess],['Munia', self.player.plat10_guess],
						['Oriole', self.player.plat11_guess],['Pipit', self.player.plat12_guess],
						['Robin', self.player.plat13_guess],['Sparrow', self.player.plat14_guess],
						['Starling', self.player.plat15_guess],['Swallow', self.player.plat16_guess],
						['Tanager', self.player.plat17_guess],['Thrush', self.player.plat18_guess],
						['Warbler', self.player.plat19_guess],['Wren', self.player.plat20_guess]]
			estimates.sort(key=lambda x: x[1], reverse = True)
			return{'company_name': 'Company B', 'estimates': estimates, 'is_dropout': self.participant.vars['is_dropout']}
		elif self.round_number > 15 and self.round_number < 31:
			estimates = [['Ajwain', self.player.plat1_guess],['Anise', self.player.plat2_guess],
						['Annatto', self.player.plat3_guess],['Cardamom', self.player.plat4_guess],
						['Cinnamon', self.player.plat5_guess],['Cumin', self.player.plat6_guess],
						['Dill', self.player.plat7_guess],['Fennel', self.player.plat8_guess],
						['Fenugreek', self.player.plat9_guess],['Galangal', self.player.plat10_guess],
						['Ginger', self.player.plat11_guess],['Mahleb', self.player.plat12_guess],
						['Mustard', self.player.plat13_guess],['Nigella', self.player.plat14_guess],
						['Nutmeg', self.player.plat15_guess],['Paprika', self.player.plat16_guess],
						['Pepper', self.player.plat17_guess],['Saffron', self.player.plat18_guess],
						['Sumac', self.player.plat19_guess],['Turmeric', self.player.plat20_guess]]
			estimates.sort(key=lambda x: x[1], reverse = True)
			return{'company_name': 'Company S', 'estimates': estimates, 'is_dropout': self.participant.vars['is_dropout']}
		else:
			estimates = [['Argon', self.player.plat1_guess],['Bismuth', self.player.plat2_guess],
						['Bromine', self.player.plat3_guess],['Carbon', self.player.plat4_guess],
						['Cobalt', self.player.plat5_guess],['Copper', self.player.plat6_guess],
						['Gallium', self.player.plat7_guess],['Helium', self.player.plat8_guess],
						['Hydrogen', self.player.plat9_guess],['Iodine', self.player.plat10_guess],
						['Iron', self.player.plat11_guess],['Mercury', self.player.plat12_guess],
						['Neon', self.player.plat13_guess],['Nickel', self.player.plat14_guess],
						['Oxygen', self.player.plat15_guess],['Tin', self.player.plat16_guess],
						['Radon', self.player.plat17_guess],['Rhodium', self.player.plat18_guess],
						['Xenon', self.player.plat19_guess],['Zinc', self.player.plat20_guess]]
			estimates.sort(key=lambda x: x[1], reverse = True)
			return{'company_name': 'Company E', 'estimates': estimates, 'is_dropout': self.participant.vars['is_dropout']}

	def before_next_page(self):
		if self.timeout_happened:
			self.player.confidence_timeout = True
			self.participant.vars['num_timeouts'] += 1
			self.player.num_timeouts = self.participant.vars['num_timeouts']
			if self.round_number < 16:
				if self.participant.vars['num_timeouts'] > 6:
					self.participant.vars['is_dropout'] = True
					self.player.is_dropout == True
					print("DROPOUT", self.player.id_in_subsession, 
						  "code", self.player.participant.code,
						  "num_timeouts", self.participant.vars['num_timeouts'], 
						  "round", self.round_number)
			elif self.round_number > 15 and self.round_number < 31:
				if self.participant.vars['num_timeouts'] > 8:
					self.participant.vars['is_dropout'] = True
					self.player.is_dropout == True
					print("DROPOUT", self.player.id_in_subsession, 
						  "code", self.player.participant.code,
						  "num_timeouts", self.participant.vars['num_timeouts'], 
						  "round", self.round_number)
			else:
				if self.participant.vars['num_timeouts'] > 10:
					self.participant.vars['is_dropout'] = True
					self.player.is_dropout == True
					print("DROPOUT", self.player.id_in_subsession, 
						  "code", self.player.participant.code,
						  "num_timeouts", self.participant.vars['num_timeouts'], 
						  "round", self.round_number)

	def checkslider_confidence_error_message(self, value):
			if not value:
				return 'Please indicate your response on the sliding scale'

class ConfidenceWaitPage(WaitPage):
	def is_displayed(self):
		checkin_rounds = [8, 15, 23, 30, 38, 45]
		return self.round_number in checkin_rounds and self.participant.vars['is_dropout'] == False and self.participant.vars['groupsize'] > 1

	template_name = 'social_sales_game/GroupWaitPage.html'


class CompanySummary(Page):
	def is_displayed(self):
		summary_rounds = [15, 30, 45]
		return self.round_number in summary_rounds

	def get_timeout_seconds(self):
		if self.participant.vars['is_dropout'] == True:
			return 1
		else:
			return 30

	def vars_for_template(self):
		if self.round_number == 15:
			return{'company_name': 'Company B', 'company_score': self.player.company_score, 
				   'company_bonus': c(self.player.company_score).to_real_world_currency(self.session),
				   'is_dropout': self.participant.vars['is_dropout'], 'phase': 1, 'nextphase': 2}
		elif self.round_number == 30:
			return{'company_name': 'Company S', 'company_score': self.player.company_score,
				   'company_bonus': c(self.player.company_score).to_real_world_currency(self.session),
				   'is_dropout': self.participant.vars['is_dropout'], 'phase': 2, 'nextphase': 3}
		else:
			return{'company_name': 'Company E', 'company_score': self.player.company_score,
				   'company_bonus': c(self.player.company_score).to_real_world_currency(self.session),
				   'is_dropout': self.participant.vars['is_dropout'], 'phase': 3}

	def before_next_page(self):
		if self.timeout_happened:
			self.player.companysummary_timeout = True
			self.participant.vars['num_timeouts'] += 1
			self.player.num_timeouts = self.participant.vars['num_timeouts']
			if self.round_number < 16:
				if self.participant.vars['num_timeouts'] > 6:
					self.participant.vars['is_dropout'] = True
					self.player.is_dropout == True
					print("DROPOUT", self.player.id_in_subsession, 
						  "code", self.player.participant.code,
						  "num_timeouts", self.participant.vars['num_timeouts'], 
						  "round", self.round_number)
			elif self.round_number > 15 and self.round_number < 31:
				if self.participant.vars['num_timeouts'] > 8:
					self.participant.vars['is_dropout'] = True
					self.player.is_dropout == True
					print("DROPOUT", self.player.id_in_subsession, 
						  "code", self.player.participant.code,
						  "num_timeouts", self.participant.vars['num_timeouts'], 
						  "round", self.round_number)
			else:
				if self.participant.vars['num_timeouts'] > 10:
					self.participant.vars['is_dropout'] = True
					self.player.is_dropout == True
					print("DROPOUT", self.player.id_in_subsession, 
						  "code", self.player.participant.code,
						  "num_timeouts", self.participant.vars['num_timeouts'], 
						  "round", self.round_number)

		# this block adds a bonus payment to participant's final payoff if they made it through
		# the entire procedure without being marked as a dropout
		if self.round_number == Constants.num_rounds:
			completion_bonus = 0
			if self.participant.vars['is_dropout'] == False:
				completion_bonus = 40000
			self.player.payoff = self.player.payoff + completion_bonus

class FinalResults(Page):
	def is_displayed(self):
		return self.round_number == Constants.num_rounds

	def vars_for_template(self):
		score_bonus = self.player.aggregate_score
		total_bonus = 0
		completion_bonus = 0

		if self.participant.vars['is_dropout'] == False:
			completion_bonus = 40000

		total_bonus = score_bonus + completion_bonus

		return{'aggregate_score': score_bonus, 
			   'score_bonus': c(score_bonus).to_real_world_currency(self.session),
			   'total_bonus': c(total_bonus).to_real_world_currency(self.session),
			   'is_dropout': self.player.participant.vars['is_dropout'],
			   'completion_bonus': c(completion_bonus).to_real_world_currency(self.session)}

class Debrief(Page):
	def is_displayed(self):
		return self.round_number == Constants.num_rounds 

	form_model = models.Player

	def get_form_fields(self):
		if self.participant.vars['groupsize'] == 1:
			return ['strategy', 'comments', 'selfassessment','checkslider_selfassessment']
		elif self.participant.vars['groupsize'] == 3:
			return ['alter1_help', 'alter2_help', 'strategy', 'comments', 'selfassessment',
				    'checkslider_selfassessment', 'checkslider_alter1_help', 'checkslider_alter2_help']
		elif self.participant.vars['groupsize'] == 4:
			return ['alter1_help', 'alter2_help', 'alter3_help', 'strategy', 'comments', 
				    'selfassessment', 'checkslider_selfassessment', 'checkslider_alter1_help', 
				    'checkslider_alter2_help', 'checkslider_alter3_help']
		elif self.participant.vars['groupsize'] == 5:
			return ['alter1_help', 'alter2_help', 'alter3_help', 'alter4_help', 'strategy',
				    'comments', 'selfassessment', 'checkslider_selfassessment', 'checkslider_alter1_help', 
				    'checkslider_alter2_help', 'checkslider_alter3_help', 'checkslider_alter4_help']
		else:
			return ['alter1_help', 'alter2_help', 'alter3_help', 'alter4_help', 'alter5_help',
				    'strategy', 'comments', 'selfassessment', 'checkslider_selfassessment', 
				    'checkslider_alter1_help', 'checkslider_alter2_help', 'checkslider_alter3_help', 
				    'checkslider_alter4_help', 'checkslider_alter5_help']

	def vars_for_template(self):
		if self.participant.vars['groupsize'] == 1:
			return{'groupsize': self.participant.vars['groupsize']}
		elif self.participant.vars['groupsize'] == 3:
			return{'alter1_id': self.participant.vars['alter1_id'], 
				   'alter2_id': self.participant.vars['alter2_id'],
				   'groupsize': self.participant.vars['groupsize']}
		elif self.participant.vars['groupsize'] == 4:
			return{'alter1_id': self.participant.vars['alter1_id'], 
				   'alter2_id': self.participant.vars['alter2_id'],
				   'alter3_id': self.participant.vars['alter3_id'],
				   'groupsize': self.participant.vars['groupsize']}
		elif self.participant.vars['groupsize'] == 5:
			return{'alter1_id': self.participant.vars['alter1_id'], 
				   'alter2_id': self.participant.vars['alter2_id'],
				   'alter3_id': self.participant.vars['alter3_id'],
				   'alter4_id': self.participant.vars['alter4_id'],
				   'groupsize': self.participant.vars['groupsize']}
		else:
			return{'alter1_id': self.participant.vars['alter1_id'], 
				   'alter2_id': self.participant.vars['alter2_id'],
				   'alter3_id': self.participant.vars['alter3_id'],
				   'alter4_id': self.participant.vars['alter4_id'],
				   'alter5_id': self.participant.vars['alter5_id'],
				   'groupsize': self.participant.vars['groupsize']}

	# this block of functions defines specific error messages that display when a
	# participant fails to interact with a given slider form input
	def checkslider_selfassessment_error_message(self, value):
			if not value:
				return 'Please rate your performance on the sliding scale'
	def checkslider_alter1_help_error_message(self, value):
			if not value:
				return 'Please rate the helpfulness of Player' + str(self.participant.vars['alter1_id'])
	def checkslider_alter2_help_error_message(self, value):
			if not value:
				return 'Please rate the helpfulness of Player' + str(self.participant.vars['alter2_id'])
	def checkslider_alter3_help_error_message(self, value):
			if not value:
				return 'Please rate the helpfulness of Player' + str(self.participant.vars['alter3_id'])
	def checkslider_alter4_help_error_message(self, value):
			if not value:
				return 'Please rate the helpfulness of Player' + str(self.participant.vars['alter4_id'])
	def checkslider_alter5_help_error_message(self, value):
			if not value:
				return 'Please rate the helpfulness of Player' + str(self.participant.vars['alter5_id'])

	

page_sequence = [
	ArrivalWaitPage,
	SoloPlayer,
	Matched,
	NewCompany,
	NewCompanyWaitPage,
	ChoosePlatforms,
	Results,
	ResultsWaitPage,
	Feelcheck,
	FeelCheckWaitPage,
	CheckIn,
	Confidence,
	ConfidenceWaitPage,
	CompanySummary,
	FinalResults,
	Debrief
]
