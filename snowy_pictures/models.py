from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import random

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'visual_perception'
    players_per_group = None
    num_rounds = 24

    # list of image ids
    snowy_pictures = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]


class Subsession(BaseSubsession):
	def creating_session(self):    

		image_index = self.round_number - 1
		print(image_index)


		if self.round_number == 1:
			for p in self.get_players():
				snowy_pictures = Constants.snowy_pictures.copy()
				print(snowy_pictures)
				random.shuffle(snowy_pictures)
				print(snowy_pictures)
				p.participant.vars['snowy_pictures'] = snowy_pictures
				print(p.participant.vars['snowy_pictures'])
				snowy_list = p.participant.vars['snowy_pictures']
				print(snowy_list)
				p.image_id = snowy_list[image_index]
				print(p.image_id)
		else:
			for p in self.get_players():
				snowy_list = p.participant.vars['snowy_pictures']
				p.image_id = snowy_list[image_index]
	    	

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    snowy_label = models.TextField(widget=widgets.Textarea(attrs={'cols':'10','rows':'5'}))
    image_id = models.CharField()

