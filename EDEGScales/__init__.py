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
    NAME_IN_URL = 'EDEG_Scales'
    PLAYERS_PER_GROUP = None
    ROUNDS_PER_CONDITION = 1
    NUM_ROUNDS = 1
    STARTING_PAYMENT = 1
    PAYRATIO = 200 
    carbonA = 0

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

#PLAYER FUNCTION 
def make_field(label):
        return models.IntegerField(
            choices=[1,2,3,4,5],
            label=label,
            widget=widgets.RadioSelect,
            )


class Player(BasePlayer):
    gender = models.IntegerField(choices=[[1,'Male'], [2,'Female'],[3,'Diverse'], [4,'Other']])
    age = models.IntegerField(min=18, max=100, max_length=2)
    hh_income = models.IntegerField(choices=[[1,'up to 30k'], [2,'between 30k and 50k'],[3,'between 50k and 80k'], [4,'more than 80k'], [5, "prefer not to say"]])
    hh_party = models.IntegerField(choices=[[1, "Democratic Party"], [2, "Republican Party"], [3, "Other"]])
    hh_party_other = models.StringField(max_length=150, blank=True, label="Please specify")
    range_party = models.IntegerField( min=-100, max=100)
    conservative_liberal = models.IntegerField( widget=widgets.RadioSelect, choices=[-5, -4, -3, -2, -1, 0, 1, 2, 3, 4,5])
    ccc1 = make_field('We must protect the climate’s delicate equilibrium.') ## concern 4 items
    ccc2 = make_field('Climate protection is important for our future.')
    ccc3 = make_field('I worry about the climate’s state.')
    ccc4 = make_field('Climate change has severe consequences for humans and nature.')
    att_ccc = make_field('In this row, please mark the third circle (center circle) to indicate you are paying attention.')
    ccc10 = make_field('Climate change and its consequences are being exaggerated in the media.')     ### skepticism 6 items 
    ccc11 = make_field('Climate change is a racket.')
    ccc12 = make_field('As long as meteorologists are not even able to accurately forecast weather, climate cannot be reliably predicted either.')
    ccc13 = make_field('There are larger problems than climate protection.')
    ccc14 = make_field('I do not feel threatened by climate change.')
    ccc15 = make_field('The impacts of climate change are unpredictable; thus, my climate-friendly behavior is futile.')
    ccc16 = make_field('Climate protection needlessly impedes economic growth.')
    ind1 = make_field('The government interferes far too much in our everyday lives.')
    ind2 = make_field('I feel that people who are successful in business have a right to enjoy their wealth as they see fit.')
    ind3 = make_field('Too many people expect society to do things for them that they should be doing for themselves.')
    hie1 = make_field('Our society would be better off if the distribution of wealth was more equal.')
    hie2 = make_field('A lot of problems in our society come from the decline in the traditional family, where the man works and the woman stays home.')
    hie3 = make_field('Discrimination against minorities is still a very serious problem in our country.')
    trustCC = models.IntegerField(choices=[1,2,3,4,5,6,7,8],label='How much did you trust the carbon offsetting procedure in this study?',widget=widgets.RadioSelect )
    faithful = models.IntegerField(choices=[[1,'yes'], [0,'no']], label="Is there any reason why we should NOT use your data?")
    use_data = models.StringField(max_length=1000, blank=True, label="If we should NOT use your data, please specify why:")
    generalFeedback = models.StringField(max_length=3000, blank=True, label="Do you have any other comments or feedback on the study?")
    
    Block1CarbonLeft = models.IntegerField() 
    Block1CarbonRight = models.IntegerField() 
    Block2CarbonLeft = models.IntegerField() 
    Block2CarbonRight = models.IntegerField()
    memoryCarbon_block1 = models.BooleanField()
    memoryCarbon_block2 = models.BooleanField()
    memoryBonus = models.IntegerField() 
    
    # choiceAttention = models.StringField( choices=['correct', 'false'])  # , widget=widgets.RadioSelect)
    random_bonus = models.CurrencyField()


