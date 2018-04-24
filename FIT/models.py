from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import csv
import random

author = 'Your name here'

doc = """
Reads faith in intuition scale questions from a spreadsheet
(see quiz.csv in this directory).
There is 1 question per page; the number of pages in the game
is determined by the number of questions in the CSV.
See the comment below about how to randomize the order of pages.
"""


class Constants(BaseConstants):
    name_in_url = 'follow up'
    players_per_group = None

    with open('FIT/quiz.csv') as f:
        questions = list(csv.DictReader(f))

    num_rounds = len(questions)


class Subsession(BaseSubsession):
    def before_session_starts(self):
        if self.round_number == 1:
            # randomly shuffle questions for each participant
            for p in self.get_players():
                randomized_questions = random.sample(Constants.questions, len(Constants.questions))
                # assign questions to participant.vars
                p.participant.vars['questions'] = randomized_questions
                
                # self.session.vars['questions'] = Constants.questions
            
            ## ALTERNATIVE DESIGN:
            ## to randomize the order of the questions, you could instead do:

            # import random
            # randomized_questions = random.sample(Constants.questions, len(Constants.questions))
            # self.session.vars['questions'] = randomized_questions

            ## and to randomize differently for each participant, you could use
            ## the random.sample technique, but assign into participant.vars
            ## instead of session.vars.

        for p in self.get_players():
            question_data = p.current_question()
            p.question_id = question_data['id']
            p.question = question_data['question']


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    question_id = models.PositiveIntegerField()
    question = models.CharField()
    submitted_answer = models.IntegerField(
        widget=widgets.Slider(attrs={'step': '1.00'},
            show_value=False))

    def current_question(self):
        return self.participant.vars['questions'][self.round_number - 1]
