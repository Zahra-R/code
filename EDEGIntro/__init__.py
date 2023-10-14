from random import random, seed, choice as random_choice, randint
from otree.api import *
import numpy as np
#import scipy.stats as stats

author = 'Zahra Rahmani'
doc = """
Description Experience Gap with Carbon Externalities
"""

class C(BaseConstants):
    NAME_IN_URL = 'EDEG_Intro'
    PLAYERS_PER_GROUP = None
    ROUNDS_PER_CONDITION = 1
    NUM_ROUNDS = 1
    NUM_ROUNDS_Game = 6
    ROUNDS_PER_BLOCK = NUM_ROUNDS_Game/2
    carbon = 30
    safe_outcome = 7
    high_lottery = 30 # typical outcome of the lottery
    low_lottery = -200 # rare disaster 


class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    Exp_Con = models.IntegerField()  # This is a between subjects variable, 1 is first block safe is neutral, 2 is first block safe is carbon negative
    SwitchPayoffs = models.BooleanField()
    Salience = models.BooleanField()
    safeLeftBlock1 = models.BooleanField()
    dataScience = models.BooleanField(initial=False)
    dataTeach = models.BooleanField(initial=False)
    realEmissions = models.IntegerField(choices=[[1,'True'], [0,'False']], label="Does the decision that will determine your bonus have a real consequence for the environment?")
    attention = models.StringField(max_length=60, blank=True)
    # attention2 = models.StringField(max_length=360, blank=True)
    mobileDevice= models.BooleanField(initial=False, blank=True)
    prolificIDMissing= models.BooleanField(initial=False)
    amountEmissionsLeft = models.IntegerField(blank = True, min_length=1)
    amountEmissionsRight = models.IntegerField(blank = True, min_length=1)
    leftEmissionsCorrect = models.BooleanField( blank=True)
    rightEmissionsCorrect = models.BooleanField( blank=True)
    #amountEmissionsRisky2 = models.IntegerField(blank = True, min_length=1)
    #amountEmissionsSafe2 = models.IntegerField(blank = True, min_length=1)
    preference = models.StringField( choices=[ 'A', 'B'])  # , widget=widgets.RadioSelect)
    prefersEmissions = models.BooleanField( blank=True)
    riskyCausesEmissions = models.BooleanField( blank=True)

    carbon_left = models.IntegerField() 
    carbon_right = models.IntegerField() 
    riskyLeft = models.BooleanField()
    riskyCarbon = models.BooleanField()
    real_preference = models.StringField()
    preference_carbon = models.IntegerField()
    salient = models.BooleanField()
    
    
    
# FUNCTIONS

def creating_session(subsession: Subsession):
    import itertools
    conditions = itertools.cycle([1, 2])
    reverse_display = itertools.cycle([True, True, True, True, True, True, True, True, False, False, False, False, False, False, False, False])
    salientEmissions = itertools.cycle([True, True, False, False])
    blockswitchPayoffs = itertools.cycle([True, True, True, True, False, False, False, False])
    # randomize to treatments
    for player in subsession.get_players():
        if subsession.round_number == 1:
            if 'Exp_Con' in player.session.config:
                # Exp_Con = 1 means in first block, risky choices cause emissions, in second block risky choices are co2 neutral
                # Exp_ con 2 means in first block, risky choices are carbon netral, in second block, risky choices cause emissions
                player.Exp_Con = player.session.config['Exp_Con']
            else:
                player.Exp_Con = next(conditions)
            if 'Salience' in player.session.config:
                player.Salience = player.session.config['Salience']
            else:
                player.Salience = next(salientEmissions)
            if 'PayoffSwitches' in player.session.config: 
                player.SwitchPayoffs = player.session.config['PayoffSwitches']
            else:
                player.SwitchPayoffs = next(blockswitchPayoffs)

            ## reversed buttons TRUE means risky option is left, fALSE means risky option is right 
            player.safeLeftBlock1 = next(reverse_display)

            player.participant.Exp_Con=player.Exp_Con
            player.participant.safeLeftBlock1= player.safeLeftBlock1
            player.participant.Salience = player.Salience
            player.participant.SwitchPayoffs = player.SwitchPayoffs


def make_choice(player: Player, choiceMade):
    if choiceMade == 'A':
        player.real_preference = "Safe" if player.riskyLeft == False else "Risky"
    if choiceMade == 'B': 
        player.real_preference = "Safe" if player.riskyLeft == True else "Risky"
    
    if player.real_preference == "Safe":
        player.preference_carbon = C.carbon if player.riskyCarbon == False else 0
    if player.real_preference == "Risky":
        player.preference_carbon = C.carbon if player.riskyCarbon == True else 0


def attention_check_emissions(player: Player, emissionsLeft, emissionsRight):
    player.rightEmissionsCorrect = True if emissionsRight == player.carbon_right else False
    player.leftEmissionsCorrect = True if emissionsLeft  == player.carbon_left else False


