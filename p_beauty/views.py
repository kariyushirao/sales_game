from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
from collections import defaultdict

import random
from random import shuffle


class Introduction(Page):
	def is_displayed(self):
		return self.round_number == 1


class Guess(Page):
	form_model = 'player'
	form_fields = ['guess']


class ResultsWaitPage(WaitPage):
	template_name = 'p_beauty/ResultsWaitPage.html'

	def after_all_players_arrive(self):
		self.group.set_payoffs()


class Results(Page):
	def vars_for_template(self):
		sorted_guesses = sorted(p.guess for p in self.group.get_players())

		return dict(sorted_guesses=sorted_guesses)


page_sequence = [Introduction, Guess, ResultsWaitPage, Results]