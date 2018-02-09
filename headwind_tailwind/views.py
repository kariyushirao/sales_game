from . import models
from ._builtin import Page, WaitPage


class Introduction(Page):
    def is_displayed(self):
        return self.round_number == 1

class Invest(Page):
    form_model = models.Player
    form_fields = ['asset_a_purchase', 'asset_b_purchase', 'asset_c_purchase']

    def vars_for_template(self):
        if self.round_number == 1:
            return {
                'asset_a_holdings': self.player.asset_a_holdings,
                'asset_b_holdings': self.player.asset_b_holdings,
                'asset_c_holdings': self.player.asset_c_holdings,
                'inv_port_balance': self.player.inv_port_balance,
                'round_number': self.round_number
                }
        else:
            return {
                'asset_a_holdings': self.player.in_round(self.round_number - 1).asset_a_holdings,
                'asset_b_holdings': self.player.in_round(self.round_number - 1).asset_b_holdings,
                'asset_c_holdings': self.player.in_round(self.round_number - 1).asset_c_holdings,
                'inv_port_balance': self.player.in_round(self.round_number - 1).inv_port_balance,
                'round_number': self.round_number
                }

    def error_message(self, values):
        if values["asset_a_purchase"] + values["asset_b_purchase"] + values["asset_c_purchase"] > 1000:
            return 'Your total investment cannot exceed $1,000.00'

    def before_next_page(self):
        self.player.update_holdings()
        self.player.update_inv_port_balance()


class Results(Page):

    def vars_for_template(self):
        if self.round_number == 1:
            return {
            # amount of each asset purchased in this round
            'asset_a_purchase': self.player.asset_a_purchase,
            'asset_b_purchase': self.player.asset_b_purchase,
            'asset_c_purchase': self.player.asset_c_purchase,
            # current amount of each asset held
            'asset_a_holdings': self.player.asset_a_holdings,
            'asset_b_holdings': self.player.asset_b_holdings,
            'asset_c_holdings': self.player.asset_c_holdings,
            # previous amount of each asset held
            'asset_a_prior': '$0.00',
            'asset_b_prior': '$0.00',
            'asset_c_prior': '$0.00',
            # player's current investment portfolio balance
            'inv_port_balance': self.player.inv_port_balance,
            'inv_prev_balance': '$0.00',
            'round_number': self.round_number
            }
        else:
            return {
            # amount of each asset purchased in this round
            'asset_a_purchase': self.player.asset_a_purchase,
            'asset_b_purchase': self.player.asset_b_purchase,
            'asset_c_purchase': self.player.asset_c_purchase,
            # current amount of each asset held
            'asset_a_holdings': self.player.asset_a_holdings,
            'asset_b_holdings': self.player.asset_b_holdings,
            'asset_c_holdings': self.player.asset_c_holdings,
            # previous amount of each asset held
            'asset_a_prior': self.player.in_round(self.round_number - 1).asset_a_holdings,
            'asset_b_prior': self.player.in_round(self.round_number - 1).asset_b_holdings,
            'asset_c_prior': self.player.in_round(self.round_number - 1).asset_c_holdings,
            # player's current investment portfolio balance
            'inv_port_balance': self.player.inv_port_balance,
            'inv_prev_balance': self.player.in_round(self.round_number - 1).inv_port_balance,
            'round_number': self.round_number
            }

class ResultsTailwind(Page):
    def is_displayed(self):
        return self.round_number >= 12 and self.participant.vars['treatment'] == 'tailwind'

    def vars_for_template(self):
        return {
        # player's current investment portfolio balance
        'inv_port_balance': self.player.inv_port_balance,
        'num_participants': self.participant.vars['other_participants']
        }

class ResultsNeutral(Page):
    def is_displayed(self):
            return self.round_number >= 12 and self.participant.vars['treatment'] == 'neutral'

    def vars_for_template(self):
        return {
        # player's current investment portfolio balance
        'inv_port_balance': self.player.inv_port_balance,
        'num_participants': self.participant.vars['other_participants']
        }

class ResultsHeadwind(Page):
    def is_displayed(self):
        return self.round_number >= 12 and self.participant.vars['treatment'] == 'headwind'

    def vars_for_template(self):
        return {
        # player's current investment portfolio balance
        'inv_port_balance': self.player.inv_port_balance,
        'num_participants': self.participant.vars['other_participants']
        }

class Attribution(Page):
    form_model = models.Player
    form_fields = ['advice','luck_or_skill']

    def is_displayed(self):
        return self.round_number >= 12

page_sequence = [Introduction,
                 Invest,
                 Results,
                 ResultsTailwind,
                 ResultsNeutral,
                 ResultsHeadwind,
                 Attribution]
