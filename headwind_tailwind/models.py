from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency
)

import itertools
import random


doc = """
Participants choose how to invest money each month for
12 months. Depending on treatment, the value of their 
investments either grow or shrink based on how much 
they've chosen to invest the previous month.
"""


class Constants(BaseConstants):
    players_per_group = None
    num_rounds = 12
    name_in_url = 'investment_12_months'

    # how much $$ participants may invest every round
    # monthly_budget = models.CurrencyField()
    monthly_budget = Currency(1000.00)

    instructions_template = 'headwind_tailwind/Instructions.html'

    # sets asset names
    asset_a_name = "GOLD"
    asset_b_name = "OIL"
    asset_c_name = "STOCKS"

    # defines the multipliers for each treatment
    tailwinds_high = [1.18, 1.17, 1.16, 1.15, 1.14, 1.13, 1.12, 1.11, 1.10, 1.09, 1.08, 1.07]
    tailwinds_medium = [1.09, 1.08, 1.07, 1.06, 1.05, 1.04, 1.03, 1.02, 1.01, 1.00, 0.99, 0.98]
    tailwinds_low = [1.00, 0.99, 0.98, 0.97, 0.96, 0.95, 0.94, 0.93, 0.92, 0.91, 0.90, 0.89]

    neutrals_high = [1.09, 1.08, 1.07, 1.06, 1.05, 1.04, 1.03, 1.02, 1.01, 1.00, 0.99, 0.98]
    neutrals_medium = [1.09, 1.08, 1.07, 1.06, 1.05, 1.04, 1.03, 1.02, 1.01, 1.00, 0.99, 0.98]
    neutrals_low = [1.09, 1.08, 1.07, 1.06, 1.05, 1.04, 1.03, 1.02, 1.01, 1.00, 0.99, 0.98]

    headwinds_high = [1.00, 0.99, 0.98, 0.97, 0.96, 0.95, 0.94, 0.93, 0.92, 0.91, 0.90, 0.89]
    headwinds_medium = [1.09, 1.08, 1.07, 1.06, 1.05, 1.04, 1.03, 1.02, 1.01, 1.00, 0.99, 0.98]
    headwinds_low = [1.18, 1.17, 1.16, 1.15, 1.14, 1.13, 1.12, 1.11, 1.10, 1.09, 1.08, 1.07]

