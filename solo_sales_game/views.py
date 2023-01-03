from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
from collections import defaultdict

import random
from random import shuffle

class NewCompany(Page):
	def is_displayed(self):
		start_rounds = [1, 16, 31]
		return self.round_number in start_rounds 

	def get_timeout_seconds(self):
		if self.participant.vars['is_dropout'] == True:
			return 1 
		else:
			return 60

	def vars_for_template(self):
		if self.round_number == 1: 
			return{'company_name': 'Company B', 'platform_types': 'bird', 
				   'is_dropout': self.participant.vars['is_dropout']}
		elif self.round_number == 16:
			return{'company_name': 'Company S', 'platform_types': 'spice',
			'is_dropout': self.participant.vars['is_dropout']}
		else:
			return{'company_name': 'Company E', 'platform_types': 'element',
			'is_dropout': self.participant.vars['is_dropout']}

	def before_next_page(self):
		if self.timeout_happened:
			self.player.newcomp_timeout = True
			self.participant.vars['num_timeouts'] += 1
			self.player.num_timeouts = self.participant.vars['num_timeouts']
			if self.round_number < 16:
				if self.participant.vars['num_timeouts'] > 6:
					self.participant.vars['is_dropout'] = True
					self.player.is_dropout == True
					print("DROPOUT HAPPENED", self.player.id_in_subsession, 
						  "code", self.player.participant.code,
						  "num_timeouts", self.participant.vars['num_timeouts'], 
						  "round", self.round_number)
			elif self.round_number > 15 and self.round_number < 31:
				if self.participant.vars['num_timeouts'] > 8:
					self.participant.vars['is_dropout'] = True
					self.player.is_dropout == True
					print("DROPOUT HAPPENED", self.player.id_in_subsession, 
						  "code", self.player.participant.code,
						  "num_timeouts", self.participant.vars['num_timeouts'], 
						  "round", self.round_number)
			else:
				if self.participant.vars['num_timeouts'] > 10:
					self.participant.vars['is_dropout'] = True
					self.player.is_dropout == True
					print("DROPOUT HAPPENED", self.player.id_in_subsession, 
						  "code", self.player.participant.code,
						  "num_timeouts", self.participant.vars['num_timeouts'], 
						  "round", self.round_number)

