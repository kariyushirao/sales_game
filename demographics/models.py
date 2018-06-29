from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import csv

author = 'Kariyushi'

doc = """
Very basic demographics questionnaire.
"""


class Constants(BaseConstants):
    name_in_url = 'wrapup'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    age = models.PositiveIntegerField()
    gender = models.IntegerField(
        choices=[[0, 'Male'],[1, 'Female']],
        widget=widgets.RadioSelect
        )
    responsibility = models.TextField()
    most_important = models.CharField(
        choices=['Average Score in Past Tournaments',
                 'Number of Tournaments Completed',
                 'Score in the Tournament Today'],
        widget=widgets.RadioSelect
        )
    comments = models.TextField()
