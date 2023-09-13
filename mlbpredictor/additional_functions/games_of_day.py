import random

def select_game(dataFrame, number_games):

    game_index = random.randint(0,number_games)

    Team_one = dataFrame['Tm'].iloc[game_index]
    Team_two = dataFrame['Opp'].iloc[game_index]

    winner = 0

    if dataFrame['predict_v2'].iloc[game_index] == 1:
        winner = Team_one
    else:
        winner = Team_two

    return Team_one, Team_two,winner


