import requests
import pandas as pd
year = 2022
league_id=55646
year=2017
swid = '{8F5C0C75-0EC6-4CD4-9C0C-750EC64CD455}'
espn_s2 = 'AEBvIL4Dlefi3KlVW0JH87iCDbcx0707HaHAXb8P3MgYzjwJWCk1xxdv5Jx7tR0CBOFRNPNOwgz1%2BwcsidB7tbVivNai4urRBeT%2FzXT59InIGYVeI8KHVfwy1eHZmQy%2FS5MDXM8caPu0seOzHhRF7PpYibmzCnmRCN4OBxBDrUEioqe%2BJsL93wEsl6ElDWE8Ff8laLi4MLZUbN6gQ1jFiCYdqwbmAOfCPIK%2Fe%2FnVRRdIoI5jpK82fUujjmoDqqkDj%2BTRTERwvpxvTx49B%2F3FKZCj9GzKr3N8dh46X%2FUermxajA%3D%3D'
'https://fantasy.espn.com/apis/v3/games/flb/seasons/2022/segments/0/leagues/55646?view=mDraftDetail&view=mSettings&view=mTeam&view=modular&view=mNav'
espn_cookies = {'swid': '{8F5C0C75-0EC6-4CD4-9C0C-750EC64CD455}',
 'espn_s2': 'AEBvIL4Dlefi3KlVW0JH87iCDbcx0707HaHAXb8P3MgYzjwJWCk1xxdv5Jx7tR0CBOFRNPNOwgz1%2BwcsidB7tbVivNai4urRBeT%2FzXT59InIGYVeI8KHVfwy1eHZmQy%2FS5MDXM8caPu0seOzHhRF7PpYibmzCnmRCN4OBxBDrUEioqe%2BJsL93wEsl6ElDWE8Ff8laLi4MLZUbN6gQ1jFiCYdqwbmAOfCPIK%2Fe%2FnVRRdIoI5jpK82fUujjmoDqqkDj%2BTRTERwvpxvTx49B%2F3FKZCj9GzKr3N8dh46X%2FUermxajA%3D%3D'}

custom_headers_2 = {
 'Connection': 'keep-alive',
 'Accept': 'application/json, text/plain, */*',
 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
 'x-fantasy-filter': '{"players":{"filterStatsForSplitTypeIds":{"value":[0]},"filterStatsForSourceIds":{"value":[1]},"filterStatsForExternalIds":{"value":[2023]},"sortDraftRanks":{"sortPriority":2,"sortAsc":true,"value":"STANDARD"},"sortPercOwned":{"sortPriority":3,"sortAsc":false},"filterStatsForTopScoringPeriodIds":{"value":5,"additionalValue":["002023","102023","002022","012023","022023","032023","042023","062023","010002023"]}}}',
 'x-fantasy-platform': 'kona-PROD-ee68d9ab1a30c5c961b9d2c47cb84c8f1ce2bd94',
 'x-fantasy-source': 'kona'
}

custom_headers = {
 'Connection': 'keep-alive',
 'Accept': 'application/json, text/plain, */*',
 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
 'x-fantasy-filter': '{"filterActive":null}',
 'x-fantasy-platform': 'kona-PROD-1dc40132dc2070ef47881dc95b633e62cebc9913',
 'x-fantasy-source': 'kona'
}

headers = {
 'Connection': 'keep-alive',
 'Accept': 'application/json, text/plain, */*',
 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
}

# draft details function
def get_draft_details(league_id, season_id):
    # newest API v3 url
    espn_cookies = {'swid': '{8F5C0C75-0EC6-4CD4-9C0C-750EC64CD455}',
    'espn_s2': 'AEBvIL4Dlefi3KlVW0JH87iCDbcx0707HaHAXb8P3MgYzjwJWCk1xxdv5Jx7tR0CBOFRNPNOwgz1%2BwcsidB7tbVivNai4urRBeT%2FzXT59InIGYVeI8KHVfwy1eHZmQy%2FS5MDXM8caPu0seOzHhRF7PpYibmzCnmRCN4OBxBDrUEioqe%2BJsL93wEsl6ElDWE8Ff8laLi4MLZUbN6gQ1jFiCYdqwbmAOfCPIK%2Fe%2FnVRRdIoI5jpK82fUujjmoDqqkDj%2BTRTERwvpxvTx49B%2F3FKZCj9GzKr3N8dh46X%2FUermxajA%3D%3D'}
    url = 'https://fantasy.espn.com/apis/v3/games/flb/seasons/2022/segments/0/leagues/55646?view=mDraftDetail&view=mSettings&view=mTeam&view=modular&view=mNav'
    #url = "https://fantasy.espn.com/apis/v3/games/flb/leagueHistory/{}?view=mDraftDetail&view=mSettings&view=mTeam&view=modular&view=mNav&seasonId={}".format(league_id, season_id)
    r = requests.get(url,
                     cookies=espn_cookies,
                     headers=headers)
    espn_raw_data = r.json()
    draft_picks = espn_raw_data['draftDetail']['picks']
    df = pd.DataFrame(draft_picks)
    # get only columns we need in draft detail
    draft_df = df[['overallPickNumber', 'playerId', 'teamId']].copy()
    return draft_df

