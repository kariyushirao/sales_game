from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import math


class Consent(Page):
    timeout_seconds = Constants.consent_timeout
    form_model = models.Player
    form_fields = ['consent']
    timeout_submission = {'consent': False}

    def vars_for_template(self):
        if self.session.config.get('name') == 'survey':
            self.template_name = 'consent/AltConsent.html'
        return {'consent_timeout_min': math.ceil(self.timeout_seconds / 60)}

    def is_displayed(self):
        return self.round_number == 1

    def consent_error_message(self, value):
        if not value:
            return 'You must accept the consent form in order to proceed with the study!'

    def before_next_page(self):
        if self.timeout_happened:
            self.player.consent = False
            self.player.is_dropout = True
            self.player.participant.vars['dropout'] = True
            self.player.participant.vars['consent_dropout'] = True


class BlockDropouts(Page):
    def is_displayed(self):
        return self.round_number == 1 and self.player.participant.vars.get('consent_dropout', False)


page_sequence = [
    Consent,
    BlockDropouts,
]
