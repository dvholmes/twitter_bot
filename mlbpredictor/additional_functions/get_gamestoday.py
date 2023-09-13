import requests
from bs4 import BeautifulSoup
import json


dict_teams = {
    "Rays" : "TBR",
    "D'backs" : "ARI",
    "Pirates" : "PIT",
    "Reds" : "CIN",
    "Blue Jays": "TOR",
    "Angels": "LAA",
    "Guardians": "CLE",
    "Astros": "HOU",
    "Tigers": "DET",
    "Phillies": "PHI",
    "Marlins": "MIA",
    "Orioles": "BAL",
    "Nationals": "WSN",
    "Yankees" : "NYY",
    "Red Sox": "BOS",
    "Cubs" : "CHC",
    "Mets" : "NYM", 
    "Royals": "KCR",
    "Twins": "MIN",
    "Brewers": "MIL",
    "Cardinals": "STL",
    "Athletics": "OAK",
    "Rangers" : "TEX",
    "Rockies": "COL",
    "White Sox": "CHW",
    "Padres" : "SDP",
    "Mariners" : "SEA",
    "Dodgers" : "LAD",
    "Braves" : "ATL",
    "Giants" : "SFG",
}

def get_todays_games():
    url = "https://www.baseball-reference.com/previews/"
    response = requests.get(url)
   
    html_content = response.content

    soup = BeautifulSoup(html_content, "html.parser")

    total_gamecards = soup.findAll(class_="game_summary nohover")

    # grab the total amount of game cards
    number_games = len(total_gamecards)
    all_games = []
    game_count = 1
    team_array = []

    #check if there are any games
    if number_games > 0:
        for game_cards in total_gamecards:
           
            game_object = {
                "Game Number": game_count,
                "Team 1": None,
                "Team 2": None,
                "Predicted  Winner": None
            }

           # loop through the tags and grab each of the team name
         
            row_elements = game_cards.find('tbody').findAll('tr')

            tracker = 0

            for row_tag in row_elements:

            

                teams_tag = row_tag.find('a')
                name = teams_tag.get_text()
                abbr = dict_teams[name]
                team_array.append(abbr)


                if tracker >0:
                    game_object["Team 2"] = abbr 
                else:
                    game_object["Team 1"] = abbr
                tracker +=1
               

            all_games.append(game_object)
            game_count += 1

    return team_array,number_games



