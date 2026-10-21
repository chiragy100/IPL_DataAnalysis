import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from utils import get_team_variants, get_head_to_head_stats, specific_team_stats

df = pd.read_csv("Match_Info.csv")

ipl_teams = {
    "A": "Chennai Super Kings",
    "B": "Deccan Chargers",
    "C": "Delhi Capitals",
    "D": "Gujarat Lions",
    "E": "Gujarat Titans",
    "F": "Kochi Tuskers Kerala",
    "G": "Kolkata Knight Riders",
    "H": "Lucknow Super Giants",
    "I": "Mumbai Indians",
    "J": "Pune Warriors",
    "K": "Punjab Kings",
    "L": "Rajasthan Royals",
    "M": "Rising Pune Supergiants",
    "N": "Sunrisers Hyderabad",
    "O": "Royal Challengers Bengaluru"
}

# Define the options clearly
menu = """
IPL Teams
[A] Chennai Super Kings
[B] Deccan Chargers
[C] Delhi Capitals
[D] Gujarat Lions
[E] Gujarat Titans
[F] Kochi Tuskers Kerala
[G] Kolkata Knight Riders
[H] Lucknow Super Giants
[I] Mumbai Indians
[J] Pune Warriors
[K] Punjab Kings
[L] Rajasthan Royals
[M] Rising Pune Supergiants
[N] Sunrisers Hyderabad
[O] Royal Challengers Bengaluru
"""

# Print the menu and get the input cleanly
print(menu)

h2h_team = input("Would you like to analyze a specfic team or head-to-head comparison of two teams (A, B): ").strip().upper()

if h2h_team == "A":
        team = input("Enter the letter corresponding to the team you would like to analyze: ").strip().upper()
    
        result = ipl_teams[team]
    
        selected_names = get_team_variants(result)
        matches_num, wins_num = specific_team_stats(df, selected_names)
        
        if matches_num > 0:
            win_percentage = (wins_num / matches_num) * 100
        else:
            win_percentage = 0.0
        
        print(f"{result} has played {matches_num} games and won {wins_num} games. Winning percentage is {win_percentage}%")
            
    
elif h2h_team == "B":
    team1 = input("Enter the letter corresponding to the first team you would like to analyze: ").strip().upper()
    team2 = input("Enter the letter corresponding to the second team you would like to analyze: ").strip().upper()

    date = input("Enter the first season to include in the data analysis (2008-2026):")

    #date = input("Enter the season you would like to analyze (2008-2026): ")

    result = ipl_teams[team1]
    result2 = ipl_teams[team2]

    selected_names = get_team_variants(result)
    selected_names2 = get_team_variants(result2)

    matches_num, wins_num, toss_num = get_head_to_head_stats(df, selected_names, selected_names2, date)

    # Prevent division by zero if they haven't played
    if matches_num > 0:
        win_percentage = (wins_num / matches_num) * 100
    else:
        win_percentage = 0.0

    print(f"{result} has played {matches_num} matches against {result2}.")
    print(f"{result} has won {wins_num} matches against {result2}.")

    if win_percentage > 50:
        print(f"{result} has a winning record against {result2}. Having won {win_percentage:.2f}% of the games played.")
    else:
        print(f"{result} has a losing record against {result2}. Having won only {win_percentage:.2f}% of the games played.")
        
    print(f"{result} won the toss {toss_num} times while {result2} won the toss {matches_num-toss_num} times.")
    
    team2wins = matches_num - wins_num
    
    categories = [result + " Wins", result2 + ' Wins']
    values = [wins_num, team2wins]
    plt.bar(categories, values, color=['blue', 'red'])
    plt.title(f"{result} vs {result2} Performance")
    plt.ylabel("Win Comparison")
    plt.show()    
else: 
    print("Error")