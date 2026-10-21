import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils import get_team_variants, get_head_to_head_stats, specific_team_stats

#streamlit run app.py

# Cache the data so it doesn't rstreamlit run app.pyeload on every UI interaction
@st.cache_data
def load_data():
    return pd.read_csv("Match_Info.csv")

df = load_data()

# Clean list of teams for the dropdowns
ipl_teams_list = [
    "Chennai Super Kings", "Deccan Chargers", "Delhi Capitals",
    "Gujarat Lions", "Gujarat Titans", "Kochi Tuskers Kerala",
    "Kolkata Knight Riders", "Lucknow Super Giants", "Mumbai Indians",
    "Pune Warriors", "Punjab Kings", "Rajasthan Royals",
    "Rising Pune Supergiants", "Sunrisers Hyderabad",
    "Royal Challengers Bengaluru"
]

st.title("🏏 IPL Data Analyzer")

# Choose the type of analysis
analysis_type = st.radio(
    "Choose Analysis Type:",
    ("Single Team Analysis", "Head-to-Head Comparison")
)

st.divider()

if analysis_type == "Single Team Analysis":
    st.subheader("Single Team Analysis")
    team = st.selectbox("Select Team", ipl_teams_list, index=0)
    
    if st.button("Analyze Team"):
        selected_names = get_team_variants(team)
        matches_num, wins_num = specific_team_stats(df, selected_names)
        
        if matches_num > 0:
            win_percentage = (wins_num / matches_num) * 100
        else:
            win_percentage = 0.0
            
        st.success(f"**{team}** has played **{matches_num}** games and won **{wins_num}** games.")
        st.info(f"Winning percentage is **{win_percentage:.2f}%**")

elif analysis_type == "Head-to-Head Comparison":
    st.subheader("Head-to-Head Comparison")
    
    # UI Layout: Create two columns for team selection
    col1, col2 = st.columns(2)

    with col1:
        team1 = st.selectbox("Select First Team", ipl_teams_list, index=0)

    with col2:
        team2 = st.selectbox("Select Second Team", ipl_teams_list, index=8)

    # Input for the season
    date = st.text_input("Enter the starting season to include in the data analysis (2008-2026):", "2008")

    if st.button("Analyze Matches"):
        if team1 == team2:
            st.warning("Please select two different teams to compare.")
        else:
            # Fetch variants from your utils
            selected_names1 = get_team_variants(team1)
            selected_names2 = get_team_variants(team2)
            
            # Calculate stats
            matches_num, wins_num, toss_num = get_head_to_head_stats(df, selected_names1, selected_names2, date)
            
            win_percentage = (wins_num / matches_num) * 100 if matches_num > 0 else 0.0
                
            st.subheader("Analysis Results")
            st.write(f"**{team1}** has played **{matches_num}** matches against **{team2}**.")
            st.write(f"**{team1}** has won **{wins_num}** matches against **{team2}**.")
            
            if matches_num > 0:
                if win_percentage >= 50:
                    st.success(f"{team1} has a winning record against {team2}. Having won {win_percentage:.2f}% of the games played.")
                else:
                    st.error(f"{team1} has a losing record against {team2}. Having won only {win_percentage:.2f}% of the games played.")
                
                st.info(f"{team1} won the toss {toss_num} times while {team2} won the toss {matches_num - toss_num} times.")
                
                # --- MATPLOTLIB CHART ---
                team2wins = matches_num - wins_num
                
                # Using subplots is the best practice for Streamlit to prevent rendering overlaps
                fig, ax = plt.subplots(figsize=(6, 4))
                categories = [f"{team1}", f"{team2}"]
                values = [wins_num, team2wins]
                
                ax.bar(categories, values, color=['blue', 'red'])
                ax.set_title(f"{team1} vs {team2} Performance")
                ax.set_ylabel("Wins")
                
                # Display the chart in Streamlit
                st.pyplot(fig)
                
            else:
                st.warning("No matches found for the selected criteria.")