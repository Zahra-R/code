from random import random, seed, choice as random_choice, randint
from otree.api import *
import numpy as np
# import scipy.stats as stats



author = 'Zahra Rahmani'
doc = """
Description Experience Gap with Carbon Externalities
"""


# def truncnorm(lower, upper, mean, std):
#     return stats.truncnorm((lower - mean) / std, (upper - mean) / std, loc=mean, scale=std).rvs()

class C(BaseConstants):
    NAME_IN_URL = 'EDEG'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 40
    ROUNDS_PER_BLOCK = NUM_ROUNDS/2
    STARTING_PAYMENT = 1
    PAYRATIO = 200
    MINIMUM_PAYMENT = 0
    MAXIMUM_PAYMENT = 1.10
    safe_outcome = 7
    high_lottery = 30 # typical outcome of the lottery
    low_lottery = -200 # rare disaster 
    carbon = 15
    show_feedback = 1

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

#PLAYER FUNCTION 

class Player(BasePlayer):
    choice = models.StringField( choices=[ 'A', 'B'])  # , widget=widgets.RadioSelect)
    real_choice = models.StringField()
    #outcomeA = models.FloatField()
    #outcomeB = models.FloatField()
    round_carbon = models.FloatField()
    round_outcome = models.FloatField()  # This is the outcome of the selected button in each round
    riskyLeft = models.BooleanField()
    riskyCarbon = models.BooleanField()
    carbonLeft = models.BooleanField()
    salient = models.BooleanField()
    block = models.IntegerField()
    switchPayoff = models.BooleanField()
    condition = models.IntegerField()
    leftEmissionsCorrect = models.BooleanField()
    rightEmissionsCorrect = models.BooleanField()
    att_check_amountEmissionsLeft = models.IntegerField()
    att_check_amountEmissionsRight = models.IntegerField()
    preference = models.StringField( choices=[ 'A', 'B'])  # , widget=widgets.RadioSelect)
    real_preference = models.StringField()
    preference_carbon = models.IntegerField()

    outcomeSafe = models.FloatField()
    outcomeRisky = models.FloatField()

    ## this is only for internal reasons (to give feedback, can be deleted for analysis)
    carbon_left = models.IntegerField()
    carbon_right = models.IntegerField()

# FUNCTIONS
def creating_session(subsession: Subsession):
    for player in subsession.get_players():
        if subsession.round_number == 1:
            player.participant.game_rounds = C.NUM_ROUNDS


def output_outcome(player: Player):
    #tax = player.tax
    outcomeA = C.safe_outcome
    rnd = random()
    if rnd < 0.90:
        outcomeB = C.high_lottery
    else:
        outcomeB = C.low_lottery
    return outcomeA, outcomeB


### Internally (in database) A is always safe and B is always risky
## In reverse Condition A is the risky option and B is the safe option, therefore, we recode this here in the function
## Condition 1 first block: safe is carbon neutral, risky is carbon negative; second block: safe is carbon negative, risky is carbon neutral
## Condition 2: block order is reversed
def make_choice(player: Player, choiceMade):
    if choiceMade == 'A':
        player.real_choice = "Safe" if player.riskyLeft == False else "Risky"
    if choiceMade == 'B': 
        player.real_choice = "Safe" if player.riskyLeft == True else "Risky"

    player.outcomeSafe, player.outcomeRisky = output_outcome(player)
    player.round_outcome = player.outcomeSafe if player.real_choice == "Safe" else player.outcomeRisky 
    if player.real_choice == "Safe":
        player.round_carbon = C.carbon if player.riskyCarbon == False else 0
    if player.real_choice == "Risky":
        player.round_carbon = C.carbon if player.riskyCarbon == True else 0



def make_preference(player: Player, choiceMade):
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


def determine_outcome(player:Player, chosen_round):
    player.participant.chosen_round_outcome = player.in_round(chosen_round).round_outcome
    player.participant.chosen_round_choice = player.in_round(chosen_round).choice
    #player.payoff = player.chosen_round_outcome / C.PAYRATIO
    
    player.participant.payoff_decimal = 1 + player.participant.chosen_round_outcome/ C.PAYRATIO 
    participant = player.participant
    participant.chosen_round = chosen_round
    player.participant.chosen_round_carbon = player.in_round(chosen_round).round_carbon
    ## now for the CarbonMemoryCheck
    # left carbon = 30 wenn risky left und riskyCarbon ist. wenn risky left und not risky carbon, dann ist carbon right
    # wenn not risky left und riskyCarbon, dann ist carbon right und wenn not risky left und not riskycarbon dann ist carbon left 
    player.participant.Block2CarbonLeft = player.carbon_left
    player.participant.Block2CarbonRight = player.carbon_right
    player.participant.Block1CarbonLeft = player.in_round(1).carbon_left
    player.participant.Block1CarbonRight = player.in_round(1).carbon_right
    

