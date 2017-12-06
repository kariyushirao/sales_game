from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Kariyushi'

doc = """
Players each guess the answer to a question three times.  Between each guess, the players
view their two counterparts' guesses, and must make a guess between the lowest and highest
guess for the next round.
"""


class Constants(BaseConstants):
    name_in_url = 'delphi'
    players_per_group = 3
    num_rounds = 3


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    highest_guess = models.PositiveIntegerField()
    lowest_guess = models.PositiveIntegerField()

    def set_payoffs(self):
        players = self.get_players()
        guesses = [p.guess for p in players]
        highest_guess = max(guesses)
        lowest_guess = min(guesses)
        self.highest_guess = round(highest_guess, 2)
        self.lowest_guess = round(lowest_guess, 2)

    def guess_lowest(self):
        return [g.lowest_guess for g in self.in_previous_rounds()]

    def guess_highest(self):
        return [g.highest_guess for g in self.in_previous_rounds()]


class Player(BasePlayer):
    guess = models.PositiveIntegerField(max=Constants.guess_max)