# ---------------------------------------------------------------
# ------------------- PAGES--------------------------------------
#----------------------------------------------------------------
class Consent(Page):
    form_model = 'player'
    form_fields = ['dataScience', 'dataTeach', 'mobileDevice']
    
    @staticmethod
    def vars_for_template(player: Player):
        # while testing this experiment do not check for prolificID (replace False with commented code) (make nolabel and prolificID Missing false for testing)
        player.prolificIDMissing = player.participant.label == None
        return {
            "particpantlabel": player.participant.label,
            "nolabel": False # player.participant.label == None
            }
    


class Intro_1(Page):
    form_model = 'player'

    @staticmethod
    def vars_for_template(player: Player):
        Exp_Con = player.in_round(1).Exp_Con
        return {
            'num_rounds': player.participant.game_rounds,
            'Exp_Con': Exp_Con
            }

    
class Intro_2(Page):
    form_model = 'player'
    form_fields = ['realEmissions']

    @staticmethod
    def vars_for_template(player: Player):
        Exp_Con = player.in_round(1).Exp_Con
        return {
            'num_rounds': player.participant.game_rounds,
            'Exp_Con': Exp_Con
            }
    
class Intro_3(Page):
    form_model = 'player'
    form_fields = ['attention']

    @staticmethod
    def vars_for_template(player: Player):
        Exp_Con = player.in_round(1).Exp_Con
        return {
            'num_rounds': player.participant.game_rounds,
            'Exp_Con': Exp_Con
            }

    
class NotAtt(Page):
    form_model = 'player'
    form_fields = ['attention2']
    @staticmethod
    def vars_for_template(player: Player):
        Exp_Con = player.in_round(1).Exp_Con
        return {'num_rounds': player.participant.game_rounds,
                'Exp_Con': Exp_Con}

    @staticmethod
    def is_displayed(player: Player):
        if player.in_round(1).attention is None:
            return True
        else:
            return not("thank" in player.in_round(1).attention.lower())
        

class Preview_Game(Page):
    form_model = 'player'
    form_fields = ['amountEmissionsLeft', 'amountEmissionsRight']

    @staticmethod
    def vars_for_template(player: Player):
        Salience = player.participant.Salience
        player.salient = Salience
        Exp_Con = player.participant.Exp_Con
        SwitchPayoffs = player.participant.SwitchPayoffs
        outcome_left = "Safe" if player.safeLeftBlock1 == True else "Risky"
        outcome_right = "Risky" if player.safeLeftBlock1 == True else "Safe"
        if Exp_Con == 1: # means risky emits in block 1 
            player.carbon_left = C.carbon if outcome_left == "Risky" else 0 
            player.carbon_right = C.carbon if outcome_right == "Risky" else 0
            player.riskyCarbon = True 
        if Exp_Con == 2: # means safe emits in block 1 
            player.carbon_left = C.carbon if outcome_left == "Safe" else 0 
            player.carbon_right = C.carbon if outcome_right == "Safe" else 0
            player.riskyCarbon = False
        player.riskyLeft = True if outcome_left == "Risky" else False 

        carbonMiles = C.carbon * 20.2/11

        return {
            'num_rounds': player.participant.game_rounds,
            'Salience' : "salient" if player.participant.Salience == True else "non_salient",
            'carbonA': player.carbon_left,
            'carbonB': player.carbon_right,
            'carbonMiles': carbonMiles, 
            'player.condition' : Exp_Con,
            'switchPayoffs' : SwitchPayoffs,
            'riskyLeft' : player.riskyLeft
            }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        attention_check_emissions(player, player.amountEmissionsLeft, player.amountEmissionsRight)
    


class Preview_Game2(Page):
    form_model = 'player'
    form_fields = ['preference']
    @staticmethod
    def vars_for_template(player: Player):
        Salience = player.participant.Salience
        player.salient = Salience
        Exp_Con = player.participant.Exp_Con
        SwitchPayoffs = player.participant.SwitchPayoffs

        carbonMiles = C.carbon * 20.2/11

        return {
            'num_rounds': player.participant.game_rounds,
            'Salience' : "salient" if player.participant.Salience == True else "non_salient",
            'carbonA': player.carbon_left,
            'carbonB': player.carbon_right,
            'carbonMiles': carbonMiles, 
            'player.condition' : Exp_Con,
            'switchPayoffs' : SwitchPayoffs,
            'riskyLeft' : player.riskyLeft
            }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        make_choice(player, player.preference)





class before_Games(Page):
    form_model = 'player'




    



page_sequence = [
    #Consent,
    #Intro_1,
    #Intro_2,
    #Intro_3,
    Preview_Game,
    Preview_Game2,
    before_Games
]
