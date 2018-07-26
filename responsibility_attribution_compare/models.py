from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import random
import itertools

author = '(c) Kariyushi Rao, 2018'

doc = """
Participants are shown performance history and current scores for pairs of individual competitors in a tournament. 
Participants are asked to decide whether the agents deserve equal, less, or more credit or blame for their 
individual performances, compared with each other.
"""


class Constants(BaseConstants):
    name_in_url = 'responsibility_attribution_compare'
    players_per_group = None
    num_rounds = 48

    # stimuli
    pairs = {1: {'gymnast1': {'name': 'Banerion', 'sample': 20, 'current': 'dotplot_alpha_3_beta_7_n_20_points_1', 'score': 1},
    			 'gymnast2': {'name': 'Cortez', 'sample': 20, 'current': 'dotplot_alpha_5_beta_5_n_20_points_1', 'score': 1},
    			 'outcome': 'FAILURE', 'attribute': 'blame', 'color': 'maroon', 'succfail': 'failed', 'didnot': 'did not meet'
    			},
    		 2: {'gymnast1': {'name': 'Paytiamo', 'sample': 100, 'current': 'dotplot_alpha_3_beta_7_n_100_points_1', 'score': 1},
    			 'gymnast2': {'name': 'Palmer', 'sample': 100, 'current': 'dotplot_alpha_5_beta_5_n_100_points_1', 'score': 1},
    			 'outcome': 'FAILURE', 'attribute': 'blame', 'color': 'maroon', 'succfail': 'failed', 'didnot': 'did not meet'
    			},
    		 3: {'gymnast1': {'name': 'Babbage', 'sample': 20, 'current': 'dotplot_alpha_3_beta_7_n_20_points_3', 'score': 3},
    			 'gymnast2': {'name': 'Sasaki', 'sample': 20, 'current': 'dotplot_alpha_5_beta_5_n_20_points_3', 'score': 3},
    			 'outcome': 'FAILURE', 'attribute': 'blame', 'color': 'maroon', 'succfail': 'failed', 'didnot': 'did not meet'
    			},
    		 4: {'gymnast1': {'name': 'Mendoza', 'sample': 100, 'current': 'dotplot_alpha_3_beta_7_n_100_points_3', 'score': 3},
    			 'gymnast2': {'name': 'Alarid', 'sample': 100, 'current': 'dotplot_alpha_5_beta_5_n_100_points_3', 'score': 3},
    			 'outcome': 'FAILURE', 'attribute': 'blame', 'color': 'maroon', 'succfail': 'failed', 'didnot': 'did not meet'
    			},
    		 5: {'gymnast1': {'name': 'Wilcox', 'sample': 20, 'current': 'dotplot_alpha_3_beta_7_n_20_points_7', 'score': 7},
    			 'gymnast2': {'name': 'Sewald', 'sample': 20, 'current': 'dotplot_alpha_5_beta_5_n_20_points_7', 'score': 7},
    			 'outcome': 'SUCCESS', 'attribute': 'credit', 'color': 'darkgreen', 'succfail': 'succeeded', 'didnot': 'exceeded'
    			},
    		 6: {'gymnast1': {'name': 'Mitchell', 'sample': 100, 'current': 'dotplot_alpha_3_beta_7_n_100_points_7', 'score': 7},
    			 'gymnast2': {'name': 'Hunter', 'sample': 100, 'current': 'dotplot_alpha_5_beta_5_n_100_points_7', 'score': 7},
    			 'outcome': 'SUCCESS', 'attribute': 'credit', 'color': 'darkgreen', 'succfail': 'succeeded', 'didnot': 'exceeded'
    			},
    		 7: {'gymnast1': {'name': 'Douglas', 'sample': 20, 'current': 'dotplot_alpha_3_beta_7_n_20_points_9', 'score': 9},
    			 'gymnast2': {'name': 'Burnley', 'sample': 20, 'current': 'dotplot_alpha_5_beta_5_n_20_points_9', 'score': 9},
    			 'outcome': 'SUCCESS', 'attribute': 'credit', 'color': 'darkgreen', 'succfail': 'succeeded', 'didnot': 'exceeded'
    			},
    		 8: {'gymnast1': {'name': 'Banuelos', 'sample': 100, 'current': 'dotplot_alpha_3_beta_7_n_100_points_9', 'score': 9},
    			 'gymnast2': {'name': 'Maldon', 'sample': 100, 'current': 'dotplot_alpha_5_beta_5_n_100_points_9', 'score': 9},
    			 'outcome': 'SUCCESS', 'attribute': 'credit', 'color': 'darkgreen', 'succfail': 'succeeded', 'didnot': 'exceeded'
    			},
    		 9: {'gymnast1': {'name': 'Dacuba', 'sample': 20, 'current': 'dotplot_alpha_3_beta_7_n_20_points_1', 'score': 1},
    			 'gymnast2': {'name': 'Jurado', 'sample': 20, 'current': 'dotplot_alpha_7_beta_3_n_20_points_1', 'score': 1},
    			 'outcome': 'FAILURE', 'attribute': 'blame', 'color': 'maroon', 'succfail': 'failed', 'didnot': 'did not meet'
    			},
    		10: {'gymnast1': {'name': 'Hossain', 'sample': 100, 'current': 'dotplot_alpha_3_beta_7_n_100_points_1', 'score': 1},
    			 'gymnast2': {'name': 'Aguilar', 'sample': 100, 'current': 'dotplot_alpha_7_beta_3_n_100_points_1', 'score': 1},
    			 'outcome': 'FAILURE', 'attribute': 'blame', 'color': 'maroon', 'succfail': 'failed', 'didnot': 'did not meet'
    			},
    		11: {'gymnast1': {'name': 'Gurule', 'sample': 20, 'current': 'dotplot_alpha_3_beta_7_n_20_points_3', 'score': 3},
    			 'gymnast2': {'name': 'Siprese', 'sample': 20, 'current': 'dotplot_alpha_7_beta_3_n_20_points_3', 'score': 3},
    			 'outcome': 'FAILURE', 'attribute': 'blame', 'color': 'maroon', 'succfail': 'failed', 'didnot': 'did not meet'
    			},
    		12: {'gymnast1': {'name': 'Raiburn', 'sample': 100, 'current': 'dotplot_alpha_3_beta_7_n_100_points_3', 'score': 3},
    			 'gymnast2': {'name': 'Leonard', 'sample': 100, 'current': 'dotplot_alpha_7_beta_3_n_100_points_3', 'score': 3},
    			 'outcome': 'FAILURE', 'attribute': 'blame', 'color': 'maroon', 'succfail': 'failed', 'didnot': 'did not meet'
    			},
    		13: {'gymnast1': {'name': 'Hiebrun', 'sample': 20, 'current': 'dotplot_alpha_3_beta_7_n_20_points_7', 'score': 7},
    			 'gymnast2': {'name': 'Santiste', 'sample': 20, 'current': 'dotplot_alpha_7_beta_3_n_20_points_7', 'score': 7},
    			 'outcome': 'SUCCESS', 'attribute': 'credit', 'color': 'darkgreen', 'succfail': 'succeeded', 'didnot': 'exceeded'
    			},
    		14: {'gymnast1': {'name': 'Barrett', 'sample': 100, 'current': 'dotplot_alpha_3_beta_7_n_100_points_7', 'score': 7},
    			 'gymnast2': {'name': 'Panchal', 'sample': 100, 'current': 'dotplot_alpha_7_beta_3_n_100_points_7', 'score': 7},
    			 'outcome': 'SUCCESS', 'attribute': 'credit', 'color': 'darkgreen', 'succfail': 'succeeded', 'didnot': 'exceeded'
    			},
    		15: {'gymnast1': {'name': 'Varelas', 'sample': 20, 'current': 'dotplot_alpha_3_beta_7_n_20_points_9', 'score': 9},
    			 'gymnast2': {'name': 'McGinn', 'sample': 20, 'current': 'dotplot_alpha_7_beta_3_n_20_points_9', 'score': 9},
    			 'outcome': 'SUCCESS', 'attribute': 'credit', 'color': 'darkgreen', 'succfail': 'succeeded', 'didnot': 'exceeded'
    			},
    		16: {'gymnast1': {'name': 'Patton', 'sample': 100, 'current': 'dotplot_alpha_3_beta_7_n_100_points_9', 'score': 9},
    			 'gymnast2': {'name': 'Tafoya', 'sample': 100, 'current': 'dotplot_alpha_7_beta_3_n_100_points_9', 'score': 9},
    			 'outcome': 'SUCCESS', 'attribute': 'credit', 'color': 'darkgreen', 'succfail': 'succeeded', 'didnot': 'exceeded'
    			},
    		17: {'gymnast1': {'name': 'Majeed', 'sample': 20, 'current': 'dotplot_alpha_5_beta_5_n_20_points_1', 'score': 1},
    			 'gymnast2': {'name': 'Shakoor', 'sample': 20, 'current': 'dotplot_alpha_7_beta_3_n_20_points_1', 'score': 1},
    			 'outcome': 'FAILURE', 'attribute': 'blame', 'color': 'maroon', 'succfail': 'failed', 'didnot': 'did not meet'
    			},
    		18: {'gymnast1': {'name': 'Delacruz', 'sample': 100, 'current': 'dotplot_alpha_5_beta_5_n_100_points_1', 'score': 1},
    			 'gymnast2': {'name': 'Cordova', 'sample': 100, 'current': 'dotplot_alpha_7_beta_3_n_100_points_1', 'score': 1},
    			 'outcome': 'FAILURE', 'attribute': 'blame', 'color': 'maroon', 'succfail': 'failed', 'didnot': 'did not meet'
    			},
    		19: {'gymnast1': {'name': 'Stangoni', 'sample': 20, 'current': 'dotplot_alpha_5_beta_5_n_20_points_3', 'score': 3},
    			 'gymnast2': {'name': 'Mangisel', 'sample': 20, 'current': 'dotplot_alpha_7_beta_3_n_20_points_3', 'score': 3},
    			 'outcome': 'FAILURE', 'attribute': 'blame', 'color': 'maroon', 'succfail': 'failed', 'didnot': 'did not meet'
    			},
    		20: {'gymnast1': {'name': 'Walters', 'sample': 100, 'current': 'dotplot_alpha_5_beta_5_n_100_points_3', 'score': 3},
    			 'gymnast2': {'name': 'Kenyon', 'sample': 100, 'current': 'dotplot_alpha_7_beta_3_n_100_points_3', 'score': 3},
    			 'outcome': 'FAILURE', 'attribute': 'blame', 'color': 'maroon', 'succfail': 'failed', 'didnot': 'did not meet'
    			},
    		21: {'gymnast1': {'name': 'Rehman', 'sample': 20, 'current': 'dotplot_alpha_5_beta_5_n_20_points_7', 'score': 7},
    			 'gymnast2': {'name': 'Yacoub', 'sample': 20, 'current': 'dotplot_alpha_7_beta_3_n_20_points_7', 'score': 7},
    			 'outcome': 'SUCCESS', 'attribute': 'credit', 'color': 'darkgreen', 'succfail': 'succeeded', 'didnot': 'exceeded'
    			},
    		22: {'gymnast1': {'name': 'Gaulden', 'sample': 100, 'current': 'dotplot_alpha_5_beta_5_n_100_points_7', 'score': 7},
    			 'gymnast2': {'name': 'Haddad', 'sample': 100, 'current': 'dotplot_alpha_7_beta_3_n_100_points_7', 'score': 7},
    			 'outcome': 'SUCCESS', 'attribute': 'credit', 'color': 'darkgreen', 'succfail': 'succeeded', 'didnot': 'exceeded'
    			},
    		23: {'gymnast1': {'name': 'Massoud', 'sample': 20, 'current': 'dotplot_alpha_5_beta_5_n_20_points_9', 'score': 9},
    			 'gymnast2': {'name': 'Grainda', 'sample': 20, 'current': 'dotplot_alpha_7_beta_3_n_20_points_9', 'score': 9},
    			 'outcome': 'SUCCESS', 'attribute': 'credit', 'color': 'darkgreen', 'succfail': 'succeeded', 'didnot': 'exceeded'
    			},
    		24: {'gymnast1': {'name': 'Thomas', 'sample': 100, 'current': 'dotplot_alpha_5_beta_5_n_100_points_9', 'score': 9},
    			 'gymnast2': {'name': 'Ellsberg', 'sample': 100, 'current': 'dotplot_alpha_7_beta_3_n_100_points_9', 'score': 9},
    			 'outcome': 'SUCCESS', 'attribute': 'credit', 'color': 'darkgreen', 'succfail': 'succeeded', 'didnot': 'exceeded'
    			},
    		25: {'gymnast1': {'name': 'Horton', 'sample': 20, 'current': 'dotplot_alpha_3_beta_7_n_20_points_1', 'score': 1},
    			 'gymnast2': {'name': 'Wieber', 'sample': 20, 'current': 'dotplot_alpha_3_beta_7_n_20_points_3', 'score': 3},
    			 'outcome': 'FAILURE', 'attribute': 'blame', 'color': 'maroon', 'succfail': 'failed', 'didnot': 'did not meet'
    			},
    		26: {'gymnast1': {'name': 'Kuebler', 'sample': 100, 'current': 'dotplot_alpha_3_beta_7_n_100_points_1', 'score': 1},
    			 'gymnast2': {'name': 'Dizmang', 'sample': 100, 'current': 'dotplot_alpha_3_beta_7_n_100_points_3', 'score': 3},
    			 'outcome': 'FAILURE', 'attribute': 'blame', 'color': 'maroon', 'succfail': 'failed', 'didnot': 'did not meet'
    			},	
    		27: {'gymnast1': {'name': 'Francom', 'sample': 20, 'current': 'dotplot_alpha_3_beta_7_n_20_points_7', 'score': 7},
    			 'gymnast2': {'name': 'Burrell', 'sample': 20, 'current': 'dotplot_alpha_3_beta_7_n_20_points_9', 'score': 9},
    			 'outcome': 'SUCCESS', 'attribute': 'credit', 'color': 'darkgreen', 'succfail': 'succeeded', 'didnot': 'exceeded'
    			},
    		28: {'gymnast1': {'name': 'Herrera', 'sample': 100, 'current': 'dotplot_alpha_3_beta_7_n_100_points_7', 'score': 7},
    			 'gymnast2': {'name': 'Akerman', 'sample': 100, 'current': 'dotplot_alpha_3_beta_7_n_100_points_9', 'score': 9},
    			 'outcome': 'SUCCESS', 'attribute': 'credit', 'color': 'darkgreen', 'succfail': 'succeeded', 'didnot': 'exceeded'
    			},
    		29: {'gymnast1': {'name': 'Crawford', 'sample': 20, 'current': 'dotplot_alpha_5_beta_5_n_20_points_1', 'score': 1},
    			 'gymnast2': {'name': 'Leyerle', 'sample': 20, 'current': 'dotplot_alpha_5_beta_5_n_20_points_3', 'score': 3},
    			 'outcome': 'FAILURE', 'attribute': 'blame', 'color': 'maroon', 'succfail': 'failed', 'didnot': 'did not meet'
    			},
    		30: {'gymnast1': {'name': 'Arnold', 'sample': 100, 'current': 'dotplot_alpha_5_beta_5_n_100_points_1', 'score': 1},
    			 'gymnast2': {'name': 'Crawley', 'sample': 100, 'current': 'dotplot_alpha_5_beta_5_n_100_points_3', 'score': 3},
    			 'outcome': 'FAILURE', 'attribute': 'blame', 'color': 'maroon', 'succfail': 'failed', 'didnot': 'did not meet'
    			},	
    		31: {'gymnast1': {'name': 'Romero', 'sample': 20, 'current': 'dotplot_alpha_5_beta_5_n_20_points_7', 'score': 7},
    			 'gymnast2': {'name': 'Serrano', 'sample': 20, 'current': 'dotplot_alpha_5_beta_5_n_20_points_9', 'score': 9},
    			 'outcome': 'SUCCESS', 'attribute': 'credit', 'color': 'darkgreen', 'succfail': 'succeeded', 'didnot': 'exceeded'
    			},
    		32: {'gymnast1': {'name': 'Khatib', 'sample': 100, 'current': 'dotplot_alpha_5_beta_5_n_100_points_7', 'score': 7},
    			 'gymnast2': {'name': 'Neesley', 'sample': 100, 'current': 'dotplot_alpha_5_beta_5_n_100_points_9', 'score': 9},
    			 'outcome': 'SUCCESS', 'attribute': 'credit', 'color': 'darkgreen', 'succfail': 'succeeded', 'didnot': 'exceeded'
    			},
    		33: {'gymnast1': {'name': 'Stinson', 'sample': 20, 'current': 'dotplot_alpha_7_beta_3_n_20_points_1', 'score': 1},
    			 'gymnast2': {'name': 'Meseke', 'sample': 20, 'current': 'dotplot_alpha_7_beta_3_n_20_points_3', 'score': 3},
    			 'outcome': 'FAILURE', 'attribute': 'blame', 'color': 'maroon', 'succfail': 'failed', 'didnot': 'did not meet'
    			},
    		34: {'gymnast1': {'name': 'Fontaine', 'sample': 100, 'current': 'dotplot_alpha_7_beta_3_n_100_points_1', 'score': 1},
    			 'gymnast2': {'name': 'Koester', 'sample': 100, 'current': 'dotplot_alpha_7_beta_3_n_100_points_3', 'score': 3},
    			 'outcome': 'FAILURE', 'attribute': 'blame', 'color': 'maroon', 'succfail': 'failed', 'didnot': 'did not meet'
    			},	
    		35: {'gymnast1': {'name': 'Cowell', 'sample': 20, 'current': 'dotplot_alpha_7_beta_3_n_20_points_7', 'score': 7},
    			 'gymnast2': {'name': 'Baldauf', 'sample': 20, 'current': 'dotplot_alpha_7_beta_3_n_20_points_9', 'score': 9},
    			 'outcome': 'SUCCESS', 'attribute': 'credit', 'color': 'darkgreen', 'succfail': 'succeeded', 'didnot': 'exceeded'
    			},
    		36: {'gymnast1': {'name': 'Kallina', 'sample': 100, 'current': 'dotplot_alpha_7_beta_3_n_100_points_7', 'score': 7},
    			 'gymnast2': {'name': 'Eatton', 'sample': 100, 'current': 'dotplot_alpha_7_beta_3_n_100_points_9', 'score': 9},
    			 'outcome': 'SUCCESS', 'attribute': 'credit', 'color': 'darkgreen', 'succfail': 'succeeded', 'didnot': 'exceeded'
    			},
    		37: {'gymnast1': {'name': 'Calhoun', 'sample': 20, 'current': 'dotplot_alpha_3_beta_7_n_20_points_1', 'score': 1},
    			 'gymnast2': {'name': 'Harroun', 'sample': 100, 'current': 'dotplot_alpha_3_beta_7_n_100_points_1', 'score': 1},
    			 'outcome': 'FAILURE', 'attribute': 'blame', 'color': 'maroon', 'succfail': 'failed', 'didnot': 'did not meet'
    			},
    		38: {'gymnast1': {'name': 'Palomar', 'sample': 20, 'current': 'dotplot_alpha_3_beta_7_n_20_points_3', 'score': 3},
    			 'gymnast2': {'name': 'Gregson', 'sample': 100, 'current': 'dotplot_alpha_3_beta_7_n_100_points_3', 'score': 3},
    			 'outcome': 'FAILURE', 'attribute': 'blame', 'color': 'maroon', 'succfail': 'failed', 'didnot': 'did not meet'
    			},
    		39: {'gymnast1': {'name': 'Hatfield', 'sample': 20, 'current': 'dotplot_alpha_3_beta_7_n_20_points_7', 'score': 7},
    			 'gymnast2': {'name': 'Vaughan', 'sample': 100, 'current': 'dotplot_alpha_3_beta_7_n_100_points_7', 'score': 7},
    			 'outcome': 'SUCCESS', 'attribute': 'credit', 'color': 'darkgreen', 'succfail': 'succeeded', 'didnot': 'exceeded'
    			},
    		40: {'gymnast1': {'name': 'Younan', 'sample': 20, 'current': 'dotplot_alpha_3_beta_7_n_20_points_9', 'score': 9},
    			 'gymnast2': {'name': 'Siddiqi', 'sample': 100, 'current': 'dotplot_alpha_3_beta_7_n_100_points_9', 'score': 9},
    			 'outcome': 'SUCCESS', 'attribute': 'credit', 'color': 'darkgreen', 'succfail': 'succeeded', 'didnot': 'exceeded'
    			},
    		41: {'gymnast1': {'name': 'Beydoun', 'sample': 20, 'current': 'dotplot_alpha_5_beta_5_n_20_points_1', 'score': 1},
    			 'gymnast2': {'name': 'Adkins', 'sample': 100, 'current': 'dotplot_alpha_5_beta_5_n_100_points_1', 'score': 1},
    			 'outcome': 'FAILURE', 'attribute': 'blame', 'color': 'maroon', 'succfail': 'failed', 'didnot': 'did not meet'
    			},
    		42: {'gymnast1': {'name': 'Stauffer', 'sample': 20, 'current': 'dotplot_alpha_5_beta_5_n_20_points_3', 'score': 3},
    			 'gymnast2': {'name': 'Wallace', 'sample': 100, 'current': 'dotplot_alpha_5_beta_5_n_100_points_3', 'score': 3},
    			 'outcome': 'FAILURE', 'attribute': 'blame', 'color': 'maroon', 'succfail': 'failed', 'didnot': 'did not meet'
    			},
    		43: {'gymnast1': {'name': 'Nguyen', 'sample': 20, 'current': 'dotplot_alpha_5_beta_5_n_20_points_7', 'score': 7},
    			 'gymnast2': {'name': 'Sengdara', 'sample': 100, 'current': 'dotplot_alpha_5_beta_5_n_100_points_7', 'score': 7},
    			 'outcome': 'SUCCESS', 'attribute': 'credit', 'color': 'darkgreen', 'succfail': 'succeeded', 'didnot': 'exceeded'
    			},
    		44: {'gymnast1': {'name': 'Moline', 'sample': 20, 'current': 'dotplot_alpha_5_beta_5_n_20_points_9', 'score': 9},
    			 'gymnast2': {'name': 'Sebben', 'sample': 100, 'current': 'dotplot_alpha_5_beta_5_n_100_points_9', 'score': 9},
    			 'outcome': 'SUCCESS', 'attribute': 'credit', 'color': 'darkgreen', 'succfail': 'succeeded', 'didnot': 'exceeded'
    			},
    		45: {'gymnast1': {'name': 'Pacheco', 'sample': 20, 'current': 'dotplot_alpha_7_beta_3_n_20_points_1', 'score': 1},
    			 'gymnast2': {'name': 'Carrera', 'sample': 100, 'current': 'dotplot_alpha_7_beta_3_n_100_points_1', 'score': 1},
    			 'outcome': 'FAILURE', 'attribute': 'blame', 'color': 'maroon', 'succfail': 'failed', 'didnot': 'did not meet'
    			},
    		46: {'gymnast1': {'name': 'Rahman', 'sample': 20, 'current': 'dotplot_alpha_7_beta_3_n_20_points_3', 'score': 3},
    			 'gymnast2': {'name': 'Eshima', 'sample': 100, 'current': 'dotplot_alpha_7_beta_3_n_100_points_3', 'score': 3},
    			 'outcome': 'FAILURE', 'attribute': 'blame', 'color': 'maroon', 'succfail': 'failed', 'didnot': 'did not meet'
    			},
    		47: {'gymnast1': {'name': 'Trobee', 'sample': 20, 'current': 'dotplot_alpha_7_beta_3_n_20_points_7', 'score': 7},
    			 'gymnast2': {'name': 'Galasso', 'sample': 100, 'current': 'dotplot_alpha_7_beta_3_n_100_points_7', 'score': 7},
    			 'outcome': 'SUCCESS', 'attribute': 'credit', 'color': 'darkgreen', 'succfail': 'succeeded', 'didnot': 'exceeded'
    			},
    		48: {'gymnast1': {'name': 'Hollins', 'sample': 20, 'current': 'dotplot_alpha_7_beta_3_n_20_points_9', 'score': 9},
    			 'gymnast2': {'name': 'Stewart', 'sample': 100, 'current': 'dotplot_alpha_7_beta_3_n_100_points_9', 'score': 9},
    			 'outcome': 'SUCCESS', 'attribute': 'credit', 'color': 'darkgreen', 'succfail': 'succeeded', 'didnot': 'exceeded'
    			},	 
    		}


