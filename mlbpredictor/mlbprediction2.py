from bs4 import BeautifulSoup
import pandas as pd
import html5lib
import requests
import time
import os

import numpy as np
from datetime import date,datetime
from .additional_functions.get_gamestoday import get_todays_games
from .additional_functions.create_csvof_games import create_csvof_games
from .additional_functions.clean_data import part1_cleandataframe, call_set_steak
from .additional_functions.add_todays_games import add_todays_games, get_current_streaks
from .additional_functions.rolling_coverter import create_roll_avg
from .additional_functions.split_train import split_train
from .additional_functions.print_results import print_results
from .additional_functions.games_of_day import select_game


# retreive today's date using the imported library

list_teams = [
    "TBR",
     "ARI",
     "PIT",
    "CIN",
    "TOR",
    "LAA",
    "CLE",
    "HOU",
    "DET",
    "PHI",
    "MIA",
    "BAL",
     "WSN",
    "NYY",
    "BOS",
    "CHC",
    "NYM", 
    "KCR",
    "MIN",
    "MIL",
    "STL",
    "OAK",
    "TEX",
    "COL",
    "CHW",
    "SDP",
    "SEA",
    "LAD",
    "ATL",
     "SFG",
]

# if there are games today, make predictions

def getMLBYear():
    # Get the current date
    current_date = datetime.now()

    # Check if the current month is May (or later)
    if current_date.month >= 5:  # May is represented as month 5
        return current_date.year
    else:
        # If it's not May or later, subtract 1 from the current year
        return current_date.year - 1

    # Now you have the appropriate year based on the condition
   

def mlbpredict():
    
    
    current_dir = os.path.dirname(__file__)
    
    date_today = date.today()
    date_today = str(date_today)

    # grab the number of games 
    teams_array ,number_games = get_todays_games()
    print(teams_array, number_games)
    
    #get the year to webscrape from.
    scrape_year = getMLBYear()
   

    if number_games > 0:

        # read the contents from date.txt
        
        data_read_path = os.path.join(current_dir, 'data_read.txt')
        file = open(data_read_path, 'r+')

        
        var = file.readline()
        #mlb months seasons 
        months = ['Jun', 'Jul', 'May','Aug','September','September/October']

        # if the file already has today's date, then the date has already been scraped and saved in a csv file
        if var != date_today:
            # if not, then write todays date to the file, and begin websraping data
            print("Data has not been retrived today. Begin scraping")
            file.seek(0)                        
            file.truncate()
            file.write(date_today)

            #call function to webscrape, and save it to a csvfile
            create_csvof_games(list_teams,months,scrape_year)
        
        # read in the date from the csv file.
        csvgames_path = os.path.join(current_dir,'csvgames.csv')
        
        games = pd.read_csv(csvgames_path, index_col=0)
       

        # clean part of the dataframe before combining todays game
        games = part1_cleandataframe(games)
        games = call_set_steak(games)

        cleangames_path = os.path.join(current_dir, "cleaned_games.csv")
        games.to_csv(cleangames_path, index = 'False')

        # add todays games to the dataframe and convert categorical to numerical data
        
        data_frame = pd.read_csv(cleangames_path, index_col=0)
        streak_hash, winning_dic = get_current_streaks(data_frame)
        games = add_todays_games(number_games,teams_array,date_today,data_frame,streak_hash,winning_dic)


        # columns that will turned into rolling averages
        aver_cols = ['RA','R','BA','OBP','OPS','Team_Hits','Hits_allowed','ERA','cLI']
        new_cols = [f"{c}_ave" for c in aver_cols]

       # add rolling averages to the dataframe.
        games_averages = create_roll_avg(games, new_cols, aver_cols)
        # games_averages.to_csv("rolling_games.csv", index = 'False')
        results_df = split_train(games_averages,date_today,new_cols)

        Team1, Team2, Winner = select_game(results_df,number_games)


        return Team1, Team2, Winner
    
    # Return False if there arent any games to predict
    else:
        return None,None,None


