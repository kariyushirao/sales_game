from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Instructions1(Page):
    def is_displayed(self):
        return self.round_number == 1

class Instructions2(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'dots1': 'responsibility_attribution/pictures/Avis0.png',
            'dots2': 'responsibility_attribution/pictures/Selle0.png',
            'heat1': 'responsibility_attribution/pictures/Avis1.png',
            'heat2': 'responsibility_attribution/pictures/Selle1.png'
        }

class Instructions3(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'curr1': 'responsibility_attribution/pictures/Avis2.png',
            'curr2': 'responsibility_attribution/pictures/Selle2.png'
        }

class Comprehension(Page):
    def is_displayed(self):
        return self.round_number == 1

    form_model = models.Player
    form_fields = ['comprehension1', 'comprehension2', 'comprehension3', 'comprehension4']

    def vars_for_template(self):
        return {
            'curr': 'responsibility_attribution/pictures/Williams2.png'
        }

    def error_message(self, values):
        print('values are', values)
        threshold = (values['comprehension1'] == 1)
        color = (values['comprehension2'] == 3)
        dots = (values['comprehension3'] == 2)
        score = (values['comprehension4'] == 2)
        if not (threshold and color and dots and score):
            return 'It looks like you may have answered one or more questions incorrectly.  Please check your answers and correct any mistakes.'

class Prediction(Page):
    form_model = models.Player
    form_fields = ['prediction']

    def vars_for_template(self):
        return {
            'dots': 'responsibility_attribution/pictures/{}.png'.format(self.player.stim_dots),
			'heat_map': 'responsibility_attribution/pictures/{}.png'.format(self.player.stim_prior),
            'name': self.player.stim_name
        }

class Responsibility(Page):
    form_model = models.Player
    form_fields = ['attribution']

    def vars_for_template(self):
        return {
            'dots': 'responsibility_attribution/pictures/{}.png'.format(self.player.stim_dots),
            'heat_map': 'responsibility_attribution/pictures/{}.png'.format(self.player.stim_current),
            'name': self.player.stim_name,
            'score': self.player.stim_score
        }


class Results(Page):
    def is_displayed(self):
        return self.round_number >= 3


page_sequence = [
    Instructions1,
    Instructions2,
    Instructions3,
    Comprehension,
    Prediction,
    Responsibility,
    Results
]