class ChoosePlatforms(Page):
	def get_timeout_seconds(self):
		if self.participant.vars['is_dropout'] == True:
			return 1
		else:
			return 60

	form_model = models.Player
	form_fields = ['p_name_0','p_points_0', 'p_name_1','p_points_1', 'p_name_2','p_points_2', 
				   'p_list_selected', 'curr_score', 'stub_msg', 'browser_innerw', 'browser_innerh']

	def vars_for_template(self):
		start_rounds = [1, 16, 31]
		company_name = ''
		company_round = 0

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
			return{'platform_list': self.participant.vars['platforms_list_' + str(self.round_number)], 
				   'start_rounds': start_rounds, 'curr_round': self.round_number,
				   'company_name': company_name, 'company_round': company_round,
				   'is_dropout': self.participant.vars['is_dropout']}
		else:
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
				   'is_dropout': self.participant.vars['is_dropout']}

	def before_next_page(self):
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
			if self.round_number < 16:
				if self.participant.vars['num_timeouts'] > 6:
					self.participant.vars['is_dropout'] = True
					self.player.is_dropout == True
					print("DROPOUT HAPPENED", self.player.id_in_subsession, 
						  "code", self.player.participant.code,
						  "num_timeouts", self.participant.vars['num_timeouts'], 
						  "round", self.round_number)
			elif self.round_number > 15 and self.round_number < 31:
				if self.participant.vars['num_timeouts'] > 8:
					self.participant.vars['is_dropout'] = True
					self.player.is_dropout == True
					print("DROPOUT HAPPENED", self.player.id_in_subsession, 
						  "code", self.player.participant.code,
						  "num_timeouts", self.participant.vars['num_timeouts'], 
						  "round", self.round_number)
			else:
				if self.participant.vars['num_timeouts'] > 10:
					self.participant.vars['is_dropout'] = True
					self.player.is_dropout == True
					print("DROPOUT HAPPENED", self.player.id_in_subsession, 
						  "code", self.player.participant.code,
						  "num_timeouts", self.participant.vars['num_timeouts'], 
						  "round", self.round_number)

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

		return{'curr_score': self.player.curr_score, 'curr_pitch': self.player.p_list_selected.split(","),
		   'p_name_0': self.player.p_name_0, 'p_points_0': self.player.p_points_0, 
		   'p_name_1': self.player.p_name_1, 'p_points_1': self.player.p_points_1, 
		   'p_name_2': self.player.p_name_2, 'p_points_2': self.player.p_points_2,
		   'company_score': self.player.company_score, 'company_name': company_name,
		   'company_bonus': c(self.player.company_score).to_real_world_currency(self.session),
		   'company_round': company_round, 'end_rounds': end_rounds,
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
					print("DROPOUT HAPPENED", self.player.id_in_subsession, 
						  "code", self.player.participant.code,
						  "num_timeouts", self.participant.vars['num_timeouts'], 
						  "round", self.round_number)
			elif self.round_number > 15 and self.round_number < 31:
				if self.participant.vars['num_timeouts'] > 8:
					self.participant.vars['is_dropout'] = True
					self.player.is_dropout == True
					print("DROPOUT HAPPENED", self.player.id_in_subsession, 
						  "code", self.player.participant.code,
						  "num_timeouts", self.participant.vars['num_timeouts'], 
						  "round", self.round_number)
			else:
				if self.participant.vars['num_timeouts'] > 10:
					self.participant.vars['is_dropout'] = True
					self.player.is_dropout == True
					print("DROPOUT HAPPENED", self.player.id_in_subsession, 
						  "code", self.player.participant.code,
						  "num_timeouts", self.participant.vars['num_timeouts'], 
						  "round", self.round_number)

class Feelcheck(Page):
	def is_displayed(self):
		feelcheck_rounds = [8, 15, 23, 30, 38, 45]
		return self.round_number in feelcheck_rounds

	def get_timeout_seconds(self):
		if self.participant.vars['is_dropout'] == True:
			return 1
		else:
			return 30

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

	def vars_for_template(self):
		return {'is_dropout': self.participant.vars['is_dropout']}

	def before_next_page(self):
		if self.timeout_happened:
			self.player.feelcheck_timeout = True
			self.participant.vars['num_timeouts'] += 1
			self.player.num_timeouts = self.participant.vars['num_timeouts']
			if self.round_number < 16:
				if self.participant.vars['num_timeouts'] > 6:
					self.participant.vars['is_dropout'] = True
					self.player.is_dropout == True
					print("DROPOUT HAPPENED", self.player.id_in_subsession, 
						  "code", self.player.participant.code,
						  "num_timeouts", self.participant.vars['num_timeouts'], 
						  "round", self.round_number)
			elif self.round_number > 15 and self.round_number < 31:
				if self.participant.vars['num_timeouts'] > 8:
					self.participant.vars['is_dropout'] = True
					self.player.is_dropout == True
					print("DROPOUT HAPPENED", self.player.id_in_subsession, 
						  "code", self.player.participant.code,
						  "num_timeouts", self.participant.vars['num_timeouts'], 
						  "round", self.round_number)
			else:
				if self.participant.vars['num_timeouts'] > 10:
					self.participant.vars['is_dropout'] = True
					self.player.is_dropout == True
					print("DROPOUT HAPPENED", self.player.id_in_subsession, 
						  "code", self.player.participant.code,
						  "num_timeouts", self.participant.vars['num_timeouts'], 
						  "round", self.round_number)

class CheckIn(Page):
	def is_displayed(self):
		checkin_rounds = [8, 15, 23, 30, 38, 45]
		return self.round_number in checkin_rounds

	form_model = models.Player
	form_fields = []

	def get_timeout_seconds(self):
		if self.participant.vars['is_dropout'] == True:
			return 1
		else:
			return 120

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
					print("DROPOUT HAPPENED", self.player.id_in_subsession, 
						  "code", self.player.participant.code,
						  "num_timeouts", self.participant.vars['num_timeouts'], 
						  "round", self.round_number)
			elif self.round_number > 15 and self.round_number < 31:
				if self.participant.vars['num_timeouts'] > 8:
					self.participant.vars['is_dropout'] = True
					self.player.is_dropout == True
					print("DROPOUT HAPPENED", self.player.id_in_subsession, 
						  "code", self.player.participant.code,
						  "num_timeouts", self.participant.vars['num_timeouts'], 
						  "round", self.round_number)
			else:
				if self.participant.vars['num_timeouts'] > 10:
					self.participant.vars['is_dropout'] = True
					self.player.is_dropout == True
					print("DROPOUT HAPPENED", self.player.id_in_subsession, 
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
		
		if self.round_number < 16:
			return{'company_name': 'Company B', 'estimates': estimates, 'is_dropout': self.participant.vars['is_dropout']}
		elif self.round_number > 15 and self.round_number < 31:
			return{'company_name': 'Company S', 'estimates': estimates, 'is_dropout': self.participant.vars['is_dropout']}
		else:
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
					print("DROPOUT HAPPENED", self.player.id_in_subsession, 
						  "code", self.player.participant.code,
						  "num_timeouts", self.participant.vars['num_timeouts'], 
						  "round", self.round_number)
			elif self.round_number > 15 and self.round_number < 31:
				if self.participant.vars['num_timeouts'] > 8:
					self.participant.vars['is_dropout'] = True
					self.player.is_dropout == True
					print("DROPOUT HAPPENED", self.player.id_in_subsession, 
						  "code", self.player.participant.code,
						  "num_timeouts", self.participant.vars['num_timeouts'], 
						  "round", self.round_number)
			else:
				if self.participant.vars['num_timeouts'] > 10:
					self.participant.vars['is_dropout'] = True
					self.player.is_dropout == True
					print("DROPOUT HAPPENED", self.player.id_in_subsession, 
						  "code", self.player.participant.code,
						  "num_timeouts", self.participant.vars['num_timeouts'], 
						  "round", self.round_number)

	def checkslider_confidence_error_message(self, value):
			if not value:
				return 'Please indicate your response on the sliding scale'

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
					print("DROPOUT HAPPENED", self.player.id_in_subsession, 
						  "code", self.player.participant.code,
						  "num_timeouts", self.participant.vars['num_timeouts'], 
						  "round", self.round_number)
			elif self.round_number > 15 and self.round_number < 31:
				if self.participant.vars['num_timeouts'] > 8:
					self.participant.vars['is_dropout'] = True
					self.player.is_dropout == True
					print("DROPOUT HAPPENED", self.player.id_in_subsession, 
						  "code", self.player.participant.code,
						  "num_timeouts", self.participant.vars['num_timeouts'], 
						  "round", self.round_number)
			else:
				if self.participant.vars['num_timeouts'] > 10:
					self.participant.vars['is_dropout'] = True
					self.player.is_dropout == True
					print("DROPOUT HAPPENED", self.player.id_in_subsession, 
						  "code", self.player.participant.code,
						  "num_timeouts", self.participant.vars['num_timeouts'], 
						  "round", self.round_number)

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
	form_fields = ['strategy', 'comments', 'selfassessment','checkslider_selfassessment']

	def checkslider_selfassessment_error_message(self, value):
			if not value:
				return 'Please rate your performance on the sliding scale'

page_sequence = [
	NewCompany,
	ChoosePlatforms,
	Results,
	Feelcheck,
	CheckIn,
	Confidence,
	CompanySummary,
	FinalResults,
	Debrief
]
