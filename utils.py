# utils.py

def get_team_variants(team_name):
    if team_name == "Delhi Capitals":
        return ["Delhi Capitals", "Delhi Daredevils"]
    elif team_name == "Punjab Kings":
        return ["Kings XI Punjab", "Punjab Kings"]
    elif team_name == "Rising Pune Supergiants":
        return ["Rising Pune Supergiant", "Rising Pune Supergiants"]
    elif team_name == "Royal Challengers Bengaluru":
        return ["Royal Challengers Bangalore", "Royal Challengers Bengaluru"]
    else: 
        return [team_name]
    
    
def get_head_to_head_stats(df, team1_names, team2_names, start_date):
    """Calculates total matches and wins between two team variant lists."""
    matches = (
        ((df["team1"].isin(team2_names) & df["team2"].isin(team1_names)) | 
        (df["team1"].isin(team1_names) & df["team2"].isin(team2_names))) & 
        (df["match_date"] >= start_date)
    )

    wins = matches & (df["winner"].isin(team1_names))
    toss = matches & (df["toss_winner"].isin(team1_names))
    
    return matches.sum(), wins.sum(), toss.sum()


def specific_team_stats(df, team_name):
    matches = (
        ((df["team1"].isin(team_name) | df["team2"].isin(team_name)))
    )
    wins = matches & (df["winner"].isin(team_name))
    
    return matches.sum(), wins.sum()