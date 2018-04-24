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
    name_in_url = 'coin_flipping'
    players_per_group = None
    num_rounds = 11

    # lists of image ids
    first_sequence = [1,2]
    	# no. 1: THTHHHTH
   		# no. 2: HTHTTTHT
    two_streak = [3,4]
    	# no. 3: HTHHTHTT
    	# no. 4: THTTHTHH
    three_streak = [5,6]
    	# no. 5: THTHHTTT
    	# no. 6: HTHTTHHH
    four_streak = [7,8]
    	# no. 7: HHTHTTTT
    	# no. 8: TTHTHHHH
    five_streak = [9,10]
    	# no. 9: THTHHHHH
    	# no. 10: HTHTTTTT
    six_streak = [11,12]
    	# no. 11: HTHHHHHH
    	# no. 12: THTTTTTT
    fillers = [13,14,15,16,17]
    	# no. 13: HTHHTTTH
    	# no. 14: HHTHTTHT
    	# no. 15: HTTHTHTH
    	# no. 16: THHTHTHT
    	# no. 17: TTHHHTHT


class Subsession(BaseSubsession):
	def creating_session(self):
		treatments = itertools.cycle(['slider','radial'])

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
		print(image_index)

		if self.round_number == 1:
			for p in self.get_players():
				# copy in the stimuli IDs
				first_sequence = Constants.first_sequence.copy()
				two_streak = Constants.two_streak.copy() 
				three_streak = Constants.three_streak.copy()
				four_streak = Constants.four_streak.copy()
				five_streak = Constants.five_streak.copy()
				six_streak = Constants.six_streak.copy()
				fillers = Constants.fillers.copy()
				
				# shuffle opening sequence and streaks
				random.shuffle(first_sequence)
				first_sequence = first_sequence[0]

				random.shuffle(two_streak)
				two_streak = two_streak[0]

				random.shuffle(three_streak)
				three_streak = three_streak[0]

				random.shuffle(four_streak)
				four_streak = four_streak[0]

				random.shuffle(five_streak)
				five_streak = five_streak[0]

				random.shuffle(six_streak)
				six_streak = six_streak[0]

				# append first object in each streak list to fillers list
				eleven_sequence = fillers
				fillers.extend((two_streak, three_streak, four_streak, five_streak, six_streak))

				print(eleven_sequence)

				# shuffle streaks and fillers
				random.shuffle(eleven_sequence)
				print(eleven_sequence)

				# add starting sequence
				eleven_sequence.insert(0, first_sequence)
				print(eleven_sequence)

				p.participant.vars['eleven_sequence'] = eleven_sequence
				print(p.participant.vars['eleven_sequence'])
				flips_list = p.participant.vars['eleven_sequence']
				print(flips_list)
				p.image_id = flips_list[image_index]
				print(p.image_id)
		else:
			for p in self.get_players():
				flips_list = p.participant.vars['eleven_sequence']
				p.image_id = flips_list[image_index]
	    	

class Group(BaseGroup):
    pass


class Player(BasePlayer):
	treatment = models.CharField()
	flip_prediction_slider = models.IntegerField(
    	widget=widgets.Slider(attrs={'step': '1.00'},
    		show_value=False))
	flip_prediction_radial = models.IntegerField(
    	choices=[[1, 'Heads'],[2, 'Tails']],
        widget=widgets.RadioSelect
        )
	image_id = models.CharField()

