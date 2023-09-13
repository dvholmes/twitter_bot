def compute_rolling(new_cols, current_cols, teams):

    teams = teams.sort_values('Date')
    five_day_ave = teams[current_cols].rolling(5,closed ='left').mean()
    teams[new_cols] = five_day_ave


    if len(teams) == 31:
        # get the teams rank, from their most recent game.

        recent_rank = teams.iloc[len(teams)- 2]['Rank']
        teams.at[teams.index[len(teams) -1],'Rank'] = recent_rank

    elif len(teams) == 32:

        #accout  for double headers 
        recent_rank = teams.iloc[len(teams)- 3]['Rank']
        teams.at[teams.index[len(teams) -2],'Rank'] = recent_rank

        # save index to reassgin
        prev_index = teams.iloc[len(teams)-1][0]

        # set the double header games to the same values
        teams.iloc[len(teams)-1]= teams.iloc[len(teams)-2]
        teams.at[teams.index[len(teams) -1],0] = prev_index

    teams = teams.dropna(subset=new_cols)

    return teams


def create_roll_avg(games,new_cols,aver_cols):

    # group and compute the rolling averages for each team over teh last 5 games
    games_averages = games.groupby('Tm').apply(lambda x: compute_rolling(new_cols, aver_cols, x))
    games_averages= games_averages.droplevel('Tm')
    games_averages.index = range(games_averages.shape[0])
    return games_averages
