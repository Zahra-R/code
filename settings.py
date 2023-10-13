from os import environ


SESSION_CONFIGS = [
    ### EDEG -3
    dict(
        name='EDEG_study_FullDesing_Reps', 
        app_sequence=['EDEGIntro', 'EDEG3', 'EDEGScales',], 
        num_demo_participants=16, 
        group = "reps"
    ),

    dict(
        name='EDEG_study2_FullDesign_Dems', 
        app_sequence=['EDEGIntro', 'EDEG3', 'EDEGScales',], 
        num_demo_participants=5, 
        group = "dems"
    ),

    dict(
        name='EDEG_study2_Salient_PayoffSwitches_SafeEmitsFirst',
        app_sequence=['EDEGIntro', 'EDEG3', 'EDEGScales',], 
        num_demo_participants=10,
        Salience= True,
        PayoffSwitches = False
    ),
   

]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = [
    # EDEG FIELDS
    'Exp_Con',
    'Salience',
    'reversedbuttons',
    'outcomeA',
    'outcomeB',
    'chosen_round',
    'chosen_round_outcome',
    'chosen_round_choice',
    'chosen_round_choice_depict',
    'chosen_round_carbon',
    'payoff_decimal',
    'game_rounds', 
    'finished',
    'SwitchPayoffs',
    'Block1CarbonLeft',
    'Block1CarbonRight',
    'Block2CarbonLeft',
    'Block2CarbonRight'
]


SESSION_FIELDS = [
]

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'GBP'
USE_POINTS = False

ROOMS = [
    dict(
        name='econ101',
        display_name='Econ 101 class',
        participant_label_file='_rooms/econ101.txt',
    ),
    dict(name='live_demo', display_name='Room for live demo (no participant labels)'),
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""


SECRET_KEY = '3153268574945'

INSTALLED_APPS = ['otree']
