# Peek-A-Bet.py

import streamlit as st
from utils.ticket_manager import TicketManager

# Initialize Ticket Manager
ticket_manager = TicketManager()

st.title("Peek-A-Bet")

# Sample data (this should eventually come from your data source)
weeks = ['Week 1', 'Week 2', 'Week 3']
teams = ['Team A', 'Team B', 'Team C', 'Team D']
bet_types = ['Spread', 'Over/Under']
spread_values = list(range(-10, 11))  # for simplicity, using -10 to +10 as spreads

# Temporary storage for match-ups and bets in the current ticket
temp_matchups = []
temp_bets = []

# Collect ticket input
selected_week = st.selectbox('Select Week', weeks)
selected_team = st.selectbox('Select Team', teams)
selected_bet_type = st.selectbox('Bet Type', bet_types)
if selected_bet_type == 'Spread':
    selected_spread = st.selectbox('Select Spread', spread_values)
else:
    over_under_value = st.number_input('Enter Over/Under Value', value=50.0)

# Add button to finalize this match-up
if st.button("Add Match-up"):
    temp_matchups.append(f"{selected_team} vs ???")  # Needs more logic to get opponent
    temp_bets.append({
        'type': selected_bet_type,
        'value': selected_spread if selected_bet_type == 'Spread' else over_under_value
    })

# Display current match-ups
st.subheader("Current Match-ups for New Ticket:")
for matchup, bet in zip(temp_matchups, temp_bets):
    st.write(f"{matchup} - {bet['type']} {bet['value']}")

# Add new ticket button
if st.button("Finalize Ticket"):
    ticket_manager.add_ticket(temp_matchups, temp_bets)
    temp_matchups.clear()
    temp_bets.clear()

# Display all tickets
st.subheader("All Tickets:")
for ticket in ticket_manager.get_all_tickets().values():
    st.write(ticket.display())
