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

# AUTH_LEVEL:
# this setting controls which parts of your site are freely accessible,
# and which are password protected:
# - If it's not set (the default), then the whole site is freely accessible.
# - If you are launching a study and want visitors to only be able to
#   play your app if you provided them with a start link, set it to STUDY.
# - If you would like to put your site online in public demo mode where
#   anybody can play a demo version of your game, but not access the rest
#   of the admin interface, set it to DEMO.

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
USE_POINTS = True


# e.g. en, de, fr, it, ja, zh-hans
# see: https://docs.djangoproject.com/en/1.9/topics/i18n/#term-language-code
LANGUAGE_CODE = 'en'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']

# EXTENSION_APPS = ['otree_tools', 'otree_mturk_utils',]

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
    'keywords': ['experiment', 'academic'],
    'title': 'academic experiment',
    'description': 'An academic experiment.',
    'frame_height': 500,
    'preview_template': 'global/MTurkPreview.html',
    'minutes_allotted_per_assignment': 120,
    'expiration_hours': 2, 
    # flags workers once they've completed the experiment 
    # 'grant_qualification_id': '',
    'qualification_requirements': [
        # prevents workers from completing experiment again after receiving flag
        # {
        #    'QualificationTypeId': '',
        #    'Comparator': "DoesNotExist",
        # },
        # requires workers be located in the US
        {
            'QualificationTypeId': '00000000000000000071',
            'Comparator': "EqualTo",
            'LocaleValues': [{'Country': "US"}],
        },
        # requires workers to have completed at least 500 HITs
        {
            'QualificationTypeId': '00000000000000000040',
            'Comparator': "GreaterThan",
            'IntegerValues': [500],
        },
        # requires workers to have HIT approval rate of at least 98 percent
        {
            'QualificationTypeId': '000000000000000000L0',
            'Comparator': "GreaterThanOrEqualTo",
            'IntegerValues': [98],
        },
    ]
}


# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 0.0001,
    'participation_fee': 6.00,
    'doc': "",
    'mturk_hit_settings': mturk_hit_settings,
}

SESSION_CONFIGS = [
    {
        'name': 'p_beauty',
        'display_name': "P-Beauty Contest",
        'num_demo_participants': 3,
        'app_sequence': ['p_beauty'],
    },
    {
        'name': 'solo_sales_game',
        'display_name': "Solo Sales Game",
        'num_demo_participants': 1,
        'app_sequence': ['solo_sales_game_instructions','solo_sales_game'],
    },
    {
        'name': 'solo_sales_game_control',
        'display_name': "Solo Sales Game CONTROL",
        'num_demo_participants': 1,
        'app_sequence': ['solo_sales_game_instructions','solo_sales_game'],
        'treatment': 'control'
    },
    {
        'name': 'solo_sales_game_abundance',
        'display_name': "Solo Sales Game ABUNDANCE",
        'num_demo_participants': 1,
        'app_sequence': ['solo_sales_game_instructions','solo_sales_game'],
        'treatment': 'abundance'
    },
    {
        'name': 'solo_sales_game_scarcity',
        'display_name': "Solo Sales Game SCARCITY",
        'num_demo_participants': 1,
        'app_sequence': ['solo_sales_game_instructions','solo_sales_game'],
        'treatment': 'scarcity'
    },
    {
        'name': 'social_sales_game',
        'display_name': "Social Sales Game",
        'num_demo_participants': 6,
        'app_sequence': ['social_sales_game_instructions','social_sales_game'],
    },
    {
        'name': 'social_sales_game_control',
        'display_name': "Social Sales Game CONTROL",
        'num_demo_participants': 6,
        'app_sequence': ['social_sales_game_instructions','social_sales_game'],
        'treatment': 'control'
    },
    {
        'name': 'social_sales_game_abundance',
        'display_name': "Social Sales Game ABUNDANCE",
        'num_demo_participants': 6,
        'app_sequence': ['social_sales_game_instructions','social_sales_game'],
        'treatment': 'abundance'
    },
    {
        'name': 'social_sales_game_scarcity',
        'display_name': "Social Sales Game SCARCITY",
        'num_demo_participants': 6,
        'app_sequence': ['social_sales_game_instructions','social_sales_game'],
        'treatment': 'scarcity'
    },
]

# anything you put after the below line will override
# oTree's default settings. Use with caution.
otree.settings.augment_settings(globals())
