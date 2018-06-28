from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Consent(Page):
    def is_displayed(self):
        return self.round_number == 1

class InstructionsCoin(Page):
    def is_displayed(self):
        return self.round_number == 1 and self.participant.vars['treatment'] == 'coins'

class InstructionsAnalyst(Page):
    def is_displayed(self):
        return self.round_number == 1 and self.participant.vars['treatment'] == 'analyst'


class PredictCoin(Page):
    def is_displayed(self):
        return self.participant.vars['treatment'] == 'coins'

    form_model = models.Player
    form_fields = ['prediction_slider']

    def vars_for_template(self):
        return {
			'image_path': 'whatsnext/pictures/{}'.format(self.player.image_name)
        }

class PredictAnalyst(Page):
    def is_displayed(self):
        return self.participant.vars['treatment'] == 'analyst'

    form_model = models.Player
    form_fields = ['prediction_slider']

    def vars_for_template(self):
        return {
            'image_path': 'whatsnext/pictures/{}'.format(self.player.image_name)
        }


class Results(Page):
    def is_displayed(self):
        return self.round_number >= 13


page_sequence = [
    Consent,
    InstructionsCoin,
    InstructionsAnalyst,
    PredictCoin,
    PredictAnalyst,
    Results
]
