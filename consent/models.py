from os import environ
from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

from django import forms as djforms

author = 'Philipp Chapkovski, UZH'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'consent'
    players_per_group = None
    num_rounds = 1
    consent_timeout = int(environ.get('CONSENT_TIMEOUT', 15))

    startwp_timer = 150


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    consent = models.BooleanField(widget=djforms.CheckboxInput, initial=False)
    is_dropout = models.BooleanField(default=False)
