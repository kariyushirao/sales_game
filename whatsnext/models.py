from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import random
import itertools

author = 'Kariyushi'

doc = """
Participants observe sequences of 8 coin flips.  At the end of each sequence, participants are
asked to guess whether the ninth flip will land on heads and tails.
"""


class Constants(BaseConstants):
    name_in_url = 'whatsnext'
    players_per_group = None
    num_rounds = 13

    # coin stimuli
    coins = {1: {'file': 'THTHHHTH.gif'}, 2: {'file': 'HTHTTTHT.gif'}, 3: {'file': 'HTHHTHTT.gif'}, 4: {'file': 'THTTHTHH.gif'},
    		 5: {'file': 'THTHHTTT.gif'}, 6: {'file': 'HTHTTHHH.gif'}, 7: {'file': 'HHTHTTTT.gif'}, 8: {'file': 'TTHTHHHH.gif'},
    		 9: {'file': 'THTHHHHH.gif'}, 10: {'file': 'HTHTTTTT.gif'}, 11: {'file': 'THTTTTTT.gif'}, 12: {'file': 'HTHHHHHH.gif'},
    		 13: {'file': 'HTTTTTTT.gif'}, 14: {'file': 'THHHHHHH.gif'}, 15: {'file': 'HTHHTHTH.gif'}, 16: {'file': 'HTHTTHTH.gif'},
    		 17: {'file': 'HTTHTTHT.gif'}, 18: {'file': 'THHTHTHT.gif'}, 19: {'file': 'TTHHTTHT.gif'}, 20: {'file': 'THTTHHTH.gif'}
    		 }

    # analyst stimuli
    analysts = {1: {'file': 'DUDUUUDU.gif'}, 2: {'file': 'UDUDDDUD.gif'}, 3: {'file': 'UDUUDUDD.gif'}, 4: {'file': 'DUDDUDUU.gif'},
    		 5: {'file': 'UDUDDUUU.gif'}, 6: {'file': 'DUDUUDDD.gif'}, 7: {'file': 'UUDUDDDD.gif'}, 8: {'file': 'DDUDUUUU.gif'},
    		 9: {'file': 'UDUDDDDD.gif'}, 10: {'file': 'DUDUUUUU.gif'}, 11: {'file': 'UDUUUUUU.gif'}, 12: {'file': 'DUDDDDDD.gif'},
    		 13: {'file': 'DUUUUUUU.gif'}, 14: {'file': 'UDDDDDDD.gif'}, 15: {'file': 'UDUUDUDU.gif'}, 16: {'file': 'UDUDDUDU.gif'},
    		 17: {'file': 'UDDUDDUD.gif'}, 18: {'file': 'DUUDUDUD.gif'}, 19: {'file': 'DDUUDDUD.gif'}, 20: {'file': 'DUDDUUDU.gif'}
    		 }

class Subsession(BaseSubsession):
	def creating_session(self):
		treatments = itertools.cycle(['coins','analyst'])

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

		image_index = self.round_number - 1

		if self.round_number == 1:
			for p in self.get_players():
				opening_streak = {}
				opening_keys = []
				two_streak = {}
				two_keys = []
				three_streak = {}
				three_keys = []
				four_streak = {}
				four_keys = []
				five_streak = {}
				five_keys = []
				six_streak = {}
				six_keys = []
				seven_streak = {}
				seven_keys = []
				filler_streak = {}

				# copy in the stimuli and construct key lists
				if treatment == 'coins':
					coins = Constants.coins.copy()
					opening_streak = {key:coins[key] for key in [1, 2]}
					opening_keys = list(opening_streak.keys())
					two_streak = {key:coins[key] for key in [3, 4]}
					two_keys = list(two_streak.keys())
					three_streak = {key:coins[key] for key in [5, 6]}
					three_keys = list(three_streak.keys())
					four_streak = {key:coins[key] for key in [7, 8]}
					four_keys = list(four_streak.keys())
					five_streak = {key:coins[key] for key in [9, 10]}
					five_keys = list(five_streak.keys())
					six_streak = {key:coins[key] for key in [11, 12]}
					six_keys = list(six_streak.keys())
					seven_streak = {key:coins[key] for key in [13, 14]}
					seven_keys = list(seven_streak.keys())
					filler_streak = {key:coins[key] for key in [15, 16, 17, 18, 19, 20]}
				else:
					analysts = Constants.analysts.copy()
					opening_streak = {key:analysts[key] for key in [1, 2]}
					opening_keys = list(opening_streak.keys())
					two_streak = {key:analysts[key] for key in [3, 4]}
					two_keys = list(two_streak.keys())
					three_streak = {key:analysts[key] for key in [5, 6]}
					three_keys = list(three_streak.keys())
					four_streak = {key:analysts[key] for key in [7, 8]}
					four_keys = list(four_streak.keys())
					five_streak = {key:analysts[key] for key in [9, 10]}
					five_keys = list(five_streak.keys())
					six_streak = {key:analysts[key] for key in [11, 12]}
					six_keys = list(six_streak.keys())
					seven_streak = {key:analysts[key] for key in [13, 14]}
					seven_keys = list(seven_streak.keys())
					filler_streak = {key:analysts[key] for key in [15, 16, 17, 18, 19, 20]}

				# shuffle opening sequence and streaks
				# select first object from each shuffled list
				random.shuffle(opening_keys)
				first_opening_key = opening_keys[0]
				first_sequence = opening_streak[first_opening_key]['file'] 

				random.shuffle(two_keys)
				first_two_key = two_keys[0]
				second_sequence = two_streak[first_two_key]['file'] 

				random.shuffle(three_keys)
				first_three_key = three_keys[0]
				third_sequence = three_streak[first_three_key]['file']

				random.shuffle(four_keys)
				first_four_key = four_keys[0]
				fourth_sequence = four_streak[first_four_key]['file']

				random.shuffle(five_keys)
				first_five_key = five_keys[0]
				fifth_sequence = five_streak[first_five_key]['file']

				random.shuffle(six_keys)
				first_six_key = six_keys[0]
				sixth_sequence = six_streak[first_six_key]['file']

				random.shuffle(seven_keys)
				first_seven_key = seven_keys[0]
				seventh_sequence = seven_streak[first_seven_key]['file']

				# pull objects out of fillers list
				fillers = []
				fillers.extend((filler_streak[15]['file'], filler_streak[16]['file'], filler_streak[17]['file'], 
					filler_streak[18]['file'], filler_streak[19]['file'], filler_streak[20]['file']))

				# append streaks to fillers list
				all_sequences = fillers
				all_sequences.extend((second_sequence, third_sequence, fourth_sequence, fifth_sequence,
					sixth_sequence, seventh_sequence))

				# shuffle streaks and fillers
				random.shuffle(all_sequences)

				# add opening sequence
				all_sequences.insert(0, first_sequence)

				p.participant.vars['all_sequences'] = all_sequences
				stimuli_list = p.participant.vars['all_sequences']
				p.image_name = stimuli_list[image_index]

		else:
			for p in self.get_players():
				stimuli_list = p.participant.vars['all_sequences']
				p.image_name = stimuli_list[image_index]
	    	

class Group(BaseGroup):
    pass


class Player(BasePlayer):
	treatment = models.CharField()
	prediction_slider = models.IntegerField(
    	widget=widgets.Slider(attrs={'step': '1.00'},
    		show_value=False))
	image_name = models.CharField()

