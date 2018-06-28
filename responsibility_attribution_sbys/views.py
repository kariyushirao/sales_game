from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Consent(Page):
    def is_displayed(self):
        return self.round_number == 1

class Instructions1(Page):
    def is_displayed(self):
        return self.round_number == 1

class Instructions2R(Page):
    def is_displayed(self):
        return self.round_number == 1 and self.participant.vars['treatment'] == 'random'
    
    def vars_for_template(self):
        return {
            # these file names refer to specific items in the ../templates/responsibility_attribution
            # folder - make sure you have images in that folder that match these file names, or 
            # change the file names to reflect which images you wish to use
            'dots1': 'responsibility_attribution/pictures/Smith_dots.png',
            'dots2': 'responsibility_attribution/pictures/Jarrod_dots.png',
            'heat1': 'responsibility_attribution/pictures/Smith_prior.png',
            'heat2': 'responsibility_attribution/pictures/Jarrod_prior.png'
        }


class Instructions2E(Page):
    def is_displayed(self):
        return self.round_number == 1 and self.participant.vars['treatment'] == 'experience'

    def vars_for_template(self):
        return {
            'dots1': 'responsibility_attribution/pictures/Smith_dots.png',
            'dots2': 'responsibility_attribution/pictures/Jarrod_dots.png',
            'heat1': 'responsibility_attribution/pictures/Smith_prior.png',
            'heat2': 'responsibility_attribution/pictures/Jarrod_prior.png'
        }

class Instructions3(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'curr1': 'responsibility_attribution/pictures/Smith_current.png',
            'curr2': 'responsibility_attribution/pictures/Jarrod_current.png'
        }

class Comprehension(Page):
    def is_displayed(self):
        return self.round_number == 1

    form_model = models.Player
    form_fields = ['comprehension1', 'comprehension2', 'comprehension3', 'comprehension4']

    def vars_for_template(self):
        return {
            'curr': 'responsibility_attribution/pictures/Nussbaum_current.png'
        }

    def error_message(self, values):
        print('values are', values)
        threshold = (values['comprehension1'] == 1)
        color = (values['comprehension2'] == 3)
        dots = (values['comprehension3'] == 2)
        score = (values['comprehension4'] == 2)
        if not (threshold and color and dots and score):
            return 'It looks like you may have answered one or more questions incorrectly.  Please check your answers and correct any mistakes.'

class PredictionR(Page):
    def is_displayed(self):
        return self.participant.vars['treatment'] == 'random'

    form_model = models.Player
    form_fields = ['prediction']

    def vars_for_template(self):
        return {
            'dots': 'responsibility_attribution/pictures/{}.png'.format(self.player.stim_dots),
			'heat_map': 'responsibility_attribution/pictures/{}.png'.format(self.player.stim_prior),
            'name': self.player.stim_name
        }

class PredictionE(Page):
    def is_displayed(self):
        return self.participant.vars['treatment'] == 'experience'

    form_model = models.Player
    form_fields = ['prediction']

    def vars_for_template(self):
        return {
            'dots': 'responsibility_attribution/pictures/{}.png'.format(self.player.stim_dots),
            'heat_map': 'responsibility_attribution/pictures/{}.png'.format(self.player.stim_prior),
            'name': self.player.stim_name
        }

class ResponsibilityE(Page):
    def is_displayed(self):
        return self.participant.vars['treatment'] == 'experience'

    form_model = models.Player
    form_fields = ['attribution']

    def vars_for_template(self):
        return {
            'dots': 'responsibility_attribution/pictures/{}.png'.format(self.player.stim_dots),
            'heat_map': 'responsibility_attribution/pictures/{}.png'.format(self.player.stim_current),
            'name': self.player.stim_name,
            'score': self.player.stim_score,
            'outcome': self.player.stim_outcome
        }

class ResponsibilityR(Page):
    def is_displayed(self):
        return self.participant.vars['treatment'] == 'random'

    form_model = models.Player
    form_fields = ['attribution']

    def vars_for_template(self):
        return {
            'dots': 'responsibility_attribution/pictures/{}.png'.format(self.player.stim_dots),
            'heat_map': 'responsibility_attribution/pictures/{}.png'.format(self.player.stim_current),
            'name': self.player.stim_name,
            'score': self.player.stim_score,
            'outcome': self.player.stim_outcome
        }

class Results(Page):
    def is_displayed(self):
        return self.round_number >= 42


page_sequence = [
    Consent,
    Instructions1,
    Instructions2E,
    Instructions2R,
    Instructions3,
    Comprehension,
    PredictionE,
    PredictionR,
    ResponsibilityE,
    ResponsibilityR,
    Results
]