class Subsession(BaseSubsession):
	def creating_session(self):
		image_index = self.round_number - 1

		if self.round_number == 1:
			for p in self.get_players():
				# copy in the stimuli keys and shuffle them
				pairs = Constants.pairs.copy()
				pairs_sequence = list(range(1, 49))

				random.shuffle(pairs_sequence)

				# order counterbalances display of stimuli (right or left side of screen)
				order_cycle = random.uniform(1, 2)
				order = round(order_cycle)
				
				# record sequence of stimuli as participant variable
				p.participant.vars['pairs_sequence'] = pairs_sequence

				pairs_list = pairs_sequence
				
				# record stim attributes
				pair_id = pairs_list[image_index]
				p.pair_id = pair_id
				p.pair_outcome = pairs[pair_id]['outcome']
				p.pair_attribute = pairs[pair_id]['attribute']
				p.color = pairs[pair_id]['color']
				p.succfail = pairs[pair_id]['succfail']
				p.didnot = pairs[pair_id]['didnot']              
				if order == 1:
					p.order = 1
					p.stim_name1 = pairs[pair_id]['gymnast1']['name']
					p.stim_sample1 = pairs[pair_id]['gymnast1']['sample']
					p.stim_current1 = pairs[pair_id]['gymnast1']['current']
					p.stim_score1 = pairs[pair_id]['gymnast1']['score']

					p.stim_name2 = pairs[pair_id]['gymnast2']['name']
					p.stim_sample2 = pairs[pair_id]['gymnast2']['sample']
					p.stim_current2 = pairs[pair_id]['gymnast2']['current']
					p.stim_score2 = pairs[pair_id]['gymnast2']['score']
				else:
					p.order = 2
					p.stim_name1 = pairs[pair_id]['gymnast2']['name']
					p.stim_sample1 = pairs[pair_id]['gymnast2']['sample']
					p.stim_current1 = pairs[pair_id]['gymnast2']['current']
					p.stim_score1 = pairs[pair_id]['gymnast2']['score']

					p.stim_name2 = pairs[pair_id]['gymnast1']['name']
					p.stim_sample2 = pairs[pair_id]['gymnast1']['sample']
					p.stim_current2 = pairs[pair_id]['gymnast1']['current']
					p.stim_score2 = pairs[pair_id]['gymnast1']['score']
			print(pair_id, order)
		else:
			for p in self.get_players():
				pairs = Constants.pairs.copy()

				order_cycle = random.uniform(1, 2)
				order = round(order_cycle)

				# pull sequence of stimuli out of participant vars as list
				pairs_list = p.participant.vars['pairs_sequence']
				
				# record stim attributes
				pair_id = pairs_list[image_index]
				p.pair_id = pair_id
				p.pair_outcome = pairs[pair_id]['outcome']
				p.pair_attribute = pairs[pair_id]['attribute']
				p.color = pairs[pair_id]['color']
				p.succfail = pairs[pair_id]['succfail']
				p.didnot = pairs[pair_id]['didnot'] 				
				if order == 1:
					p.order = 1
					p.stim_name1 = pairs[pair_id]['gymnast1']['name']
					p.stim_sample1 = pairs[pair_id]['gymnast1']['sample']
					p.stim_current1 = pairs[pair_id]['gymnast1']['current']
					p.stim_score1 = pairs[pair_id]['gymnast1']['score']

					p.stim_name2 = pairs[pair_id]['gymnast2']['name']
					p.stim_sample2 = pairs[pair_id]['gymnast2']['sample']
					p.stim_current2 = pairs[pair_id]['gymnast2']['current']
					p.stim_score2 = pairs[pair_id]['gymnast2']['score']
				else:
					p.order = 2
					p.stim_name1 = pairs[pair_id]['gymnast2']['name']
					p.stim_sample1 = pairs[pair_id]['gymnast2']['sample']
					p.stim_current1 = pairs[pair_id]['gymnast2']['current']
					p.stim_score1 = pairs[pair_id]['gymnast2']['score']

					p.stim_name2 = pairs[pair_id]['gymnast1']['name']
					p.stim_sample2 = pairs[pair_id]['gymnast1']['sample']
					p.stim_current2 = pairs[pair_id]['gymnast1']['current']
					p.stim_score2 = pairs[pair_id]['gymnast1']['score']
		print(pair_id, order)

