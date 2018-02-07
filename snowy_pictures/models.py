from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'snowy_pictures'
    players_per_group = None
    num_rounds = 4


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    snowy_label = models.TextField(widget=widgets.Textarea(attrs={'cols':'10','rows':'5'}))
    image_id = models.CharField()
