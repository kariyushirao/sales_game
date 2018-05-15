from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants

 
class Question(Page):
    form_model = models.Player
    form_fields = ['age', 'gender', 'comments']


class Results(Page):
    pass

page_sequence = [
    Question,
    Results
]
