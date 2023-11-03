import streamlit as st
from utils.ticket import Ticket
from utils.matchup_data import matchup_mapping, weeks, teams
from utils.ticket_manager import TicketManager
from utils.api_client import APIClient

# Initialize Ticket Manager and API Client
ticket_manager = TicketManager()
api_client = APIClient(api_key="YOUR_API_KEY", base_url="YOUR_BASE_URL")

# Constants
bet_types = ['Spread', 'Over/Under']
spread_values = list(range(-20, 20))
over_under_values = list(range(30, 71))

# Setup Session State
if 'draft_ticket' not in st.session_state:
    st.session_state.draft_ticket = {
        'matchups': [],
        'bets': []
    }
if 'tickets' not in st.session_state:
    st.session_state.tickets = []

# User Input Function
def get_user_input(weeks, bet_types, spread_values, over_under_values):
    # Select Week
    selected_week = st.selectbox('Select Week', weeks)

    # Select Team
    selected_team = st.selectbox('Select Team', sorted(matchup_mapping[selected_week]['teams'].keys()))

    # Opponent team
    opponent_team = matchup_mapping[selected_week]['teams'][selected_team]
    st.write(f'Opponent: {opponent_team}')

    # Select Bet Type
    selected_bet_type = st.selectbox('Bet Type', bet_types)
    
    # Select Bet Value
    if selected_bet_type == 'Spread':
        selected_value = st.selectbox('Select Spread', spread_values)
    else:
        selected_value = st.selectbox('Select Over/Under Value', over_under_values)
    
    return selected_week, selected_team, selected_bet_type, selected_value

# Function to Add Bet to Draft
def add_bet_to_draft(selected_week, selected_team, selected_bet_type, selected_value):
    opponent = matchup_mapping[selected_week].get(selected_team)
    if not opponent:
        st.warning(f"No matchup found for {selected_team} in {selected_week}.")
        return

    st.session_state.draft_ticket['matchups'].append(f"{selected_team} vs {opponent}")
    st.session_state.draft_ticket['bets'].append({
        'type': selected_bet_type,
        'value': selected_value
    })

# Function to Finalize a Ticket
def finalize_ticket():
    num_bets = len(st.session_state.draft_ticket['bets'])
    if 3 <= num_bets <= 10:
        st.session_state.tickets.append(st.session_state.draft_ticket.copy())
        st.session_state.draft_ticket = {
            'matchups': [],
            'bets': []
        }
    else:
        st.warning("A ticket requires between 3 to 10 bets.")

# UI Elements and Logic
st.subheader("Peek-A-Bet")
selected_week, selected_team, selected_bet_type, selected_value = get_user_input(weeks, bet_types, spread_values, over_under_values)

# Add Bet Button
if st.button("Add Bet"):
    add_bet_to_draft(selected_week, selected_team, selected_bet_type, selected_value)

# Display Draft Ticket
st.subheader("Draft Ticket")
for i, (matchup, bet) in enumerate(zip(st.session_state.draft_ticket['matchups'], st.session_state.draft_ticket['bets'])):
    st.write(f"{matchup} - {bet['type']} {bet['value']}")
    if st.button(f"Remove Bet {i+1}"):
        del st.session_state.draft_ticket['matchups'][i]
        del st.session_state.draft_ticket['bets'][i]

# Finalize Ticket Button
if st.button("Finalize Ticket"):
    finalize_ticket()

# Display All Tickets
tickets_data = [{'Ticket ID': i + 1, "Matchups": ', '.join(ticket['matchups']), "Bets": ', '.join([f"{bet['type']} {bet['value']}" for bet in ticket['bets']])} for i, ticket in enumerate(st.session_state.tickets)]
st.table(tickets_data)

# Check Scores
st.write("Check Ticket Status")
if st.button("Check Scores"):
    # For now, this checks the most recently selected team and week, but this can be modified
    try:
        game_data = api_client.get_game_data(team=selected_team, week=selected_week)
        if game_data:
            st.write(f"Match: {game_data['team_home']} vs {game_data['team_away']}")
            st.write(f"Score: {game_data['score_home']} - {game_data['score_away']}")
        else:
            st.warning(f"No game data found for {selected_team} in week {selected_week}.")
    except Exception as e:
        st.error(f"Error: {str(e)}")

# Debugging: Displaying Teams
st.write("Teams:")
st.write(teams)
