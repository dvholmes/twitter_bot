
from bs4 import BeautifulSoup
import pandas as pd

month_dict = {

    "Apr" : '4',
    "May": '5',
    "Jun": '6',
     "Jul" : '7',
     "Aug": '8',
     "Sep": '9',
     "Oct": '10',
     "Nov": '11'

}


def part1_cleandataframe(games):

    # reset dataframes indexs and drop some unwanted columns
    games = games.reset_index()
    games = games.drop(['Attendance','Win','Inn','Loss','Time','Orig. Scheduled','Gm#'], axis= 1)

    #convert the result to a number
    games['predict'] = (games['W/L'] == "W").astype(int)

    # iterate through each row in the dataframe, and convert the streaks and results to numerice values
    for index, row in games.iterrows():

        record = row['W-L'].split('-')

        # convert 'record' string to a winning percentage by computing, wins/total_games. 
        winning_percentage = round((int(record[0]) / (int(record[0]) + int(record[1]))) * 1000) / 1000

        g_streak = row['Streak']

        # convert 'streaks' to integer values.Ex '+++' -> 3 (wins)
        streak_len = len(g_streak)

        # if the string has dashes then convert it to a losing streak negative number.
        if g_streak[0] == '-':
            streak_len *= -1

        games.at[index,'W-L'] = winning_percentage
        games.at[index,'Streak'] = streak_len



        #-------------------------------------------

        # convert to proper date.

        current_date = row['Date'].split(' ')
        month = month_dict[current_date[1]]
        day = current_date[2]
        actual_date ='2023-'+  month + '-' + day 
        games.at[index,'Date'] = actual_date


    return games




# section 4: Set the proper game streak, using the previous games streak.

def set_streak(team):
    # iterate through the each row in the column
    team.index = range(team.shape[0])

    def_len = len(team.index) - 1
    for i in range(def_len,0,-1):
        team.at[i,'Streak'] = team.iloc[i-1]['Streak']
    return team

def call_set_steak(games_df):
    new_games_df = games_df.groupby('Tm').apply(lambda x: set_streak(x))
    new_games_df= new_games_df.droplevel('Tm')
    new_games_df.index = range(new_games_df.shape[0])
    return new_games_df



