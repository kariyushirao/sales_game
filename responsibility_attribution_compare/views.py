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

class Instructions2(Page):
    def is_displayed(self):
        return self.round_number == 1 
    
    def vars_for_template(self):
        return {
            # these file names refer to specific items in the ../templates/responsibility_attribution
            # folder - make sure you have images in that folder that match these file names, or 
            # change the file names to reflect which images you wish to use
            'dots1': 'responsibility_attribution_compare/pictures/Smith_dots.png',
            'dots2': 'responsibility_attribution_compare/pictures/Jarrod_dots.png'
        }

class Instructions3(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'curr1': 'responsibility_attribution_compare/pictures/Smith_current.png',
            'curr2': 'responsibility_attribution_compare/pictures/Jarrod_current.png'
        }

class Comprehension(Page):
    def is_displayed(self):
        return self.round_number == 1

    form_model = models.Player
    form_fields = ['comprehension1', 'comprehension3', 'comprehension4']

    def vars_for_template(self):
        return {
            'curr': 'responsibility_attribution_compare/pictures/Nussbaum_current.png'
        }

    def error_message(self, values):
        print('values are', values)
        threshold = (values['comprehension1'] == 1)
        dots = (values['comprehension3'] == 2)
        score = (values['comprehension4'] == 2)
        if not (threshold and dots and score):
            return 'It looks like you may have answered one or more questions incorrectly.  Please check your answers and correct any mistakes.'

class Responsibility(Page):
    form_model = models.Player
    form_fields = ['attribution']

    def vars_for_template(self):
        return {
            'current1': 'responsibility_attribution_compare/pictures/{}.png'.format(self.player.stim_current1),
            'current2': 'responsibility_attribution_compare/pictures/{}.png'.format(self.player.stim_current2),
            'name1': self.player.stim_name1,
            'name2': self.player.stim_name2,
            'sample1': self.player.stim_sample1,
            'sample2': self.player.stim_sample2,
            'score1': self.player.stim_score1,
            'score2': self.player.stim_score2,
            'outcome': self.player.pair_outcome,
            'attribute': self.player.pair_attribute,
            'color': self.player.color,
            'succfail': self.player.succfail,
            'didnot': self.player.didnot
        }

class Results(Page):
    def is_displayed(self):
        return self.round_number >= 48


page_sequence = [
    Consent,
    Instructions1,
    Instructions2,
    Instructions3,
    Comprehension,
    Responsibility,
    Results
]