# FUNCTIONS
def memory_test_emissions(player: Player, block1Left, block1Right, block2Left, block2Right ):
    if(player.participant.Block1CarbonLeft == block1Left and player.participant.Block1CarbonRight == block1Right ):
        print("first if true")
        player.memoryCarbon_block1 = True
    else:
        print("first if false")
        player.memoryCarbon_block1 = False
    if(player.participant.Block2CarbonLeft == block2Left and player.participant.Block2CarbonRight == block2Right ):
        print("second if true")
        player.memoryCarbon_block2 = True
    else:
        print("second if false")
        player.memoryCarbon_block2 = False
    if (player.memoryCarbon_block1 == True and player.memoryCarbon_block2 == True): 
        print("third if true")
        player.memoryBonus = 20
    else:
        print("third if false")
        player.memoryBonus = 0 
    print(block1Left,block1Right,block2Left,block2Right, player.participant.Block1CarbonLeft, player.participant.Block1CarbonRight , player.participant.Block2CarbonLeft, player.participant.Block2CarbonRight )


# ---------------------------------------------------------------
# ------------------- PAGES--------------------------------------
#----------------------------------------------------------------

#class Main_A(Page):
#    form_model = 'player'
#    form_fields = ['choiceAttention']
    

class Memory_test(Page):
    form_model = 'player'
    form_fields = ['Block1CarbonLeft','Block1CarbonRight','Block2CarbonLeft','Block2CarbonRight']
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        memory_test_emissions(player, player.Block1CarbonLeft,  player.Block1CarbonRight, player.Block2CarbonLeft,player.Block2CarbonRight)



class Demographics(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'hh_income', "hh_party", "range_party", "hh_party_other"]

    
class CCConcern(Page):
    form_model = 'player'
    form_fields= ['ccc1', 'ccc2', 'ccc3', 'ccc4', 'att_ccc', 'ccc10', 'ccc11', 'ccc12', 'ccc13', 'ccc14', 'ccc15', 'ccc16'  ]

      
class Pol_Att(Page):
    form_model = 'player'
    form_fields= ['ind1', 'ind2', 'ind3', 'hie1','hie2', 'hie3' , "conservative_liberal" ]
    
""" class Conservative(Page):
    form_model = 'player'
    form_fields= [ "conservative_econ", "conservative_social" ] """

    
class Trust(Page):
    form_model = 'player'
    form_fields = [  "trustCC" , "faithful", "use_data", "generalFeedback"]


class End(Page):
    @staticmethod
    def vars_for_template(player: Player):
        chosen_round = player.participant.chosen_round
        chosen_round_outcome = player.participant.chosen_round_outcome
        chosen_round_choice = player.participant.chosen_round_choice  ### in our logic where a is always safe and b is always risky 
        chosen_round_carbon = player.participant.chosen_round_carbon

        Exp_Con = player.participant.Exp_Con
        player.participant.finished = True
        memoryPassed = True if player.memoryBonus > 0 else 0 
        player.memoryBonus

        player.random_bonus = cu(C.STARTING_PAYMENT + ( chosen_round_outcome + player.memoryBonus) / C.PAYRATIO )
        
        return {
            'chosen_round_outcome': chosen_round_outcome,
            #'starting_payment': C.STARTING_PAYMENT,
            #'payratio': C.PAYRATIO,
            'chosen_round': chosen_round,
            'chosen_round_choice_present': chosen_round_choice,
            'chosen_round_choice': chosen_round_choice,
            'Exp_Con': Exp_Con,
            'player.payoff': player.payoff,
            'random_bonus': player.random_bonus,
            'chosen_round_carbon': chosen_round_carbon, 
            'safeLeftBlock1': player.participant.safeLeftBlock1,

            'memoryPassed': memoryPassed,
            'memoryBonus': player.memoryBonus
            #'PoliticalGroup': player.session.config['group']
            
        }

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS


class betweenGames(Page):
    form_model = 'player'


page_sequence = [
    betweenGames,
    Memory_test,
    #Main_A,
    Demographics,
    CCConcern,
    Pol_Att,
    ####Conservative,
    Trust,
    End
]
