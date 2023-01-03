from otree.api import (
	models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
	Currency as c, currency_range
)
import random
from random import shuffle
import itertools

author = '© Kariyushi Rao 2022'

doc = """
Instructions and comprehension check for group version of The Sales Game.
"""


class Constants(BaseConstants):
	name_in_url = 'instructions'
	players_per_group = None
	num_rounds = 1

class Subsession(BaseSubsession):
	def creating_session(self):
		treatments = itertools.cycle(['control', 'abundance', 'scarcity'])

		if self.round_number == 1:
			for p in self.get_players():
				if 'treatment' in self.session.config:
					treatment = self.session.config['treatment']
					p.participant.vars['treatment'] = treatment
					p.treatment = treatment
				else:
					treatment = next(treatments)
					p.participant.vars['treatment'] = treatment
					p.treatment = treatment
		else:
			for p in self.get_players():
				treatment = p.participant.vars['treatment']
				p.treatment = treatment

class Group(BaseGroup):
	pass

class Player(BasePlayer):
	treatment = models.StringField()

	numerrors_comprehension = models.IntegerField(initial=0, label="")

	comprehension1 = models.IntegerField(
		choices=[15, 20, 3, 5],
		widget=widgets.RadioSelectHorizontal
		)
	comprehension2 = models.IntegerField(
		choices=[15, 3, 5, 20],
		widget=widgets.RadioSelectHorizontal
		)
	comprehension3 = models.IntegerField(
		choices=[[1, 'adding up the points the customer assigned to each platform in the pitch.'],
				 [2, 'subtracting the lowest-value platform from the highest-value platform.'],
				 [3, 'taking the average value of the platforms in your pitch.']],
		widget=widgets.RadioSelect
		)
	comprehension4 = models.IntegerField(
		choices=[[1, 'It will be based on the highest Total Pitch Score you earned in the game.'],
				 [2, 'We will add up all the Total Pitch Scores you earned in every round of the game.'],
				 [3, 'We will subtract your lowest Total Pitch Score from your highest total Pitch Score.']],
		widget=widgets.RadioSelect
		)
	comprehension5 = models.IntegerField(
		choices=[[1, 'Each platform has the same average value as other platforms sold by that company.'],
				 [2, 'Each platform has a different average value than other platforms sold by that company.'],
				 [3, 'Platforms have average values that change all the time.']],
		widget=widgets.RadioSelect
		)
	comprehension6 = models.IntegerField(
		choices=[[1, 'Customers assign points close to the average value of each platform.'],
				 [2, 'Customers totally disagree about how valuable each platform is.'],
				 [3, 'Customers assign random point values to each platform.']],
		widget=widgets.RadioSelect
		)
	comprehension7 = models.IntegerField(
		choices=[[1, 'Customers judge platforms based on their code names, not what they do.'],
				 [2, 'Customers judge platforms based on both their code names and what they do.'],
				 [3, 'Customers judge platforms based on what they do, not their code names.']],
		widget=widgets.RadioSelect
		)
	comprehension8 = models.IntegerField(
		choices=[[1, 'Yes, each round we will all submit our pitches to the same customer.'],
				 [2, 'No, each round we will all submit our pitches to different customers.']],
		widget=widgets.RadioSelect
		)
	comprehension9 = models.IntegerField(
		choices=[[1, 'The player chose to share with you, but you did not choose to share with them.'],
				 [2, 'The player did not choose to share with you, but you did choose to share with them.'],
				 [3, 'The player chose to share with you, and you also chose to share with them.']],
		widget=widgets.RadioSelect
		)


