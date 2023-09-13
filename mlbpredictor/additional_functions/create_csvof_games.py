from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
import os



def create_csvof_games(list_teams,months,curr_year):
    current_dir = os.path.dirname(__file__)
     
    count = 30
    stats = []
    p_stats = []
    wait_counter = 0

    

    # loop through each team in the list
    for team in list_teams:
        print(team)
        
      
        
        # make request for both pitching and batting stats
        res = requests.get(f'https://www.baseball-reference.com/teams/tgl.cgi?team={team}&t=b&year={curr_year}')
        print(res.status_code)
        res2 = requests.get(f'https://www.baseball-reference.com/teams/tgl.cgi?team={team}&t=p&year={curr_year}')
        print(res.status_code)

        #locate and scrape the first table containing the games stats for batting and pitching
        batting_df = pd.read_html(res.text, match="Team Batting Gamelog")[0]
        pitching_df = pd.read_html(res2.text, match="Team Pitching Gamelog")[0]
        
        # select the last 20 games/colums from the batting dat frame
        temp_df = batting_df.tail(count)
        value = temp_df.index[temp_df['Gtm'].isin(months)].tolist()
        dividers = len(value)

        # check if there is a month seperator in the dateframe
        if dividers == 0:
            # if not, then again select last 20 rows from both the  pitching and batting dataframe
            batting_df = batting_df.tail(count)
            pitching_df = pitching_df.tail(count)

        else:
            # if there is, grab the last 20 rows from each dataframe and remove the divder to make it 15 games.
            # batting dataframe
            batting_df = batting_df.tail(count + 1)
            batting_df = batting_df.reset_index()
            ind = batting_df.index[batting_df['Gtm'].isin(months)].tolist()
            batting_df = batting_df.drop(batting_df.index[ind])

            # pitching dataframe
            pitching_df = pitching_df.tail(count + 1)
            pitching_df = pitching_df.reset_index()
            spot = pitching_df.index[pitching_df['Gtm'].isin(months)].tolist()
            pitching_df = pitching_df.drop(pitching_df.index[spot])


        # reset the batting dataframe's index and select the important columns
        batting_df = batting_df.reset_index()
        batting_df['Team'] = team
        batting_df = batting_df[['BA','OBP','OPS','H']]
        batting_df = batting_df.rename(columns={"H": "Team_Hits",})
        
        # reset the pitching dataframe's index and select the important columns
        pitching_df = pitching_df.reset_index()
        pitching_df = pitching_df[['H','HR','ERA']]
        pitching_df = pitching_df.rename(columns={"H": "Hits_allowed", "HR":"HR_allowed"})

        # combine pitching and batting stats for each teams, from the last 10 games
        all_teamstats = batting_df.join(pitching_df)

        team_url = f"https://www.baseball-reference.com/teams/{team}/{curr_year}-schedule-scores.shtml"
        team_res = requests.get(team_url)

        team_schedule = pd.read_html(team_res.text, match="Team Game-by-Game Schedule")[0]
      
        filtered_schedule = team_schedule[team_schedule.iloc[:, 2] == "boxscore"]

        last_games = filtered_schedule.tail(30)
       
        last_games = last_games.reset_index()

        last_games = last_games.join(all_teamstats)

        stats.append(last_games)
            
            
        time.sleep(15)
    
    allgame_stats = pd.concat(stats)
    cleangames_path = os.path.join(current_dir, "csvgames.csv")
    allgame_stats.to_csv(cleangames_path, index = 'False')

    