# ---------------------------------------------------------------
# ------------------- PAGES--------------------------------------
#----------------------------------------------------------------

class Main(Page):
    form_model = 'player'
    form_fields = ['choice']
    @staticmethod
    def vars_for_template(player: Player):
        Salience = player.participant.Salience
        player.salient = Salience
        Exp_Con = player.participant.Exp_Con
        SwitchPayoffs = player.participant.SwitchPayoffs
        block = 1 if  player.round_number <= C.ROUNDS_PER_BLOCK else 2
        safeLeftBlock1 = player.participant.safeLeftBlock1

        player.block = block
        player.condition = Exp_Con
        player.switchPayoff = SwitchPayoffs

        if block == 1: 
            outcome_left = "Safe" if safeLeftBlock1 == True else "Risky"
            outcome_right = "Risky" if safeLeftBlock1 == True else "Safe"
            if Exp_Con == 1: # means risky emits in block 1 
                player.carbon_left = C.carbon if outcome_left == "Risky" else 0 
                player.carbon_right = C.carbon if outcome_right == "Risky" else 0
                player.riskyCarbon = True 
            if Exp_Con == 2: # means safe emits in block 1 
                player.carbon_left = C.carbon if outcome_left == "Safe" else 0 
                player.carbon_right = C.carbon if outcome_right == "Safe" else 0
                player.riskyCarbon = False

        if block == 2: 
            outcome_left = "Risky" if SwitchPayoffs == safeLeftBlock1 else "Safe"
            outcome_right = "Safe" if SwitchPayoffs == safeLeftBlock1 else "Risky"
            if Exp_Con == 1: # means safe emits in block 2
                player.carbon_left = C.carbon if outcome_left == "Safe" else 0 
                player.carbon_right = C.carbon if outcome_right == "Safe" else 0
                player.riskyCarbon = False
            if Exp_Con == 2: # means risky emits in block 2
                player.carbon_left = C.carbon if outcome_left == "Risky" else 0 
                player.carbon_right = C.carbon if outcome_right == "Risky" else 0
                player.riskyCarbon = True

        player.riskyLeft = True if outcome_left == "Risky" else False  
        player.carbonLeft = True if player.carbon_left > 0 else False

        carbonMiles = C.carbon * 20.2/11
        game_round = player.round_number
        return {
                'firstRoundSecondBlock': int(C.ROUNDS_PER_BLOCK + 1 ),
                'game_round': game_round,
                'carbonA': player.carbon_left,
                'carbonB': player.carbon_right,
                'carbonMiles': round(carbonMiles), 
                'Salience' : Salience,
                'player.condition' : Exp_Con,
                'switchPayoffs' : SwitchPayoffs,
                'riskyLeft' : player.riskyLeft
            }
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        make_choice(player, player.choice)

class Feedback(Page):
    form_model = 'player'
    
    @staticmethod
    def is_displayed(player: Player):
        return 1 #(player.round_number >= C.show_feedback and player.participant.safeLeftBlock1== False)

    @staticmethod
    def vars_for_template(player: Player):
            Salience = player.participant.Salience
            previous_choice = player.choice
            choice_outcome = player.round_outcome
            real_choice = player.real_choice
            previous_outcomeForgone =  player.outcomeSafe if real_choice == "Risky" else player.outcomeRisky
            choice_emissions = player.round_carbon
            forgone_emissions = C.carbon if choice_emissions == 0 else 0

            previous_outcomeA = choice_outcome if previous_choice == 'A' else previous_outcomeForgone
            previous_outcomeB = choice_outcome if previous_choice == 'B' else previous_outcomeForgone
            carbonA = player.carbon_left
            carbonB = player.carbon_right
            return {
                'previous_choice': previous_choice,
                'real_choice': real_choice,
                'previous_outcome': choice_outcome,
                'previous_outcomeForgone' : previous_outcomeForgone,
                'previous_outcomeA': previous_outcomeA,
                'previous_outcomeB': previous_outcomeB,
                'Salience': Salience,
                'game_round': player.round_number,
                'choice_emissions': choice_emissions, 
                'forgone_emissions': forgone_emissions,
                'carbonB' : carbonB, 
                'carbonA' : carbonA
            }
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if (player.round_number == C.NUM_ROUNDS):
            chosen_round = randint(1,C.NUM_ROUNDS)
            determine_outcome(player,chosen_round)
            print('the chosen round is', chosen_round)
  
