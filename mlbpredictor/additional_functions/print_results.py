def print_results(dataf):

    game = 0

    for index, row in dataf.iterrows():

        print(game, '=', row['Tm'], 'vs', row['Opp'])

        if row['predict_v2'] == 1:
            print("Winner: ",row['Tm'])
            
        else:
            print("Winner: ",row['Opp'])
        game += 1

 