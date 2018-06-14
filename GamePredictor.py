##Predictor gives head to head game results based off of regular season point differential in a specific year
##Input parameters: team1 team2 season
##Year must be between 2003 and 2017 (inclusive)
##See team names list for valid team names. Put team names in " "

import pandas as pd
import sys

def main():
    if len(sys.argv) != 4:
        print("Incorrect number of parameters given")

    inputTeam1 = sys.argv[1]
    inputTeam2 = sys.argv[2]
    inputSeason = int(sys.argv[3])

    teamNames = pd.read_csv("DataFiles\\Teams.csv",sep=",")
    teamNames = pd.DataFrame(teamNames)

    inputTeamID1 = getTeamID(teamNames,inputTeam1,inputSeason)
    inputTeamID2 = getTeamID(teamNames, inputTeam2, inputSeason)

    regRaw = pd.read_csv("DataFiles\\RegularSeasonDetailedResults.csv",sep=",")
    ##Detailed results only from 2003 onward

    tourneyRaw = pd.read_csv("DataFiles\\NCAATourneyDetailedResults.csv",sep=",")
    tourneyRaw = pd.DataFrame(tourneyRaw)
    ##Excludes first play in games
    tourneyRaw = tourneyRaw[tourneyRaw['DayNum'].between(136, 154, inclusive=True)]

    seeds = pd.read_csv("DataFiles\\NCAATourneySeeds.csv",sep=",")
    seeds = pd.DataFrame(seeds)
    #seeds = seeds[seeds['Season'].between(2003, 2018, inclusive=True)]

    #Only considering March Madness participants
    regData = seeds[seeds['Season'].between(2003,2018,inclusive=True)]
    regData = pd.DataFrame(regData)
    seasons = regData['Season'].unique()

    regData.join(pd.DataFrame(columns=['Win','Loss','rPD']))

    ##Regular season data
    currentSeason = 0
    tempData = regRaw
    for row in regData.itertuples():
        if(currentSeason!=row.Season):
            tempData = regRaw[regRaw['Season']==row.Season]
            currentSeason=row.Season
        temp = allTeamGames(tempData, row.TeamID, currentSeason)
        numGames = len(temp.index)
        temp = temp[temp['WTeamID'] == row.TeamID]
        win = len(temp.index)
        loss = numGames - win
        regData.at[row.Index, 'Win'] = win
        regData.at[row.Index, 'Loss'] = loss
        regData.at[row.Index, 'rPD'] = pointDiff(tempData,row.TeamID,currentSeason)

    PD1 = regData[(regData['Season']==inputSeason) & (regData['TeamID']==inputTeamID1)].rPD.iloc[0]
    PD2 = regData[(regData['Season'] == inputSeason) & (regData['TeamID'] == inputTeamID2)].rPD.iloc[0]
    if PD1 >= PD2:
        print(inputTeam1 + " defeats " + inputTeam2 + " in " + str(inputSeason))
    else:
        print(inputTeam2 + " defeats " + inputTeam1 + " in " + str(inputSeason))


##Return detailed results of all games a team played in the regular season for the year
def allTeamGames(data,team,year):
    return data[(data['Season']==year) & ((data['WTeamID']==team) | (data['LTeamID']==team))]

#Overal season results. Assumes all data entries are from same season
def teamSeason(data,team,year):
    temp = allTeamGames(data,team,year)
    numGames = len(temp.index)
    temp = temp[temp['WTeamID']==team]
    win = len(temp.index)
    loss=numGames - win
    homeW = len(temp[temp['WLoc']=='H'])
    awayW = len(temp[temp['WLoc']=='A'])
    neutralW = win - homeW - awayW
    return [win,loss,homeW,awayW,neutralW]

##Return point differential for that team for a year
def pointDiff(data,team,year):
    data = allTeamGames(data,team,year)
    total = 0
    for row in data.itertuples():
        if(row.WTeamID==team):
            total+=row.WScore-row.LScore
        else:
            total+=row.LScore-row.WScore
    return total

def getTeamID(teamNames, team, year):
    if team not in teamNames.TeamName.unique():
        print(team + " not valid team name! Check spelling/formatting.")
        sys.exit(1)
    elif (year < 2003) | (year > 2017):
        print("Input year must be between 2003 and 2017 (inclusive)")
        sys.exit(1)
    entry = teamNames.iloc[teamNames.TeamName.tolist().index(team)]
    if int(entry.FirstD1Season) > year:
        print(team + " not D1 Team until " + entry.FirstD1Season)
        sys.exit(1)
    elif int(entry.LastD1Season) < year:
        print(team + " stopped being D1 Team in " + entry.LastD1Season)
        sys.exit(1)
    return entry.TeamID

main()