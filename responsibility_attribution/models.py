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
    num_rounds = 42

    # stimuli
    people = {1: {'name': 'Page', 'sample': 20,'dots': 'dotplot_alpha_5_beta_5_n_20', 'prior': 'alpha_6_beta_6', 'current': 'alpha_6_beta_6_points_1', 'score': 1, 'outcome': 'FAILURE', 'attribute': 'blame', 'affect': 'negative'},
    		  2: {'name': 'Nelson', 'sample': 100, 'dots': 'dotplot_alpha_5_beta_5_n_100','prior': 'alpha_6_beta_6', 'current': 'alpha_6_beta_6_points_1', 'score': 1, 'outcome': 'FAILURE','attribute': 'blame', 'affect': 'negative'},
    		  3: {'name': 'Williams', 'sample': 20, 'dots': 'dotplot_alpha_5_beta_5_n_20','prior': 'alpha_6_beta_6', 'current': 'alpha_6_beta_6_points_3', 'score': 3, 'outcome': 'FAILURE','attribute': 'blame', 'affect': 'negative'},
    		  4: {'name': 'Guerrieri', 'sample': 100, 'dots': 'dotplot_alpha_5_beta_5_n_100','prior': 'alpha_6_beta_6', 'current': 'alpha_6_beta_6_points_3', 'score': 3, 'outcome': 'FAILURE','attribute': 'blame', 'affect': 'negative'},
    		  5: {'name': 'Moncher', 'sample': 20, 'dots': 'dotplot_alpha_5_beta_5_n_20','prior': 'alpha_6_beta_6', 'current': 'alpha_6_beta_6_points_7', 'score': 7, 'outcome': 'SUCCESS','attribute': 'credit', 'affect': 'positive'},
    		  6: {'name': 'Selle', 'sample': 100, 'dots': 'dotplot_alpha_5_beta_5_n_100','prior': 'alpha_6_beta_6', 'current': 'alpha_6_beta_6_points_7', 'score': 7, 'outcome': 'SUCCESS','attribute': 'credit', 'affect': 'positive'},
    		  7: {'name': 'Richards', 'sample': 20, 'dots': 'dotplot_alpha_5_beta_5_n_20','prior': 'alpha_6_beta_6', 'current': 'alpha_6_beta_6_points_9', 'score': 9, 'outcome': 'SUCCESS','attribute': 'credit', 'affect': 'positive'},
    		  8: {'name': 'Nichols', 'sample': 100, 'dots': 'dotplot_alpha_5_beta_5_n_100','prior': 'alpha_6_beta_6', 'current': 'alpha_6_beta_6_points_9', 'score': 9, 'outcome': 'SUCCESS','attribute': 'credit', 'affect': 'positive'},
    		  9: {'name': 'Conca', 'sample': 20,'dots': 'dotplot_alpha_3_beta_7_n_20', 'prior': 'alpha_3_beta_7', 'current': 'alpha_3_beta_7_points_1', 'score': 1, 'outcome': 'FAILURE', 'attribute': 'blame', 'affect': 'negative'},
    		  10: {'name': 'Millican', 'sample': 100, 'dots': 'dotplot_alpha_3_beta_7_n_100','prior': 'alpha_3_beta_7', 'current': 'alpha_3_beta_7_points_1', 'score': 1, 'outcome': 'FAILURE','attribute': 'blame', 'affect': 'negative'},
    		  11: {'name': 'Manguso', 'sample': 20, 'dots': 'dotplot_alpha_3_beta_7_n_20','prior': 'alpha_3_beta_7', 'current': 'alpha_3_beta_7_points_3', 'score': 3, 'outcome': 'FAILURE','attribute': 'blame', 'affect': 'negative'},
    		  12: {'name': 'Avis', 'sample': 100, 'dots': 'dotplot_alpha_3_beta_7_n_100','prior': 'alpha_3_beta_7', 'current': 'alpha_3_beta_7_points_3', 'score': 3, 'outcome': 'FAILURE','attribute': 'blame', 'affect': 'negative'},
    		  13: {'name': 'Wilson', 'sample': 20, 'dots': 'dotplot_alpha_3_beta_7_n_20','prior': 'alpha_3_beta_7', 'current': 'alpha_3_beta_7_points_7', 'score': 7, 'outcome': 'SUCCESS','attribute': 'credit', 'affect': 'positive'},
    		  14: {'name': 'Ochsner', 'sample': 100, 'dots': 'dotplot_alpha_3_beta_7_n_100','prior': 'alpha_3_beta_7', 'current': 'alpha_3_beta_7_points_7', 'score': 7, 'outcome': 'SUCCESS','attribute': 'credit', 'affect': 'positive'},
    		  15: {'name': 'Boyd', 'sample': 20, 'dots': 'dotplot_alpha_3_beta_7_n_20','prior': 'alpha_3_beta_7', 'current': 'alpha_3_beta_7_points_9', 'score': 9, 'outcome': 'SUCCESS','attribute': 'credit', 'affect': 'positive'},
    		  16: {'name': 'Yaklich', 'sample': 100, 'dots': 'dotplot_alpha_3_beta_7_n_100','prior': 'alpha_3_beta_7', 'current': 'alpha_3_beta_7_points_9', 'score': 9, 'outcome': 'SUCCESS','attribute': 'credit', 'affect': 'positive'},
    		  17: {'name': 'Carmichael', 'sample': 20,'dots': 'dotplot_alpha_7_beta_3_n_20', 'prior': 'alpha_7_beta_3', 'current': 'alpha_7_beta_3_points_1', 'score': 1, 'outcome': 'FAILURE', 'attribute': 'blame', 'affect': 'negative'},
    		  18: {'name': 'Reinhardt', 'sample': 100, 'dots': 'dotplot_alpha_7_beta_3_n_100','prior': 'alpha_7_beta_3', 'current': 'alpha_7_beta_3_points_1', 'score': 1, 'outcome': 'FAILURE','attribute': 'blame', 'affect': 'negative'},
    		  19: {'name': 'Rosendahl', 'sample': 20, 'dots': 'dotplot_alpha_7_beta_3_n_20','prior': 'alpha_7_beta_3', 'current': 'alpha_7_beta_3_points_3', 'score': 3, 'outcome': 'FAILURE','attribute': 'blame', 'affect': 'negative'},
    		  20: {'name': 'Mack', 'sample': 100, 'dots': 'dotplot_alpha_7_beta_3_n_100','prior': 'alpha_7_beta_3', 'current': 'alpha_7_beta_3_points_3', 'score': 3, 'outcome': 'FAILURE','attribute': 'blame', 'affect': 'negative'},
    		  21: {'name': 'Appleby', 'sample': 20, 'dots': 'dotplot_alpha_7_beta_3_n_20','prior': 'alpha_7_beta_3', 'current': 'alpha_7_beta_3_points_7', 'score': 7, 'outcome': 'SUCCESS','attribute': 'credit', 'affect': 'positive'},
    		  22: {'name': 'Montle', 'sample': 100, 'dots': 'dotplot_alpha_7_beta_3_n_100','prior': 'alpha_7_beta_3', 'current': 'alpha_7_beta_3_points_7', 'score': 7, 'outcome': 'SUCCESS','attribute': 'credit', 'affect': 'positive'},
    		  23: {'name': 'Figueroa', 'sample': 20, 'dots': 'dotplot_alpha_7_beta_3_n_20','prior': 'alpha_7_beta_3', 'current': 'alpha_7_beta_3_points_9', 'score': 9, 'outcome': 'SUCCESS','attribute': 'credit', 'affect': 'positive'},
    		  24: {'name': 'Rossi', 'sample': 100, 'dots': 'dotplot_alpha_7_beta_3_n_100','prior': 'alpha_7_beta_3', 'current': 'alpha_7_beta_3_points_9', 'score': 9, 'outcome': 'SUCCESS','attribute': 'credit', 'affect': 'positive'},
    		  25: {'name': 'Gilsdorf', 'sample': 20,'dots': 'dotplot_alpha_5_beta_5_n_20', 'prior': 'alpha_6_beta_6', 'current': 'alpha_6_beta_6_points_5', 'score': 5, 'outcome': 'SUCCESS', 'attribute': 'credit', 'affect': 'positive'},
    		  26: {'name': 'Braley', 'sample': 100, 'dots': 'dotplot_alpha_5_beta_5_n_100','prior': 'alpha_6_beta_6', 'current': 'alpha_6_beta_6_points_5', 'score': 5, 'outcome': 'SUCCESS','attribute': 'credit', 'affect': 'positive'},
    		  27: {'name': 'Kirby', 'sample': 20,'dots': 'dotplot_alpha_3_beta_7_n_20', 'prior': 'alpha_3_beta_7', 'current': 'alpha_3_beta_7_points_4', 'score': 4, 'outcome': 'FAILURE', 'attribute': 'blame', 'affect': 'negative'},
    		  28: {'name': 'Walters', 'sample': 100, 'dots': 'dotplot_alpha_3_beta_7_n_100','prior': 'alpha_3_beta_7', 'current': 'alpha_3_beta_7_points_4', 'score': 4, 'outcome': 'FAILURE','attribute': 'blame', 'affect': 'negative'},
    		  29: {'name': 'Winten', 'sample': 20,'dots': 'dotplot_alpha_7_beta_3_n_20', 'prior': 'alpha_7_beta_3', 'current': 'alpha_7_beta_3_points_6', 'score': 6, 'outcome': 'SUCCESS', 'attribute': 'credit', 'affect': 'positive'},
    		  30: {'name': 'Butler', 'sample': 100, 'dots': 'dotplot_alpha_7_beta_3_n_100','prior': 'alpha_7_beta_3', 'current': 'alpha_7_beta_3_points_6', 'score': 6, 'outcome': 'SUCCESS','attribute': 'credit', 'affect': 'positive'},
    		  31: {'name': 'Sandoval', 'sample': 20,'dots': 'dotplot_alpha_1.5_beta_3.5_n_20', 'prior': 'alpha_1.5_beta_3.5', 'current': 'alpha_1.5_beta_3.5_points_2', 'score': 2, 'outcome': 'FAILURE', 'attribute': 'blame', 'affect': 'negative'},
    		  32: {'name': 'Ekberg', 'sample': 100, 'dots': 'dotplot_alpha_1.5_beta_3.5_n_100','prior': 'alpha_1.5_beta_3.5', 'current': 'alpha_1.5_beta_3.5_points_4', 'score': 4, 'outcome': 'FAILURE','attribute': 'blame', 'affect': 'negative'},
    		  33: {'name': 'Pegram', 'sample': 100,'dots': 'dotplot_alpha_6_beta_14_n_100', 'prior': 'alpha_6_beta_14', 'current': 'alpha_6_beta_14_points_2', 'score': 2, 'outcome': 'FAILURE', 'attribute': 'blame', 'affect': 'negative'},
    		  34: {'name': 'Miller', 'sample': 20, 'dots': 'dotplot_alpha_6_beta_14_n_20','prior': 'alpha_6_beta_14', 'current': 'alpha_6_beta_14_points_3', 'score': 3, 'outcome': 'FAILURE','attribute': 'blame', 'affect': 'negative'},
    		  35: {'name': 'Nadiak', 'sample': 20,'dots': 'dotplot_alpha_2.5_beta_2.5_n_20', 'prior': 'alpha_2.5_beta_2.5', 'current': 'alpha_2.5_beta_2.5_points_4', 'score': 4, 'outcome': 'FAILURE', 'attribute': 'blame', 'affect': 'negative'},
    		  36: {'name': 'Petrelli', 'sample': 100, 'dots': 'dotplot_alpha_2.5_beta_2.5_n_100','prior': 'alpha_2.5_beta_2.5', 'current': 'alpha_2.5_beta_2.5_points_6', 'score': 6, 'outcome': 'SUCCESS','attribute': 'credit', 'affect': 'positive'},
    		  37: {'name': 'Edmisson', 'sample': 20,'dots': 'dotplot_alpha_10_beta_10_n_20', 'prior': 'alpha_10_beta_10', 'current': 'alpha_10_beta_10_points_5', 'score': 5, 'outcome': 'SUCCESS', 'attribute': 'credit', 'affect': 'positive'},
    		  38: {'name': 'Morris', 'sample': 100, 'dots': 'dotplot_alpha_10_beta_10_n_100','prior': 'alpha_10_beta_10', 'current': 'alpha_10_beta_10_points_7', 'score': 7, 'outcome': 'SUCCESS','attribute': 'credit', 'affect': 'positive'},
    		  39: {'name': 'Shannon', 'sample': 100,'dots': 'dotplot_alpha_3.5_beta_1.5_n_100', 'prior': 'alpha_3.5_beta_1.5', 'current': 'alpha_3.5_beta_1.5_points_6', 'score': 6, 'outcome': 'SUCCESS', 'attribute': 'credit', 'affect': 'positive'},
    		  40: {'name': 'Lewis', 'sample': 20, 'dots': 'dotplot_alpha_3.5_beta_1.5_n_20','prior': 'alpha_3.5_beta_1.5', 'current': 'alpha_3.5_beta_1.5_points_8', 'score': 8, 'outcome': 'SUCCESS','attribute': 'credit', 'affect': 'positive'},
    		  41: {'name': 'Sisson', 'sample': 100,'dots': 'dotplot_alpha_14_beta_6_n_100', 'prior': 'alpha_14_beta_6', 'current': 'alpha_14_beta_6_points_9', 'score': 9, 'outcome': 'SUCCESS', 'attribute': 'credit', 'affect': 'positive'},
    		  42: {'name': 'McCallum', 'sample': 20, 'dots': 'dotplot_alpha_14_beta_6_n_20','prior': 'alpha_14_beta_6', 'current': 'alpha_14_beta_6_points_10', 'score': 10, 'outcome': 'SUCCESS','attribute': 'credit', 'affect': 'positive'}
    		  }


