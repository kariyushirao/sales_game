from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Consent(Page):
    def is_displayed(self):
        return self.round_number == 1

## INSTRUCTIONS PAGES ##

# First page same for all conditions
class Instructions1(Page):
    def is_displayed(self):
        return self.round_number == 1

# Instructions fork starting at page 2
class Instructions2HG(Page):
    def is_displayed(self):
        return self.round_number == 1 and self.participant.vars['treatment'] == 'histogram'
    
    def vars_for_template(self):
        return {
            # these file names refer to specific items in the ../templates/responsibility_attribution
            # folder - make sure you have images in that folder that match these file names, or 
            # change the file names to reflect which images you wish to use
            'dots1': 'responsibility_attribution/pictures/Smith_dots.png',
            'dots2': 'responsibility_attribution/pictures/Jarrod_dots.png',
        }

class Instructions2HM(Page):
    def is_displayed(self):
        return self.round_number == 1 and self.participant.vars['treatment'] == 'heatmap'
    
    def vars_for_template(self):
        return {
            # these file names refer to specific items in the ../templates/responsibility_attribution
            # folder - make sure you have images in that folder that match these file names, or 
            # change the file names to reflect which images you wish to use
            'heat1': 'responsibility_attribution/pictures/Smith_prior.png',
            'heat2': 'responsibility_attribution/pictures/Jarrod_prior.png'
        }

class Instructions2WD(Page):
    def is_displayed(self):
        return self.round_number == 1 and self.participant.vars['treatment'] == 'words'

class Instructions3HG(Page):
    def is_displayed(self):
        return self.round_number == 1 and self.participant.vars['treatment'] == 'histogram'

    def vars_for_template(self):
        return {
            'curr1': 'responsibility_attribution/pictures/Smith_dots_current.png',
            'curr2': 'responsibility_attribution/pictures/Jarrod_dots_current.png'
        }

class Instructions3HM(Page):
    def is_displayed(self):
        return self.round_number == 1 and self.participant.vars['treatment'] == 'heatmap'

    def vars_for_template(self):
        return {
            'curr1': 'responsibility_attribution/pictures/Smith_current.png',
            'curr2': 'responsibility_attribution/pictures/Jarrod_current.png'
        }

class Instructions3WD(Page):
    def is_displayed(self):
        return self.round_number == 1 and self.participant.vars['treatment'] == 'words'

## COMPREHENSION CHECK PAGES ##
class ComprehensionHG(Page):
    def is_displayed(self):
        return self.round_number == 1 and self.participant.vars['treatment'] == 'histogram'

    form_model = models.Player
    form_fields = ['comprehension1', 'comprehension3', 'comprehension4']

    def vars_for_template(self):
        return {
            'curr': 'responsibility_attribution/pictures/Nussbaum_current.png'
        }

    def error_message(self, values):
        print('values are', values)
        threshold = (values['comprehension1'] == 1)
        dots = (values['comprehension3'] == 2)
        score = (values['comprehension4'] == 2)
        if not (threshold and dots and score):
            return 'It looks like you may have answered one or more questions incorrectly.  Please check your answers and correct any mistakes.'

class ComprehensionHM(Page):
    def is_displayed(self):
        return self.round_number == 1 and self.participant.vars['treatment'] == 'heatmap'

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
        score = (values['comprehension4'] == 2)
        if not (threshold and color and score):
            return 'It looks like you may have answered one or more questions incorrectly.  Please check your answers and correct any mistakes.'

class ComprehensionWD(Page):
    def is_displayed(self):
        return self.round_number == 1 and self.participant.vars['treatment'] == 'words'

    form_model = models.Player
    form_fields = ['comprehension1', 'comprehension2', 'comprehension3', 'comprehension4']

    def vars_for_template(self):
        return {
            'curr': 'responsibility_attribution/pictures/Nussbaum_current.png'
        }

    def error_message(self, values):
        print('values are', values)
        threshold = (values['comprehension1'] == 1)
        pastrange = (values['comprehension5'] == 2)
        score = (values['comprehension4'] == 2)
        if not (threshold and pastrange and score):
            return 'It looks like you may have answered one or more questions incorrectly.  Please check your answers and correct any mistakes.'

##  PREDICTION PAGES ##
class PredictionHG(Page):
    def is_displayed(self):
        return self.participant.vars['treatment'] == 'histogram'

    form_model = models.Player
    form_fields = ['prediction']

    def vars_for_template(self):
        return {
            'dots': 'responsibility_attribution/pictures/{}.png'.format(self.player.stim_dots),
            'name': self.player.stim_name
        }

class PredictionHM(Page):
    def is_displayed(self):
        return self.participant.vars['treatment'] == 'heatmap'

    form_model = models.Player
    form_fields = ['prediction']

    def vars_for_template(self):
        return {
            'heat_map': 'responsibility_attribution/pictures/{}.png'.format(self.player.stim_prior),
            'name': self.player.stim_name
        }

class PredictionWD(Page):
    def is_displayed(self):
        return self.participant.vars['treatment'] == 'words'

    form_model = models.Player
    form_fields = ['prediction']

    def vars_for_template(self):
        return {
            'name': self.player.stim_name
        }

## RESPONSIBILITY PAGES ##
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

## RESULTS PAGE ##
class Results(Page):
    def is_displayed(self):
        return self.round_number >= 42


page_sequence = [
    Consent,
    Instructions1,
    Instructions2HG,
    Instructions2HM,
    Instructions2WD,
    Instructions3HG,
    Instructions3HM,
    Instructions3WD,
    ComprehensionHG,
    ComprehensionHM,
    ComprehensionWD,
    PredictionHG,
    PredictionHM,
    PredictionWD,
    ResponsibilityE,
    ResponsibilityR,
    Results
]
