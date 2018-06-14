import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import sklearn
import sys


teamName = pd.read_csv("/Users/yibowang/Downloads/DataFiles/Teams.csv")

teamData = pd.DataFrame(teamName) #stores into a data frame

#print(teamData) #prints Teams.csv file

tourneyResults= pd.read_csv("/Users/yibowang/Downloads/DataFiles/RegularSeasonCompactResults.csv")

tourneyData = pd.DataFrame(tourneyResults) #stores into a data frame

tourneyData = tourneyData[tourneyData.Season == 2017]

#print ('shape', tourneyData.shape)

#print(tourneyData) #prints NCAATourneyCompactResults.csv

results = pd.read_csv("/Users/yibowang/Downloads/DataFiles/NCAATourneySeeds.csv")

resultsData = pd.DataFrame(results) #stores into a data frame

#print(resultsData) #prints NCAATourneySeeds.csv file

resultsData = resultsData[resultsData.Season == 2017] #gets only data for 2017

#print(resultsData)  #prints NCAATourneySeeds.csv file for only teams in the 2017 Season

seedTeamID = resultsData.drop("Season", axis = 1)

seedTeamID['TeamWins'] = 0
seedTeamID['TeamLoses'] = 0
seedTeamID['WinRatio'] = 0
seedTeamID['Region'] = 0
seedTeamID['Rounds'] = 0
seedTeamID['HomeWins'] = 0
seedTeamID['VisitWins'] = 0
seedTeamID['NeutralWins'] = 0

##########################################################
# For Team Wins Column
##########################################################

win = 0;
row = 2082

for TeamID in seedTeamID.TeamID:
    for winTeam in tourneyData.WTeamID:
        if TeamID == winTeam:
            win = win + 1
    seedTeamID.loc[row, 'TeamWins'] = win
    win = 0
    row = row + 1

lose = 0
row = 2082

##########################################################
# For Team Loses Column
##########################################################

for TeamID in seedTeamID.TeamID:
    for loseTeam in tourneyData.LTeamID:
        if TeamID == loseTeam:
            lose = lose + 1
    seedTeamID.loc[row, 'TeamLoses'] = lose
    lose = 0
    row = row + 1



##########################################################
# For Win Ratio Column
##########################################################

sum = 0
winRatio = 0
row = 2082

for teamWins in seedTeamID.TeamWins:
    sum = teamWins + seedTeamID.loc[row, 'TeamLoses']
    winRatio = (teamWins/sum) * 100
    seedTeamID.loc[row, 'WinRatio'] = winRatio
    sum = 0
    winRatio = 0
    row = row + 1


##########################################################
# For Team Region Column
##########################################################

row = 2082
for seed in seedTeamID.Seed:
    string = seed[0]
    seedTeamID.loc[row, 'Region'] = string
    row = row + 1


#Returns dataframe with all team games for specified year. Data is dataframe from Results.csv data file
def allTeamGamesY(data,team):
    data = data[(data['WTeamID'] == team) | (data['LTeamID'] == team)]
    return data

##########################################################
# For Home Wins Column
##########################################################
row = 2082
count = 0

for teamID in seedTeamID.TeamID:

    homedata = allTeamGamesY(tourneyData, teamID)
    size = homedata.shape[0]

    for winteamID in homedata.WTeamID:
        for character in homedata.WLoc:
            if teamID == winteamID and character == 'H':
                count = count + 1

    homeratio = count/size
    seedTeamID.loc[row, 'HomeWins'] = homeratio
    row = row + 1
    count = 0

row = 2082
count = 0


##########################################################
# For Neutral Wins Column
##########################################################
for teamID in seedTeamID.TeamID:

    homedata = allTeamGamesY(tourneyData, teamID)
    size = homedata.shape[0]

    for winteamID in homedata.WTeamID:
        for character in homedata.WLoc:
            if teamID == winteamID and character == 'N':
                count = count + 1

    neutralRatio = count/size
    seedTeamID.loc[row, 'NeutralWins'] = neutralRatio
    row = row + 1
    count = 0

##########################################################
# For Visiting Wins Column
##########################################################

row = 2082
count = 0

for teamID in seedTeamID.TeamID:

    homedata = allTeamGamesY(tourneyData, teamID)
    size = homedata.shape[0]

    for winteamID in homedata.WTeamID:
        for character in homedata.WLoc:
            if teamID == winteamID and character == 'A':
                count = count + 1

    visitRatio = count/size
    seedTeamID.loc[row, 'VisitWins'] = visitRatio
    row = row + 1
    count = 0



print(tourneyData)
print(seedTeamID)

##########################################################
# For Linear Regression
##########################################################
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

lm = LinearRegression()
lm.fit(seedTeamID.TeamWins.values.reshape(-1,1), seedTeamID.HomeWins)
prediction = lm.predict(seedTeamID.TeamWins.values.reshape(-1,1))

# The coefficients
print('Coefficients: \n', lm.coef_)

# The mean squared error
print("Mean squared error: %.2f"
      % mean_squared_error(seedTeamID.TeamWins, prediction))

# Explained variance score: 1 is perfect prediction
print('Variance score: %.2f' % r2_score(seedTeamID.TeamWins, prediction))

plt.scatter(seedTeamID.TeamWins, seedTeamID.HomeWins)
plt.plot(seedTeamID.TeamWins, prediction, color = 'blue', linewidth = 3)
plt.xlabel("TeamWins")
plt.ylabel("HomeWins")
plt.title("TeamWins vs HomeWins")
plt.show()
