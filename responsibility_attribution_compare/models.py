from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import random
import itertools

author = '(c) Kariyushi Rao, 2018'

doc = """
Participants are shown performance history and current scores for pairs of individual competitors in a tournament. 
Participants are asked to decide whether the agents deserve equal, less, or more credit or blame for their 
individual performances, compared with each other.
"""


class Constants(BaseConstants):
    name_in_url = 'responsibility_attribution_compare'
    players_per_group = None
    num_rounds = 3

    # stimuli
    pairs = {1: {'gymnast1': {'name': 'Page', 'sample': 20,'dots': 'dotplot_alpha_3_beta_7_n_20', 'current': 'alpha_3_beta_7_points_1', 'score': 1},
    			 'gymnast2': {'name': 'Walker', 'sample': 20,'dots': 'dotplot_alpha_7_beta_3_n_20', 'current': 'alpha_7_beta_3_points_1', 'score': 1},
    			 'outcome': 'FAILURE', 'attribute': 'blame'
    			},
    		 2: {'gymnast1': {'name': 'Nelson', 'sample': 100,'dots': 'dotplot_alpha_5_beta_5_n_100', 'current': 'alpha_6_beta_6_points_7', 'score': 7},
    			 'gymnast2': {'name': 'Samuels', 'sample': 100,'dots': 'dotplot_alpha_5_beta_5_n_100', 'current': 'alpha_6_beta_6_points_9', 'score': 9},
    			 'outcome': 'SUCCESS', 'attribute': 'credit'
    			},
    		 3: {'gymnast1': {'name': 'Williams', 'sample': 20,'dots': 'dotplot_alpha_5_beta_5_n_20', 'current': 'alpha_6_beta_6_points_3', 'score': 3},
    			 'gymnast2': {'name': 'Guerrieri', 'sample': 100,'dots': 'dotplot_alpha_5_beta_5_n_100', 'current': 'alpha_6_beta_6_points_3', 'score': 3},
    			 'outcome': 'FAILURE', 'attribute': 'blame'
    			}
    		  }


class Subsession(BaseSubsession):
	def creating_session(self):
		# order counterbalances display of stimuli (right or left side of screen)
		order = itertools.cycle([1, 2])
		image_index = self.round_number - 1
		print(image_index)

		if self.round_number == 1:
			for p in self.get_players():
				# copy in the stimuli keys and shuffle them
				pairs = Constants.pairs.copy()
				pairs_sequence = list(range(1, 4))
				print(pairs_sequence)

				random.shuffle(pairs_sequence)
				print(pairs_sequence)
				
				# record sequence of stimuli as participant variable
				p.participant.vars['pairs_sequence'] = pairs_sequence
				print(p.participant.vars['pairs_sequence'])

				pairs_list = pairs_sequence
				print(pairs_list)
				print(pairs_list[image_index])
				
				# record stim attributes
				pair_id = pairs_list[image_index]
				print(pair_id)
				p.pair_id = pair_id
				p.pair_outcome = pairs[pair_id]['outcome']
				print(pairs[pair_id]['outcome'])
				print(p.pair_outcome)
				p.pair_attribute = pairs[pair_id]['attribute']
				print(pairs[pair_id]['attribute'])
				print(p.pair_attribute)
				print(pair_id)
				if order == 1:
					p.stim_name1 = pairs[pair_id]['gymnast1']['name']
					p.stim_sample1 = pairs[pair_id]['gymnast1']['sample']
					p.stim_dots1 = pairs[pair_id]['gymnast1']['dots']
					p.stim_current1 = pairs[pair_id]['gymnast1']['current']
					p.stim_score1 = pairs[pair_id]['gymnast1']['score']

					p.stim_name2 = pairs[pair_id]['gymnast2']['name']
					p.stim_sample2 = pairs[pair_id]['gymnast2']['sample']
					p.stim_dots2 = pairs[pair_id]['gymnast2']['dots']
					p.stim_current2 = pairs[pair_id]['gymnast2']['current']
					p.stim_score2 = pairs[pair_id]['gymnast2']['score']
				else:
					p.stim_name1 = pairs[pair_id]['gymnast2']['name']
					p.stim_sample1 = pairs[pair_id]['gymnast2']['sample']
					p.stim_dots1 = pairs[pair_id]['gymnast2']['dots']
					p.stim_current1 = pairs[pair_id]['gymnast2']['current']
					p.stim_score1 = pairs[pair_id]['gymnast2']['score']

					p.stim_name2 = pairs[pair_id]['gymnast1']['name']
					p.stim_sample2 = pairs[pair_id]['gymnast1']['sample']
					p.stim_dots2 = pairs[pair_id]['gymnast1']['dots']
					p.stim_current2 = pairs[pair_id]['gymnast1']['current']
					p.stim_score2 = pairs[pair_id]['gymnast1']['score']

		else:
			for p in self.get_players():
				pairs = Constants.pairs.copy()

				# pull sequence of stimuli out of participant vars as list
				pairs_list = p.participant.vars['pairs_sequence']
				
				# record stim attributes
				pair_id = pairs_list[image_index]
				p.pair_id = pair_id
				p.pair_outcome = pairs[pair_id]['outcome']
				p.pair_attribute = pairs[pair_id]['attribute']
				if order == 1:
					p.stim_name1 = pairs[pair_id]['gymnast1']['name']
					p.stim_sample1 = pairs[pair_id]['gymnast1']['sample']
					p.stim_dots1 = pairs[pair_id]['gymnast1']['dots']
					p.stim_current1 = pairs[pair_id]['gymnast1']['current']
					p.stim_score1 = pairs[pair_id]['gymnast1']['score']

					p.stim_name2 = pairs[pair_id]['gymnast2']['name']
					p.stim_sample2 = pairs[pair_id]['gymnast2']['sample']
					p.stim_dots2 = pairs[pair_id]['gymnast2']['dots']
					p.stim_current2 = pairs[pair_id]['gymnast2']['current']
					p.stim_score2 = pairs[pair_id]['gymnast2']['score']
				else:
					p.stim_name1 = pairs[pair_id]['gymnast2']['name']
					p.stim_sample1 = pairs[pair_id]['gymnast2']['sample']
					p.stim_dots1 = pairs[pair_id]['gymnast2']['dots']
					p.stim_current1 = pairs[pair_id]['gymnast2']['current']
					p.stim_score1 = pairs[pair_id]['gymnast2']['score']

					p.stim_name2 = pairs[pair_id]['gymnast1']['name']
					p.stim_sample2 = pairs[pair_id]['gymnast1']['sample']
					p.stim_dots2 = pairs[pair_id]['gymnast1']['dots']
					p.stim_current2 = pairs[pair_id]['gymnast1']['current']
					p.stim_score2 = pairs[pair_id]['gymnast1']['score']
	    	

class Group(BaseGroup):
    pass


class Player(BasePlayer):
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

	pair_id = models.IntegerField()
	pair_outcome = models.CharField()
	pair_attribute = models.CharField()
	stim_name1 = models.CharField()
	stim_name1 = models.CharField()
	stim_name2 = models.CharField()
	stim_sample1 = models.IntegerField()
	stim_sample2 = models.IntegerField()
	stim_dots1 = models.CharField()
	stim_dots2 = models.CharField()
	stim_current1 = models.CharField()
	stim_current2 = models.CharField()
	stim_score1 = models.CharField()
	stim_score2 = models.CharField()

	attribution = models.IntegerField(
    	widget=widgets.Slider(attrs={'step': '1.00'},
    		show_value=False))

