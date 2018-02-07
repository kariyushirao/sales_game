from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Instructions(Page):
    def is_displayed(self):
        return self.round_number == 1


class JudgePicture(Page):
	form_model = models.Player
	form_fields = ['snowy_label']

	def vars_for_template(self):
		return {
			'image_path': 'snowy_pictures/pictures/{}.png'.format(self.round_number)
        }


class Results(Page):
    def is_displayed(self):
        return self.round_number >= 4


page_sequence = [
    Instructions,
    JudgePicture,
    Results
]
