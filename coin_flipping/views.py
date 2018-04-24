from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Instructions(Page):
    def is_displayed(self):
        return self.round_number == 1


class PredictFlipSlider(Page):
    def is_displayed(self):
        return self.participant.vars['treatment'] == 'slider'

    form_model = models.Player
    form_fields = ['flip_prediction_slider']

    # def flip_prediction_choices(self):
    #     choices = ['Heads', 'Tails']
    #     random.shuffle(choices)
    #     return choices

    def vars_for_template(self):
        return {
			'image_path': 'coin_flipping/pictures/{}.gif'.format(self.player.image_id)
        }

class PredictFlipRadial(Page):
    def is_displayed(self):
        return self.participant.vars['treatment'] == 'radial'

    form_model = models.Player
    form_fields = ['flip_prediction_radial']

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
    PredictFlipSlider,
    PredictFlipRadial,
    Results
]
