from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import random
import itertools

author = 'Kariyushi'

doc = """
Participants are shown performance history of an agent, and guess how that agent
will perform in the current competition.  Participants are then shown the outcome
of the current competition, and are asked to assign credit or blame to the agent
for that outcome.
"""


class Constants(BaseConstants):
    name_in_url = 'responsibility_attribution'
    players_per_group = None
    num_rounds = 3

    # stimuli
    people = {1: {'name': 'Williams', 'sample': 20,'dots': 'Williams0', 'prior': 'Williams1', 'current': 'Williams2', 'score': 7, 'attribute': 'credit', 'affect': 'positive'},
    		  2: {'name': 'Selle', 'sample': 100, 'dots': 'Selle0','prior': 'Selle1', 'current': 'Selle2', 'score': 3, 'attribute': 'blame', 'affect': 'negative'},
    		  3: {'name': 'Avis', 'sample': 20, 'dots': 'Avis0','prior': 'Avis1', 'current': 'Avis2', 'score': 9, 'attribute': 'credit', 'affect': 'positive'}}


class Subsession(BaseSubsession):
	def creating_session(self):
		image_index = self.round_number - 1
		print(image_index)

		if self.round_number == 1:
			for p in self.get_players():
				# copy in the stimuli keys and shuffle them
				people = Constants.people.copy()
				people_sequence = [1,2,3]
				print(people_sequence)

				random.shuffle(people_sequence)

				print(people_sequence)
				# record sequence of stimuli as participant variable
				p.participant.vars['people_sequence'] = people_sequence
				
				print(p.participant.vars['people_sequence'])
				# create a temporary list to manipulate
				people_list = people_sequence

				print(people_list)
				# record stim attributes
				stim_id = people_list[image_index]
				p.stim_id = stim_id
				p.stim_name = people[stim_id]['name']
				p.stim_sample = people[stim_id]['sample']
				p.stim_dots = people[stim_id]['dots']
				p.stim_prior = people[stim_id]['prior']
				p.stim_current = people[stim_id]['current']
				p.stim_score = people[stim_id]['score']
				p.stim_attribute = people[stim_id]['attribute']
				p.stim_affect = people[stim_id]['affect']
		else:
			for p in self.get_players():
				people = Constants.people.copy()
				# create a temporary list to manipulate
				people_list = p.participant.vars['people_sequence']
				# record player attributess
				stim_id = people_list[image_index]
				p.stim_id = stim_id
				p.stim_name = people[stim_id]['name']
				p.stim_sample = people[stim_id]['sample']
				p.stim_dots = people[stim_id]['dots']
				p.stim_prior = people[stim_id]['prior']
				p.stim_current = people[stim_id]['current']
				p.stim_score = people[stim_id]['score']
				p.stim_attribute = people[stim_id]['attribute']
				p.stim_affect = people[stim_id]['affect']
	    	

class Group(BaseGroup):
    pass


class Player(BasePlayer):
	stim_id = models.CharField()
	stim_name = models.CharField()
	stim_sample = models.IntegerField()
	stim_dots = models.CharField()
	stim_prior = models.CharField()
	stim_current = models.CharField()
	stim_score = models.CharField()
	stim_attribute = models.CharField()
	stim_affect = models.CharField()

	prediction = models.IntegerField(
    	widget=widgets.Slider(attrs={'step': '1.00'},
    		show_value=False))

	attribution = models.IntegerField(
    	widget=widgets.Slider(attrs={'step': '1.00'},
    		show_value=False))

