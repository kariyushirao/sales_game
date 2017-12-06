from . import models
from ._builtin import Page, WaitPage


class ArrivalWaitPage(WaitPage):
    group_by_arrival_time = True

    def is_displayed(self):
        return self.round_number == 1

class IntroductionNovice(Page):
    def is_displayed(self):
        return self.round_number == 1 and self.group.treatment == 'novice'

    timeout_seconds = 90


class IntroductionExpert(Page):
    def is_displayed(self):
        return self.round_number == 1 and self.group.treatment == 'expert'

    timeout_seconds = 90


class Guess(Page):
    form_model = models.Player
    form_fields = ['guess']

    timeout_seconds = 30
    timeout_submission = {'guess': 50}

    def before_next_page(self):
    if self.timeout_happened:
        self.player.timeout = True


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs()

class Results(Page):
    def round_number(self):
        return self.round_number

    def vars_for_template(self):
        sorted_guesses = sorted(p.guess for p in self.group.get_players())

        return {'sorted_guesses': sorted_guesses}

    timeout_seconds = 30


page_sequence = [ArrivalWaitPage,
                 IntroductionNovice,
                 IntroductionExpert,
                 Guess,
                 ResultsWaitPage,
                 Results]