class betweenGames(Page):

    @staticmethod
    def is_displayed(player: Player):
        return (
            player.round_number == (C.ROUNDS_PER_BLOCK + 1)
        )

class Preview_Part2(Page):
    form_model = 'player'
    form_fields = ['att_check_amountEmissionsLeft', 'att_check_amountEmissionsRight']

    @staticmethod
    def vars_for_template(player: Player):
        Salience = player.participant.Salience
        player.salient = Salience
        Exp_Con = player.participant.Exp_Con
        SwitchPayoffs = player.participant.SwitchPayoffs
        safeLeftBlock1 = player.participant.safeLeftBlock1
        outcome_left = "Risky" if SwitchPayoffs == safeLeftBlock1 else "Safe"
        outcome_right = "Safe" if SwitchPayoffs == safeLeftBlock1 else "Risky"
        if Exp_Con == 1: # means safe emits in block 2
            player.carbon_left = C.carbon if outcome_left == "Safe" else 0 
            player.carbon_right = C.carbon if outcome_right == "Safe" else 0
            player.riskyCarbon = False
        if Exp_Con == 2: # means risky emits in block 2
            player.carbon_left = C.carbon if outcome_left == "Risky" else 0 
            player.carbon_right = C.carbon if outcome_right == "Risky" else 0
            player.riskyCarbon = True

        player.riskyLeft = True if outcome_left == "Risky" else False  
        player.carbonLeft = True if player.carbon_left > 0 else False

        carbonMiles = C.carbon * 20.2/11

        return {
            'num_rounds': player.participant.game_rounds,
            'Salience' : "salient" if player.participant.Salience == True else "non_salient",
            'carbonA': player.carbon_left,
            'carbonB': player.carbon_right,
            'carbonMiles': round(carbonMiles), 
            'player.condition' : Exp_Con,
            'switchPayoffs' : SwitchPayoffs,
            'riskyLeft' : player.riskyLeft
            }
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        attention_check_emissions(player, player.att_check_amountEmissionsLeft, player.att_check_amountEmissionsRight)
    @staticmethod
    def is_displayed(player: Player):
        return (player.round_number == (C.ROUNDS_PER_BLOCK + 1 ))
    

class Preview2_Part2(Page):
    form_model = 'player'
    form_fields = ['preference']

    @staticmethod
    def vars_for_template(player: Player):
        Salience = player.participant.Salience
        player.salient = Salience
        Exp_Con = player.participant.Exp_Con
        SwitchPayoffs = player.participant.SwitchPayoffs
        safeLeftBlock1 = player.participant.safeLeftBlock1
        outcome_left = "Risky" if SwitchPayoffs == safeLeftBlock1 else "Safe"
        outcome_right = "Safe" if SwitchPayoffs == safeLeftBlock1 else "Risky"
        if Exp_Con == 1:  # means safe emits in block 2
            player.carbon_left = C.carbon if outcome_left == "Safe" else 0
            player.carbon_right = C.carbon if outcome_right == "Safe" else 0
            player.riskyCarbon = False
        if Exp_Con == 2:  # means risky emits in block 2
            player.carbon_left = C.carbon if outcome_left == "Risky" else 0
            player.carbon_right = C.carbon if outcome_right == "Risky" else 0
            player.riskyCarbon = True

        player.riskyLeft = True if outcome_left == "Risky" else False
        player.carbonLeft = True if player.carbon_left > 0 else False

        carbonMiles = C.carbon * 20.2/11

        return {
            'num_rounds': player.participant.game_rounds,
            'Salience': "salient" if player.participant.Salience == True else "non_salient",
            'carbonA': player.carbon_left,
            'carbonB': player.carbon_right,
            'carbonMiles': round(carbonMiles),
            'player.condition': Exp_Con,
            'switchPayoffs': SwitchPayoffs,
            'riskyLeft': player.riskyLeft
        }

    @staticmethod
    def is_displayed(player: Player):
        return (player.round_number == (C.ROUNDS_PER_BLOCK + 1))

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        make_preference(player, player.preference)
    

page_sequence = [
    betweenGames,
    Preview_Part2,
    Preview2_Part2,
    Main,
    Feedback
]
