from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants

import random

class Instructions1(Page):
	def is_displayed(self):
		return self.round_number == 1

class Instructions2(Page):
	def is_displayed(self):
		return self.round_number == 1

class Instructions3(Page):
	def is_displayed(self):
		return self.round_number == 1

class Instructions4(Page):
	def is_displayed(self):
		return self.round_number == 1

	def vars_for_template(self):
		return{'demo1': 'solo_sales_game_instructions/pictures/demo1.gif'}

class Instructions5(Page):
	def is_displayed(self):
		return self.round_number == 1
	
	def vars_for_template(self):
		treatment = self.player.treatment
		demo2 = ''

		if treatment == 'control':
			demo2 = 'solo_sales_game_instructions/pictures/demo2_c.png'
		elif treatment == 'abundance':
			demo2 = 'solo_sales_game_instructions/pictures/demo2_a.png'
		else:
			demo2 = 'solo_sales_game_instructions/pictures/demo2_s.png'

		return{'demo2': demo2}

class Instructions6(Page):
	def is_displayed(self):
		return self.round_number == 1
	
	def vars_for_template(self):
		treatment = self.player.treatment
		demo3 = ''

		if treatment == 'control':
			demo3 = 'solo_sales_game_instructions/pictures/demo3_c.png'
		elif treatment == 'abundance':
			demo3 = 'solo_sales_game_instructions/pictures/demo3_a.png'
		else:
			demo3 = 'solo_sales_game_instructions/pictures/demo3_s.png'

		return{'demo3': demo3}

class ComprehensionCheck(Page):
	def is_displayed(self):
		return self.round_number == 1

	form_model = models.Player
	form_fields = ['comprehension1', 'comprehension2', 'comprehension3', 'comprehension4', 
				   'comprehension5', 'comprehension6', 'comprehension7']

	def error_message(self, values):
		comp1 = (values['comprehension1'] == 15)
		comp2 = (values['comprehension2'] == 3)
		comp3 = (values['comprehension3'] == 1)
		comp4 = (values['comprehension4'] == 2)
		comp5 = (values['comprehension5'] == 2)
		comp6 = (values['comprehension6'] == 1)
		comp7 = (values['comprehension7'] == 3)

		results = [comp1, comp2, comp3, comp4, comp5, comp6, comp7]
		checks = []

		for i in range(0,len(results)):
			if results[i] == False:
				checks.append(i + 1)

		if not (comp1 and comp2 and comp3 and comp4 and comp5 and comp6 and comp7):
			self.player.numerrors_comprehension += 1
			return ('Check your answers to these questions: ' + ', '.join(str(c) for c in checks))

class DropoutWarning(Page):
	def is_displayed(self):
		return self.round_number == 1


page_sequence = [
	Instructions1,
	Instructions2,
	Instructions3,
	Instructions4,
	Instructions5,
	Instructions6,
	ComprehensionCheck,
	DropoutWarning
]
