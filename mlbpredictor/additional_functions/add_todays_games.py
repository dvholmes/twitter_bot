from bs4 import BeautifulSoup
import pandas as pd



def get_current_streaks(dataframe):

    grouped_dfs = dataframe.groupby('Tm')

    streak_dict = {}
    winning_dic = {}


    for team, team_data in grouped_dfs:
        last_game = team_data.tail(1)


        current_streak = last_game['Streak'].iloc[0]
        last_result = last_game['predict'].iloc[0]
      


        if last_result == 1 and current_streak > 0:
            current_streak += 1
        elif last_result == 1 and current_streak < 0:
            current_streak = -1
        elif last_result == 0 and current_streak > 0:
            current_streak  = -1
        elif last_result == 0 and current_streak < 0:
            current_streak -= 1

        streak_dict[last_game['Tm'].iloc[0]] = current_streak
        winning_dic[last_game['Tm'].iloc[0]]= last_game['W-L'].iloc[0]

    
    return streak_dict, winning_dic
        



def add_todays_games(number_games, teams_array, date_today, games,streak_dict, winning_dict):

    team_index = 0

    # add todays games to the data frame
    for i in range(0,number_games):

        print("Home",teams_array[team_index],"Away", teams_array[team_index+1])

   
        new_row = {"Date": date_today, "Streak" :streak_dict[teams_array[team_index]] ,
                "W-L":winning_dict[teams_array[team_index]], "Opp": teams_array[team_index+1],"Tm": teams_array[team_index]}


        games.loc[len(games.index)] = new_row
        team_index += 2
    
    # convert the opponent to a distinct decimal value.
    games["opp_number"] = games['Opp'].astype('category').cat.codes
   
    # convert string object to datetime object
    games['Date'] = pd.to_datetime(games['Date'], format='%Y-%m-%d')



    
    return games



