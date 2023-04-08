import pandas as pd
from math import log
# from .elo import calculate_elo_changes

INITIAL_ELO_RATING = 1300
K = 20
SEASON = 2023

teams_df = pd.read_csv("data_2023/MTeams.csv", index_col='TeamID')
teams_df = teams_df[teams_df['LastD1Season'] == SEASON]

elo_df = teams_df
elo_df[SEASON] = INITIAL_ELO_RATING
elo_df = elo_df[[SEASON]]

print(elo_df)

reg_season_df = pd.read_csv("data_2023/MRegularSeasonCompactResults.csv.zip", compression='zip')
reg_season_df = reg_season_df[reg_season_df['Season'] == SEASON]
print(reg_season_df)

# https://fivethirtyeight.com/features/how-we-calculate-nba-elo-ratings/

for index, row in reg_season_df.iterrows():
    # w_ind = elo_df.index[elo_df['TeamID'] == row['WTeamID']]
    # print(row['WTeamID'])
    # print(type(row['WTeamID']))
    w_elo = elo_df.at[row['WTeamID'], SEASON]
    # print(f'w_elo: {w_elo}')
    # l_ind = elo_df.index[elo_df['TeamID'] == row['LTeamID']]
    l_elo = elo_df.at[row['LTeamID'], SEASON]
    # print(f'l_elo: {l_elo}')

    # ratings difference
    diff_elo = abs(w_elo - l_elo) + 100 if row['WLoc'] == 'H' else abs(w_elo - l_elo)
    # print(f'diff_elo: {diff_elo}')
    # expected score difference
    we = 1 / (10 ** (-diff_elo / 400) + 1)
    # print(f'we: {we}')
    # victory margin
    v_mar = 1 + log((row['WScore'] - row['LScore']) + 1) * (2.2/((w_elo - l_elo) * .001 + 2.2))
    # elo change
    d_elo = (w_elo + K * (v_mar - we)) - w_elo
    # print(f'd_elo: {d_elo}')

    elo_df.at[row['WTeamID'], SEASON] = w_elo + d_elo
    elo_df.at[row['LTeamID'], SEASON] = l_elo - d_elo

    reg_season_df.at[index, 'eloChange'] = d_elo


print(reg_season_df)
print(elo_df)
print()
print(elo_df.max())
print(elo_df.min())
print(elo_df.mean())

elo_df.to_csv('data_2023/eloRatings.csv')