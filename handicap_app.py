
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Course & tee data
tee_options = {
    "White": {"rating": 32.7, "slope": 113},
    "Blue": {"rating": 33.5, "slope": 118},
    "Red": {"rating": 31.2, "slope": 107},
}

holes = 9
pars = [4, 3, 4, 4, 3, 5, 4, 3, 4]

# Handicap calculation helpers
def handicap_differential(score, rating, slope):
    return ((score - rating) * 113) / slope

def course_handicap(index, slope):
    return round(index * slope / 113)

# State initialization
if "players" not in st.session_state:
    st.session_state.players = {}
if "tee_color" not in st.session_state:
    st.session_state.tee_color = "White"

# Sidebar controls
st.sidebar.title("Settings")
st.sidebar.selectbox("Tee Color", options=tee_options.keys(), key="tee_color")
new_player = st.sidebar.text_input("Add New Player")
if st.sidebar.button("Add Player") and new_player:
    if new_player not in st.session_state.players:
        st.session_state.players[new_player] = []

# Main layout
st.title("🏌️ Wellington Greens Handicap Tracker")
tee = tee_options[st.session_state.tee_color]
rating, slope = tee["rating"], tee["slope"]

for player, rounds in st.session_state.players.items():
    st.subheader(player)
    for i, round_scores in enumerate(rounds):
        cols = st.columns(holes)
        for j in range(holes):
            round_scores[j] = cols[j].number_input(
                f"Hole {j+1}", value=round_scores[j], key=f"{player}_{i}_{j}", min_value=0
            )
    if st.button(f"Add Round for {player}"):
        st.session_state.players[player].append([0] * holes)

    # Handicap calculations
    if rounds:
        totals = [sum(r) for r in rounds]
        diffs = sorted([handicap_differential(s, rating, slope) for s in totals])
        top3 = diffs[:3]
        if top3:
            index = round(np.mean(top3) * 0.96, 1)
            chcp = course_handicap(index, slope)
            st.markdown(f"**Handicap Index:** {index}  \n**Course Handicap ({st.session_state.tee_color}):** {chcp}")
            
            # Chart
            st.line_chart(pd.DataFrame({'Total Score': totals}, index=[f'Round {i+1}' for i in range(len(totals))]))
