from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Instructions(Page):
    def is_displayed(self):
        return self.round_number == 1


class PredictFlip(Page):
	form_model = models.Player
	form_fields = ['flip_prediction']

    # def flip_prediction_choices(self):
    #     choices = ['Heads', 'Tails']
    #     random.shuffle(choices)
    #     return choices

	def vars_for_template(self):
		return {
			'image_path': 'coin_flipping/pictures/{}.gif'.format(self.player.image_id)
        }


class Results(Page):
    def is_displayed(self):
        return self.round_number >= 11


page_sequence = [
    Instructions,
    PredictFlip,
    Results
]
