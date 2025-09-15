import pickle
import datetime
import requests
import pandas as pd
import dataframe_image as dfi

def main():
    #Load id_to_customID_dict from pickle file
    with open("id_to_customID_dict.pkl", "rb") as ff:
        id_to_customID_dict = pickle.load(ff)

    #Load id_to_draft_dict from pickle file
    with open("id_to_draft_dict.pkl", "rb") as ff:
        id_to_draft_dict = pickle.load(ff)

    # Get the current year and hit MLB StatsAPI to get current team records
    year = datetime.datetime.now().year
    url = f"https://statsapi.mlb.com/api/v1/standings?leagueId=103,104&season={year}&standingsTypes=regularSeason"
    response = requests.get(url)
    data = response.json().get('records')

    #list that will hold data for DataFrame
    df_data = []

    #for each division
    for division in data:
        #for each division
        for team in division['teamRecords']:
            #get MLB ID, Name, Wins, Losses, Winning Percentage, and whether they are a division leader
            api_data = {
                'id': team['team']['id'],
                'name': team['team']['name'],
                'wins': int(team['leagueRecord']['wins']),
                'losses': int(team['leagueRecord']['losses']),
                'pct': float(team['leagueRecord']['pct']),
                'divisionLeader': int(team['divisionLeader']),
                'hasWildcard': 0 #this value is updated below
            }
    
            #if team is not leading division and they have positive WildCard GamesBack, update this value
            if not team['divisionLeader'] and not team['wildCardGamesBack'][0].isdigit():
                api_data['hasWildcard']=1
            #calculate expected wins with current winning percentage
            api_data['exp_wins'] = round(api_data['pct']*162)
            #get custom_id_data_dict and draft_data values from dictionaries
            custom_id_data = id_to_customID_dict[api_data['id']]
            draft_data = id_to_draft_dict[custom_id_data[0]]
            draft_data[0] = round(draft_data[0], 1)

            #adjust wins over projection if team's current pace is better than expected wins
            wins_over_proj = 0
            if api_data['exp_wins'] > draft_data[0]:
                wins_over_proj = api_data['exp_wins'] - draft_data[0]

            #format data into list for dataframe
            current_row = [api_data['name'], custom_id_data[1], draft_data[1], api_data['wins'],
                           api_data['losses'], api_data['pct'], api_data['divisionLeader'],
                           api_data['hasWildcard'], api_data['exp_wins'], draft_data[0], wins_over_proj]
            
            #add data to df_data list
            df_data.append(current_row)

    #create DataFrame with df_data and appropriate columns
    df = pd.DataFrame(data=df_data, columns=['Team', 'Division', 'Owner', 'Wins',
                                             'Losses', 'Pct', 'DivisionLeader', 'WildCardTeam',
                                             'ExpectedWins', 'ProjectedWins', 'OverProjection'])

    #style DataFrame to hide row numbers and round columns appropriately
    styled = (
    df.style
        .hide(axis="index")                 # hide row numbers
        .format({"Pct": "{:.3f}", "ProjectedWins": "{:.1f}", "OverProjection": "{:.1f}"})  # round with formatting
    )
   
    #export Standings DataFrame as image
    dfi.export(styled, "standings.png")

    #Wins Over Projection Totals
    print("Wins Over Projections")
    #Group By Owner and sum OverProjection
    grouped = df.groupby("Owner")["OverProjection"].sum()
    #print sorted Owner & OverProjection with proper formatting
    print(grouped.sort_values(ascending=False).to_string(index=True, header=False, name=False))

    #Division Leaders counts
    print("Division Leaders")
    #Group By Owner and sum DivisionLeader
    grouped = df.groupby("Owner")["DivisionLeader"].sum()
    #print sorted Owner & Division Leaders with proper formatting 
    print(grouped.sort_values(ascending=False).to_string(index=True, header=False, name=False))

    #Wildcard Team counts
    print("Wild Card Teams")
    #Group By Owner and sum Wild Card Teams
    grouped = df.groupby("Owner")["WildCardTeam"].sum()
    #print sorted Owner & Wild Card Teams with proper formatting
    print(grouped.sort_values(ascending=False).to_string(index=True, header=False, name=False))

if __name__ == "__main__":
    main()