def historical_get_draft_details(league_id, season_id):
    # newest API v3 url
    #url = "https://fantasy.espn.com/apis/v3/games/flb/seasons/{}/segments/0/leagues/{}?view=mDraftDetail&view=mSettings&view=mTeam&view=modular&view=mNav".format(season_id, league_id)
    url = "https://fantasy.espn.com/apis/v3/games/flb/leagueHistory/{}?view=mDraftDetail&view=mSettings&view=mTeam&view=modular&view=mNav&seasonId={}".format(league_id, season_id)
    r = requests.get(url,
                     headers=headers,
                     cookies=espn_cookies)
    espn_raw_data = r.json()
    espn_draft_detail = espn_raw_data[0]
    draft_picks = espn_draft_detail['draftDetail']['picks']
    df = pd.DataFrame(draft_picks)
    # get only columns we need in draft detail
    draft_df = df[['overallPickNumber', 'playerId', 'teamId']].copy()
    return draft_df
    

# get player info
def get_player_info(season_id):
    #url = "https://fantasy.espn.com/apis/v3/games/flb/leagueHistory/{}?view=mDraftDetail&view=mSettings&view=mTeam&view=modular&view=mNav&seasonId={}".format(league_id, season_id)
    url = "https://fantasy.espn.com/apis/v3/games/flb/seasons/{}/players?scoringPeriodId=0&view=players_wl".format(season_id)
    POSITION_MAP = {
        0: 'C',
        1: '1B',
        2: '2B',
        3: '3B',
        4: 'SS',
        5: 'OF',
        6: '2B/SS',
        7: '1B/3B',
        8: 'LF',
        9: 'CF',
        10: 'RF',
        11: 'DH',
        12: 'UTIL',
        13: 'P',
        14: 'SP',
        15: 'RP',
        16: 'BE',
        17: 'IL',
        19: 'IF', # 1B/2B/SS/3B
        # reverse TODO
        # 18, 21, 22 have appeared but unknown what position they correspond to
    }
    r = requests.get(url,
                    cookies=espn_cookies,
                    headers=custom_headers)
    player_data = r.json()
    df = pd.DataFrame(player_data)
    df2 = df.loc[pd.notnull(df['eligibleSlots'])].reset_index(drop = True)
    # get only needed columns for players
    player_df = df2[['eligibleSlots', 'defaultPositionId','fullName','id','proTeamId']].copy()
    player_df.eligibleSlots = [[POSITION_MAP.get(pos, pos) for pos in df2['eligibleSlots'][i] if pos not in [12, 17, 19, 13, 16]] for i in range(len(df2))]
    # rename in column
    player_df.rename(columns = {'id':'player_id'}, inplace = True)
    return player_df

# get team information
def get_team_info(season_id):
    url = "https://fantasy.espn.com/apis/v3/games/flb/seasons/{}?view=proTeamSchedules_wl".format(season_id)
    r = requests.get(url,
                     headers=headers,
                     cookies=espn_cookies)
    team_data = r.json()
    team_names = team_data['settings']['proTeams']
    df = pd.DataFrame(team_names)
    # get only needed columns for teams
    team_df = df[['id', 'location', 'name']].copy()
    team_df["team name"] = team_df['location'].astype(str) +" "+ team_df["name"]
    # rename in column
    team_df.rename(columns = {'id':'team_id'}, inplace = True)
    return team_df

# get team information
def get_draft_strategy(season_id, league_type = 'STANDARD'):
    url = "https://fantasy.espn.com/apis/v3/games/flb/seasons/{}/segments/0/leagues/55646?view=kona_player_info_edit_draft_strategy".format(season_id)
    r = requests.get(url,
                     headers=custom_headers_2,
                     cookies=espn_cookies)
    draft_strat_data = r.json()
    if season_id < 2022:
        ids = []
        rankings = []
        for i in range(0, 3000):
                ids = ids + [draft_strat_data['players'][i]['player']['id']]
                rankings = rankings + [i + 1]
        df = pd.DataFrame({'id': ids, 'pre_draft_ranking':rankings})
    else:
        ids = []
        rankings = []
        for i in range(0, 3000):
            ids = ids + [draft_strat_data['players'][i]['player']['id']]
            rankings = rankings + [draft_strat_data['players'][i]['player']['draftRanksByRankType']['STANDARD']['rank']]
        df = pd.DataFrame({'id': ids, 'pre_draft_ranking':rankings})
    return df