class Group(BaseGroup):
    pass


class Player(BasePlayer):
	comprehension1 = models.IntegerField(
        choices=[[1, '5 points'],[2, '7 points'], [3, '4 points']],
        widget=widgets.RadioSelect
        )
	comprehension3 = models.IntegerField(
        choices=[[1, 'Each dot represents one of the points the gymnast earned today'],
        		[2, 'Each dot represents a score the gymnast earned in a past competition'], 
        		[3, 'Each dot represents a special move performed by the gymnast']],
        widget=widgets.RadioSelect
        )
	comprehension4 = models.IntegerField(
        choices=[[1, '5 points'],[2, '7 points'], [3, '2 points']],
        widget=widgets.RadioSelect
        )

	order = models.IntegerField()
	pair_id = models.IntegerField()
	pair_outcome = models.CharField()
	pair_attribute = models.CharField()
	color = models.CharField()
	succfail = models.CharField()
	didnot = models.CharField()
	stim_name1 = models.CharField()
	stim_name1 = models.CharField()
	stim_name2 = models.CharField()
	stim_sample1 = models.IntegerField()
	stim_sample2 = models.IntegerField()
	stim_current1 = models.CharField()
	stim_current2 = models.CharField()
	stim_score1 = models.CharField()
	stim_score2 = models.CharField()

	attribution = models.IntegerField(
    	widget=widgets.Slider(attrs={'step': '1.00'},
    		show_value=False))

