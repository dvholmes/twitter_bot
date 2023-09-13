
from bs4 import BeautifulSoup
import pandas as pd
import html5lib
import requests
import time
from sklearn.ensemble import RandomForestClassifier
def split_train(games_averages,date_today,new_cols):

    v1_features = ['opp_number', 'Rank','W-L']
    v2_feat = ['opp_number', 'Rank','Streak','W-L']

    # combine the lists
    for c in new_cols:
        v1_features.append(c)

    # split the data into a training set and testing set.
    train_set = games_averages[games_averages['Date'] != date_today]
    games_today = games_averages[games_averages['Date'] == date_today]

    # train the randomforest models

    # version without game streaks
    rforest_object = RandomForestClassifier(n_estimators= 200, min_samples_split=40,random_state=1)
    rforest_object.fit(train_set[v1_features],train_set['predict'])
    games_outcomes = rforest_object.predict(games_today[v1_features])
    print("train")

    # version with streaks
    v2_forest = RandomForestClassifier(n_estimators= 200, min_samples_split=40,random_state=1)
    v2_forest.fit(train_set[v2_feat],train_set['predict'])
    version2 = v2_forest.predict(games_today[v2_feat])

    # add those to the dataframes
    games_today = pd.DataFrame(games_today)
    games_today = games_today.rename(columns={"HR_allowed": "predict_v2", "predict": "predict_v1" })
    games_today['predict_v1'] = games_outcomes.tolist()
    games_today['predict_v2'] = version2.tolist()


    games_today = games_today.drop(['BA','OBP','OPS','Team_Hits','Hits_allowed','ERA','W/L','RA','R','cLI'], axis=1)

    return games_today
