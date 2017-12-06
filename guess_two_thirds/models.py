from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency
)

import itertools


doc = """
a.k.a. Keynesian beauty contest.

Players all guess a number; whoever guesses closest to
2/3 of the average wins.

See https://en.wikipedia.org/wiki/Guess_2/3_of_the_average
"""


class Constants(BaseConstants):
    players_per_group = 3
    num_rounds = 3
    name_in_url = 'guess_two_thirds'

    jackpot = Currency(100)
    guess_max = 100

    instructions_template_novice = 'guess_two_thirds/InstructionsNovice.html'
    instructions_template_expert = 'guess_two_thirds/InstructionsExpert.html'


class Subsession(BaseSubsession):
    def creating_session(self):
        treatments = itertools.cycle(['novice', 'expert'])
        for g in self.get_groups():
            if 'treatment' in self.session.config:
                # demo mode
                g.treatment = self.session.config['treatment']
            else:
                # live experiment mode
                g.treatment = next(treatments)


class Group(BaseGroup):
    treatment = models.CharField()
    two_thirds_avg = models.FloatField()
    best_guess = models.PositiveIntegerField()
    num_winners = models.PositiveIntegerField()

    def set_payoffs(self):
        players = self.get_players()
        guesses = [p.guess for p in players]
        two_thirds_avg = (2 / 3) * sum(guesses) / len(players)
        self.two_thirds_avg = round(two_thirds_avg, 2)

        self.best_guess = min(guesses,
            key=lambda guess: abs(guess - self.two_thirds_avg))

        winners = [p for p in players if p.guess == self.best_guess]
        self.num_winners = len(winners)

        for p in winners:
            p.is_winner = True
            p.payoff = Constants.jackpot / self.num_winners

    def two_thirds_avg_history(self):
        return [g.two_thirds_avg for g in self.in_previous_rounds()]


class Player(BasePlayer):
    guess = models.PositiveIntegerField(max=Constants.guess_max)
    is_winner = models.BooleanField(initial=False)