class Subsession(BaseSubsession):
	def creating_session(self):
		treatments = itertools.cycle(['random', 'experience'])
		image_index = self.round_number - 1
		print(image_index)

		# assigns treatment at the participant level so that same treatment
        # persists across rounds
		if self.round_number == 1:
			for p in self.get_players():
				if 'treatment' in self.session.config:
					# demo mode
					treatment = self.session.config['treatment']
					p.participant.vars['treatment'] = treatment
					p.treatment = treatment
				else:
					# live experiment mode
					treatment = next(treatments)
					p.participant.vars['treatment'] = treatment
					p.treatment = treatment
		else:
			for p in self.get_players():
				treatment = p.participant.vars['treatment']
				p.treatment = treatment

		if self.round_number == 1:
			for p in self.get_players():
				# copy in the stimuli keys and shuffle them
				people = Constants.people.copy()
				people_sequence = list(range(1, 43))
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
				p.stim_outcome = people[stim_id]['outcome']
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
				p.stim_outcome = people[stim_id]['outcome']
				p.stim_attribute = people[stim_id]['attribute']
				p.stim_affect = people[stim_id]['affect']
	    	

class Group(BaseGroup):
    pass


class Player(BasePlayer):
	treatment = models.CharField()
	comprehension1 = models.IntegerField(
        choices=[[1, '5 points'],[2, '7 points'], [3, '4 points']],
        widget=widgets.RadioSelect
        )
	comprehension2 = models.IntegerField(
        choices=[[1, 'Marking the score with a light gray color'],
        		[2, 'Marking the score with a black dot'], 
        		[3, 'Marking the score with a dark red color']],
        widget=widgets.RadioSelect
        )
	comprehension3 = models.IntegerField(
        choices=[[1, 'Each dot represents one of the points the gymnast earned today'],
        		[2, 'Each dot represents a score the gymnast earned in a past competition'], 
        		[3, 'Each dot represents a special move performed by the gymnast']],
        widget=widgets.RadioSelect
        )
	comprehension4 = models.IntegerField(
        choices=[[1, '5 points'],[2, '7 points'], [3, '2 points']],
        widget=widgets.RadioSelect
        )

	stim_id = models.CharField()
	stim_name = models.CharField()
	stim_sample = models.IntegerField()
	stim_dots = models.CharField()
	stim_prior = models.CharField()
	stim_current = models.CharField()
	stim_score = models.CharField()
	stim_outcome = models.CharField()
	stim_attribute = models.CharField()
	stim_affect = models.CharField()

	prediction = models.IntegerField(
    	widget=widgets.Slider(attrs={'step': '1.00'},
    		show_value=False))

	attribution = models.IntegerField(
    	widget=widgets.Slider(attrs={'step': '1.00'},
    		show_value=False))

