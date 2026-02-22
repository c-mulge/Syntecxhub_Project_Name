import pandas as pd

matches = pd.read_csv('data/matches.csv')
deliveries = pd.read_csv('data/deliveries.csv')

season_data = matches[['id','season']]
deliveries = deliveries.merge(season_data, left_on='match_id', right_on='id')

players = ["V Kohli", "RG Sharma", "MS Dhoni"]
player_data = deliveries[deliveries['batter'].isin(players)]

# Total runs
total_runs = player_data.groupby('batter')['batsman_runs'].sum()

# strike rate
legal = player_data[player_data['extra_runs'] == 0]
runs = player_data.groupby('batter')['batsman_runs'].sum()
balls = legal.groupby('batter')['ball'].count()
sr = (runs/balls)*100

# average runs per match
match_runs = player_data.groupby(['batter','match_id'])['batsman_runs'].sum()
avg = match_runs.groupby('batter').mean()
with open('outputs/report.txt','w') as f:

    f.write("IPL PLAYER PERFORMANCE ANALYSIS\n\n")

    f.write("Total Runs:\n")
    f.write(str(total_runs))
    f.write("\n\nStrike Rate:\n")
    f.write(str(sr.round(2)))

    f.write("\n\nAverage Runs Per Match:\n")
    f.write(str(avg.round(2)))

    best_batsman = total_runs.idxmax()
    best_sr = sr.idxmax()

    f.write(f"\n\nInsight:\n")
    f.write(f"{best_batsman} is the highest run scorer.\n")
    f.write(f"{best_sr} has the most aggressive batting (highest strike rate).\n")
