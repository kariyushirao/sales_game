import os
from os import environ

import dj_database_url
from boto.mturk import qualification

import otree.settings


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# the environment variable OTREE_PRODUCTION controls whether Django runs in
# DEBUG mode. If OTREE_PRODUCTION==1, then DEBUG=False
if environ.get('OTREE_PRODUCTION') not in {None, '', '0'}:
    DEBUG = False
else:
    DEBUG = True

# don't share this with anybody.
SECRET_KEY = '=zx=7j0vl1cc($jp%axd--wwc@fx1b6dfowieux3$64$j5e^zd'


DATABASES = {
    'default': dj_database_url.config(
        # Rather than hardcoding the DB parameters here,
        # it's recommended to set the DATABASE_URL environment variable.
        # This will allow you to use SQLite locally, and postgres/mysql
        # on the server
        # Examples:
        # export DATABASE_URL=postgres://USER:PASSWORD@HOST:PORT/NAME
        # export DATABASE_URL=mysql://USER:PASSWORD@HOST:PORT/NAME

        # fall back to SQLite if the DATABASE_URL env var is missing
        default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
    )
}

# AUTH_LEVEL:
# this setting controls which parts of your site are freely accessible,
# and which are password protected:
# - If it's not set (the default), then the whole site is freely accessible.
# - If you are launching a study and want visitors to only be able to
#   play your app if you provided them with a start link, set it to STUDY.
# - If you would like to put your site online in public demo mode where
#   anybody can play a demo version of your game, but not access the rest
#   of the admin interface, set it to DEMO.

# sentry account
SENTRY_DSN = 'http://b8fc561a3b23401ba162d355df0c4990:a2bf0845f5f6452093aa9dc5a0b9820a@sentry.otree.org/246'

# for flexibility, you can set it in the environment variable OTREE_AUTH_LEVEL
AUTH_LEVEL = environ.get('OTREE_AUTH_LEVEL')

ADMIN_USERNAME = 'kdizzle'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')


# setting for integration with AWS Mturk
AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')


# e.g. EUR, CAD, GBP, CHF, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False


# e.g. en, de, fr, it, ja, zh-hans
# see: https://docs.djangoproject.com/en/1.9/topics/i18n/#term-language-code
LANGUAGE_CODE = 'en'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']

# SENTRY_DSN = ''

DEMO_PAGE_INTRO_TEXT = """
<ul>
    <li>
        <a href="https://github.com/oTree-org/otree" target="_blank">
            oTree on GitHub
        </a>.
    </li>
    <li>
        <a href="http://www.otree.org/" target="_blank">
            oTree homepage
        </a>.
    </li>
</ul>
<p>
    Here are various games implemented with oTree. These games are all open
    source, and you can modify them as you wish.
</p>
"""

ROOMS = [
    {
        'name': 'RaoWebLab',
        'display_name': 'Rao Web Lab',
        # 'participant_label_file': '_rooms/econ101.txt',
    },
    {
        'name': 'live_demo',
        'display_name': 'Room for live demo (no participant labels)',
    },
]


# from here on are qualifications requirements for workers
# see description for requirements on Amazon Mechanical Turk website:
# http://docs.aws.amazon.com/AWSMechTurk/latest/AWSMturkAPI/ApiReference_QualificationRequirementDataStructureArticle.html
# and also in docs for boto:
# https://boto.readthedocs.org/en/latest/ref/mturk.html?highlight=mturk#module-boto.mturk.qualification

mturk_hit_settings = {
    'keywords': ['easy', 'brief', 'choice', 'prediction', 'study', 'short', 'experiment'],
    'title': 'Quick game with short survey',
    'description': 'A quick experiment about making predictions in games. Less than 15 minutes to complete.',
    'frame_height': 500,
    'preview_template': 'global/MTurkPreview.html',
    'minutes_allotted_per_assignment': 60,
    'expiration_hours': 1*24, # 1 day
    # flags workers once they've completed the task (currently set to responsibility expectations)
    'grant_qualification_id': '3U4RTBK6TCJR6ZG8XM0M3T5YE3KU20',
    'qualification_requirements': [
        # prevents workers from completing responsibility expectations again after receiving flag
        {
            'QualificationTypeId': "3U4RTBK6TCJR6ZG8XM0M3T5YE3KU20",
            'Comparator': "DoesNotExist",
        },
        # requires workers be located in the US
        {
            'QualificationTypeId': '00000000000000000071',
            'Comparator': "EqualTo",
            'LocaleValues': [{'Country': "US"}],
        },
        # requires workers to have completed at least 5 HITs
        {
            'QualificationTypeId': '00000000000000000040',
            'Comparator': "GreaterThan",
            'IntegerValues': [5],
        },
        # requires workers to have HIT approval rate of at least 95 percent
        {
            'QualificationTypeId': '000000000000000000L0',
            'Comparator': "GreaterThanOrEqualTo",
            'IntegerValues': [95],
        },
    ]
}


# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 0.001,
    'participation_fee': 3.00,
    'doc': "",
    'mturk_hit_settings': mturk_hit_settings,
}

SESSION_CONFIGS = [
    {
        'name': 'my_public_goods',
        'display_name': "My Public Goods (Simple Version)",
        'num_demo_participants': 3,
        'app_sequence': ['my_public_goods', 'survey', 'payment_info'],
        'use_browser_bots': False
    },
    {
        'name': 'public_goods',
        'display_name': "Public Goods",
        'num_demo_participants': 3,
        'app_sequence': ['public_goods', 'payment_info'],
    },
    {
        'name': 'my_trust',
        'display_name': "My Trust Game (simple version from tutorial)",
        'num_demo_participants': 2,
        'app_sequence': ['my_trust'],
    },
    {
        'name': 'trust',
        'display_name': "Trust Game",
        'num_demo_participants': 2,
        'app_sequence': ['trust', 'payment_info'],
    },
    {
        'name': 'consent',
        'display_name': "Consent Form",
        'num_demo_participants': 1,
        'app_sequence': ['consent'],
    },
    {
        'name': 'guess_two_thirds',
        'display_name': "Guess 2/3 of the Average",
        'num_demo_participants': 3,
        'app_sequence': ['guess_two_thirds', 'payment_info'],
    },
    {
        'name': 'guess_two_thirds_novice',
        'treatment': 'novice',
        'display_name': "Guess 2/3 Novice",
        'num_demo_participants': 3,
        'app_sequence': ['guess_two_thirds', 'payment_info'],
    },
    {
        'name': 'guess_two_thirds_expert',
        'treatment': 'expert',
        'display_name': "Guess 2/3 Expert",
        'num_demo_participants': 3,
        'app_sequence': ['guess_two_thirds', 'payment_info'],
    },
    {
        'name': 'headwind_tailwind',
        'display_name': "Headwind Tailwind",
        'num_demo_participants': 1,
        'app_sequence': ['headwind_tailwind','snowy_pictures', 'survey'],
    },
    {
        'name': 'headwind_tailwind_hw',
        'treatment': 'headwind',
        'display_name': "Headwind Tailwind (Headwind)",
        'num_demo_participants': 1,
        'app_sequence': ['headwind_tailwind','snowy_pictures', 'survey'],
    },
    {
        'name': 'headwind_tailwind_tw',
        'treatment': 'tailwind',
        'display_name': "Headwind Tailwind (Tailwind)",
        'num_demo_participants': 1,
        'app_sequence': ['headwind_tailwind', 'snowy_pictures', 'survey'],
    },
    {
        'name': 'headwind_tailwind_ne',
        'treatment': 'neutral',
        'display_name': "Headwind Tailwind (Neutral)",
        'num_demo_participants': 1,
        'app_sequence': ['headwind_tailwind'],
    },
    {
        'name': 'whatsnext',
        'display_name': 'Whats Next',
        'num_demo_participants': 1,
        'app_sequence': ['whatsnext'],
    },
    {
        'name': 'whatsnext_coins',
        'treatment': 'coins',
        'display_name': 'Whats Next Coins',
        'num_demo_participants': 1,
        'app_sequence': ['whatsnext'],
    },
    {
        'name': 'whatsnext_analyst',
        'treatment': 'analyst',
        'display_name': 'Whats Next Analyst',
        'num_demo_participants': 1,
        'app_sequence': ['whatsnext'],
    },
    {
        'name': 'snowy_pictures',
        'display_name': "Snowy Pictures",
        'num_demo_participants': 1,
        'app_sequence': ['snowy_pictures'],
    },
    {
        'name': 'coin_flipping',
        'display_name': "Coin Flipping",
        'num_demo_participants': 1,
        'app_sequence': ['coin_flipping','FIT'],
    },
    # {
    #     'name': 'survey',
    #     'display_name': "Survey",
    #     'num_demo_participants': 1,
    #     'app_sequence': ['survey', 'payment_info'],
    # },
    {
        'name': 'quiz',
        'display_name': "Quiz",
        'num_demo_participants': 1,
        'app_sequence': ['quiz'],
    },
    {   
        'name': 'FIT',
        'display_name': "FIT",
        'num_demo_participants': 1,
        'app_sequence': ['FIT'],
    },
    {   
        'name': 'responsibility_attribution',
        'display_name': "Responsibility Attribution",
        'num_demo_participants': 1,
        'app_sequence': ['responsibility_attribution','demographics'],
    },
    {   
        'name': 'responsibility_attribution_e',
        'treatment': 'experience',
        'display_name': "Responsibility Attribution (Experience)",
        'num_demo_participants': 1,
        'app_sequence': ['responsibility_attribution','demographics'],
    },
    {   
        'name': 'responsibility_attribution_r',
        'treatment': 'random',
        'display_name': "Responsibility Attribution (Random)",
        'num_demo_participants': 1,
        'app_sequence': ['responsibility_attribution','demographics'],
    },
    {   
        'name': 'responsibility_attribution_compare',
        'display_name': "Responsibility Attribution Compare",
        'num_demo_participants': 1,
        'app_sequence': ['responsibility_attribution_compare','demographics'],
    },
    {
        'name': 'prisoner',
        'display_name': "Prisoner's Dilemma",
        'num_demo_participants': 2,
        'app_sequence': ['prisoner', 'payment_info'],
    },
    {
        'name': 'ultimatum',
        'display_name': "Ultimatum (randomized: strategy vs. direct response)",
        'num_demo_participants': 2,
        'app_sequence': ['ultimatum', 'payment_info'],
    },
    {
        'name': 'ultimatum_strategy',
        'display_name': "Ultimatum (strategy method treatment)",
        'num_demo_participants': 2,
        'app_sequence': ['ultimatum', 'payment_info'],
        'use_strategy_method': True,
    },
    {
        'name': 'ultimatum_non_strategy',
        'display_name': "Ultimatum (direct response treatment)",
        'num_demo_participants': 2,
        'app_sequence': ['ultimatum', 'payment_info'],
        'use_strategy_method': False,
    },
    {
        'name': 'vickrey_auction',
        'display_name': "Vickrey Auction",
        'num_demo_participants': 3,
        'app_sequence': ['vickrey_auction', 'payment_info'],
    },
    {
        'name': 'volunteer_dilemma',
        'display_name': "Volunteer's Dilemma",
        'num_demo_participants': 3,
        'app_sequence': ['volunteer_dilemma', 'payment_info'],
    },
    {
        'name': 'cournot',
        'display_name': "Cournot Competition",
        'num_demo_participants': 2,
        'app_sequence': [
            'cournot', 'payment_info'
        ],
    },
    {
        'name': 'principal_agent',
        'display_name': "Principal Agent",
        'num_demo_participants': 2,
        'app_sequence': ['principal_agent', 'payment_info'],
    },
    {
        'name': 'dictator',
        'display_name': "Dictator Game",
        'num_demo_participants': 2,
        'app_sequence': ['dictator', 'payment_info'],
    },
    {
        'name': 'matching_pennies',
        'display_name': "Matching Pennies",
        'num_demo_participants': 2,
        'app_sequence': [
            'matching_pennies',
        ],
    },
    {
        'name': 'traveler_dilemma',
        'display_name': "Traveler's Dilemma",
        'num_demo_participants': 2,
        'app_sequence': ['traveler_dilemma', 'payment_info'],
    },
    {
        'name': 'bargaining',
        'display_name': "Bargaining Game",
        'num_demo_participants': 2,
        'app_sequence': ['bargaining', 'payment_info'],
    },
    {
        'name': 'common_value_auction',
        'display_name': "Common Value Auction",
        'num_demo_participants': 3,
        'app_sequence': ['common_value_auction', 'payment_info'],
    },
    {
        'name': 'stackelberg',
        'display_name': "Stackelberg Competition",
        'real_world_currency_per_point': 0.01,
        'num_demo_participants': 2,
        'app_sequence': [
            'stackelberg', 'payment_info'
        ],
    },
    {
        'name': 'bertrand',
        'display_name': "Bertrand Competition",
        'num_demo_participants': 2,
        'app_sequence': [
            'bertrand', 'payment_info'
        ],
    },
    {
        'name': 'real_effort',
        'display_name': "Real-effort transcription task",
        'num_demo_participants': 1,
        'app_sequence': [
            'real_effort',
        ],
    },
    {
        'name': 'lemon_market',
        'display_name': "Lemon Market Game",
        'num_demo_participants': 3,
        'app_sequence': [
            'lemon_market', 'payment_info'
        ],
    },
    {
        'name': 'battle_of_the_sexes',
        'display_name': "Battle of the Sexes",
        'num_demo_participants': 2,
        'app_sequence': [
            'battle_of_the_sexes', 'payment_info'
        ],
    },
    {
        'name': 'public_goods_simple',
        'display_name': "Public Goods (simple version from tutorial)",
        'num_demo_participants': 3,
        'app_sequence': ['public_goods_simple', 'survey', 'payment_info'],
    },
    {
        'name': 'trust_simple',
        'display_name': "Trust Game (simple version from tutorial)",
        'num_demo_participants': 2,
        'app_sequence': ['trust_simple'],
    },
    {
        'name': 'demographics',
        'display_name': "Demographics",
        'num_demo_participants': 1,
        'app_sequence': ['demographics'],
    },

]

# anything you put after the below line will override
# oTree's default settings. Use with caution.
otree.settings.augment_settings(globals())