class Subsession(BaseSubsession):
    def creating_session(self):
        
        treatments = itertools.cycle(['tailwind', 'neutral', 'headwind'])
        num_participants = itertools.cycle([112, 115, 117, 122, 125, 126, 129, 131, 135])

        if self.round_number == 1:    
            for p in self.get_players():
                other_participants = next(num_participants)
                p.participant.vars['other_participants'] = other_participants

        # assigns treatment at the participant level so that same treatment
        # persists across rounds
        if self.round_number == 1:    
            for p in self.get_players():
                if 'treatment' in self.session.config:
                    # demo mode
                    treatment = self.session.config['treatment']
                    p.participant.vars['treatment'] = treatment
                    p.treatment = treatment
                    # assigns asset multipliers based on treatment
                    if treatment == 'tailwind':
                        tailwinds_high = Constants.tailwinds_high.copy()
                        tailwinds_medium = Constants.tailwinds_medium.copy()
                        tailwinds_low = Constants.tailwinds_low.copy()
                        random.shuffle(tailwinds_high)
                        random.shuffle(tailwinds_medium)
                        random.shuffle(tailwinds_low)
                        p.participant.vars['high_multipliers'] = tailwinds_high
                        p.participant.vars['medium_multipliers'] = tailwinds_medium
                        p.participant.vars['low_multipliers'] = tailwinds_low
                    elif treatment == 'neutral':
                        neutrals_high = Constants.neutrals_high.copy()
                        neutrals_medium = Constants.neutrals_medium.copy()
                        neutrals_low = Constants.neutrals_low.copy()
                        random.shuffle(neutrals_high)
                        random.shuffle(neutrals_medium)
                        random.shuffle(neutrals_low)
                        p.participant.vars['high_multipliers'] = neutrals_high
                        p.participant.vars['medium_multipliers'] = neutrals_medium
                        p.participant.vars['low_multipliers'] = neutrals_low
                    else:
                        headwinds_high = Constants.headwinds_high.copy()
                        headwinds_medium = Constants.headwinds_medium.copy()
                        headwinds_low = Constants.headwinds_low.copy()
                        random.shuffle(headwinds_high)
                        random.shuffle(headwinds_medium)
                        random.shuffle(headwinds_low)
                        p.participant.vars['high_multipliers'] = headwinds_high
                        p.participant.vars['medium_multipliers'] = headwinds_medium
                        p.participant.vars['low_multipliers'] = headwinds_low
                else:
                    # live experiment mode
                    treatment = next(treatments)
                    p.participant.vars['treatment'] = treatment
                    p.treatment = treatment
                    if treatment == 'tailwind':
                        tailwinds_high = Constants.tailwinds_high.copy()
                        tailwinds_medium = Constants.tailwinds_medium.copy()
                        tailwinds_low = Constants.tailwinds_low.copy()
                        random.shuffle(tailwinds_high)
                        random.shuffle(tailwinds_medium)
                        random.shuffle(tailwinds_low)
                        p.participant.vars['high_multipliers'] = tailwinds_high
                        p.participant.vars['medium_multipliers'] = tailwinds_medium
                        p.participant.vars['low_multipliers'] = tailwinds_low
                    elif treatment == 'neutral':
                        neutrals_high = Constants.neutrals_high.copy()
                        neutrals_medium = Constants.neutrals_medium.copy()
                        neutrals_low = Constants.neutrals_low.copy()
                        random.shuffle(neutrals_high)
                        random.shuffle(neutrals_medium)
                        random.shuffle(neutrals_low)
                        p.participant.vars['high_multipliers'] = neutrals_high
                        p.participant.vars['medium_multipliers'] = neutrals_medium
                        p.participant.vars['low_multipliers'] = neutrals_low
                    else:
                        headwinds_high = Constants.headwinds_high.copy()
                        headwinds_medium = Constants.headwinds_medium.copy()
                        headwinds_low = Constants.headwinds_low.copy()
                        random.shuffle(headwinds_high)
                        random.shuffle(headwinds_medium)
                        random.shuffle(headwinds_low)
                        p.participant.vars['high_multipliers'] = headwinds_high
                        p.participant.vars['medium_multipliers'] = headwinds_medium
                        p.participant.vars['low_multipliers'] = headwinds_low
        else:
            for p in self.get_players():
                treatment = p.participant.vars['treatment']
                p.treatment = treatment


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    treatment = models.CharField()
    advice = models.TextField()
    luck_or_skill = models.IntegerField(widget=widgets.Slider(attrs={'step': '1.00'},show_value=False))

    inv_port_balance = models.CurrencyField(initial=0.00)

    # db variable tracks amount purchased each round
    asset_a_purchase = models.CurrencyField(initial=0.00)
    # db variable tracks multiplier each round
    asset_a_multiplier = models.FloatField(initial=0.00)
    # db variable tracks balance of asset holdings each round
    asset_a_holdings = models.CurrencyField(initial=0.00)

    asset_b_purchase = models.CurrencyField(initial=0.00)
    asset_b_multiplier = models.FloatField(initial=0.00)
    asset_b_holdings = models.CurrencyField(initial=0.00)

    asset_c_purchase = models.CurrencyField(initial=0.00)
    asset_c_multiplier = models.FloatField(initial=0.00)
    asset_c_holdings = models.CurrencyField(initial=0.00)

    def update_holdings(self):
        # adds any investments made in current round to balance of holdings
        # for each asset
        if self.round_number == 1: 
            asset_a_holdings = self.asset_a_holdings + self.asset_a_purchase
            asset_b_holdings = self.asset_b_holdings + self.asset_b_purchase
            asset_c_holdings = self.asset_c_holdings + self.asset_c_purchase
        else:
            asset_a_holdings = self.in_round(self.round_number - 1).asset_a_holdings + self.asset_a_purchase
            asset_b_holdings = self.in_round(self.round_number - 1).asset_b_holdings + self.asset_b_purchase
            asset_c_holdings = self.in_round(self.round_number - 1).asset_c_holdings + self.asset_c_purchase

        # creates a list of the holdings so we can determine relative values
        holdings = [asset_a_holdings, asset_b_holdings, asset_c_holdings]

        # finds asset with largest balance
        max_hold = max(holdings)
        # finds asset with smallest balance
        min_hold = min(holdings)

        # SET MULTIPLIERS BASED ON TREATMENT
        # 1) determines multipliers for each asset based on balance of holdings
        # balance is the sum of holdings going into current round, plus
        # any new investment made in current round 
        # 2) applies the multipliers for each treatment, as defined in Constants 
        
        # sets index based on round number to iterate through shuffled
        # multipliers lists
        multiplier_index = self.round_number - 1

        high_multipliers = self.participant.vars['high_multipliers']
        print(high_multipliers)
        medium_multipliers = self.participant.vars['medium_multipliers']
        print(medium_multipliers)
        low_multipliers = self.participant.vars['low_multipliers']
        print(low_multipliers)

        # NOTE: HOW DO WE WANT TO HANDLE TIES?  CURRENTLY, WHICHEVER ASSET IS 
        # EARLIER IN THE ORDER A, B, C WILL BE ATTRIBUTED THE HIGHEST MULTIPLIER
        # I.E. IF A AND B ARE EQUAL, A WILL BE ATTRIBUTED THE HIGH MULTIPLIER
        # AND B WILL BE ATTRIBUTED THE MEDIUM MULTIPLIER

        # first, if player is in the tailwind treatment
        if self.treatment == 'tailwind':
            if asset_a_holdings == max_hold:
                self.asset_a_multiplier =  high_multipliers[multiplier_index]
                if asset_b_holdings == min_hold:
                    self.asset_b_multiplier = low_multipliers[multiplier_index]
                    self.asset_c_multiplier = medium_multipliers[multiplier_index]
                else:
                    self.asset_b_multiplier = medium_multipliers[multiplier_index]
                    self.asset_c_multiplier = low_multipliers[multiplier_index]
            elif asset_a_holdings == min_hold:
                self.asset_a_multiplier = low_multipliers[multiplier_index]
                if asset_b_holdings == max_hold:
                    self.asset_b_multiplier = high_multipliers[multiplier_index]
                    self.asset_c_multiplier = medium_multipliers[multiplier_index]
                else: 
                    self.asset_b_multiplier = medium_multipliers[multiplier_index]
                    self.asset_c_multiplier = high_multipliers[multiplier_index]
            else:
                self.asset_a_multiplier = medium_multipliers[multiplier_index]
                if asset_b_holdings == max_hold:
                    self.asset_b_multiplier = high_multipliers[multiplier_index]
                    self.asset_c_multiplier = low_multipliers[multiplier_index]
                else:
                    self.asset_b_multiplier = low_multipliers[multiplier_index]
                    self.asset_c_multiplier = high_multipliers[multiplier_index]
        # next, if player is in the headwind treatment
        if self.treatment == 'headwind':
            if asset_a_holdings == max_hold:
                self.asset_a_multiplier =  high_multipliers[multiplier_index]
                if asset_b_holdings == min_hold:
                    self.asset_b_multiplier = low_multipliers[multiplier_index]
                    self.asset_c_multiplier = medium_multipliers[multiplier_index]
                else:
                    self.asset_b_multiplier = medium_multipliers[multiplier_index]
                    self.asset_c_multiplier = low_multipliers[multiplier_index]
            elif asset_a_holdings == min_hold:
                self.asset_a_multiplier = low_multipliers[multiplier_index]
                if asset_b_holdings == max_hold:
                    self.asset_b_multiplier = high_multipliers[multiplier_index]
                    self.asset_c_multiplier = medium_multipliers[multiplier_index]
                else: 
                    self.asset_b_multiplier = medium_multipliers[multiplier_index]
                    self.asset_c_multiplier = high_multipliers[multiplier_index]
            else:
                self.asset_a_multiplier = medium_multipliers[multiplier_index]
                if asset_b_holdings == max_hold:
                    self.asset_b_multiplier = high_multipliers[multiplier_index]
                    self.asset_c_multiplier = low_multipliers[multiplier_index]
                else:
                    self.asset_b_multiplier = low_multipliers[multiplier_index]
                    self.asset_c_multiplier = high_multipliers[multiplier_index]
        # finally, if in the neutral treatment
        if self.treatment == 'neutral':
            if asset_a_holdings == max_hold:
                self.asset_a_multiplier =  high_multipliers[multiplier_index]
                if asset_b_holdings == min_hold:
                    self.asset_b_multiplier = low_multipliers[multiplier_index]
                    self.asset_c_multiplier = medium_multipliers[multiplier_index]
                else:
                    self.asset_b_multiplier = medium_multipliers[multiplier_index]
                    self.asset_c_multiplier = low_multipliers[multiplier_index]
            elif asset_a_holdings == min_hold:
                self.asset_a_multiplier = low_multipliers[multiplier_index]
                if asset_b_holdings == max_hold:
                    self.asset_b_multiplier = high_multipliers[multiplier_index]
                    self.asset_c_multiplier = medium_multipliers[multiplier_index]
                else: 
                    self.asset_b_multiplier = medium_multipliers[multiplier_index]
                    self.asset_c_multiplier = high_multipliers[multiplier_index]
            else:
                self.asset_a_multiplier = medium_multipliers[multiplier_index]
                if asset_b_holdings == max_hold:
                    self.asset_b_multiplier = high_multipliers[multiplier_index]
                    self.asset_c_multiplier = low_multipliers[multiplier_index]
                else:
                    self.asset_b_multiplier = low_multipliers[multiplier_index]
                    self.asset_c_multiplier = high_multipliers[multiplier_index]

        self.asset_a_holdings = asset_a_holdings * self.asset_a_multiplier
        self.asset_b_holdings = asset_b_holdings * self.asset_b_multiplier
        self.asset_c_holdings = asset_c_holdings * self.asset_c_multiplier

    def update_inv_port_balance(self):
        total_holdings = self.asset_a_holdings + self.asset_b_holdings + self.asset_c_holdings

        self.inv_port_balance = total_holdings 


