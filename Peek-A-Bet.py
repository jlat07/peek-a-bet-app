import streamlit as st
from utils.ticket_manager import TicketManager

# Initialize Ticket Manager
ticket_manager = TicketManager()

# Global Constants/Variables Initialization
matchup_mapping = {
    'Week 1': {'Team A': 'Team B', 'Team C': 'Team D'},
    'Week 2': {'Team A': 'Team C', 'Team B': 'Team D'},
}

weeks = ['Week 1', 'Week 2', 'Week 3']
teams = ['Team A', 'Team B', 'Team C', 'Team D']
bet_types = ['Spread', 'Over/Under']
spread_values = list(range(-10, 11))

# User Input Function
def get_user_input(weeks, teams, bet_types, spread_values):
    selected_week = st.selectbox('Select Week', weeks, key='select_week_key')
    selected_team = st.selectbox('Select Team', teams, key='select_team_key')
    selected_bet_type = st.selectbox('Bet Type', bet_types, key='select_bet_types_key')
    selected_spread = None
    over_under_value = None
    if selected_bet_type == 'Spread':
        selected_spread = st.selectbox('Select Spread', spread_values, key='select_spread_values_key')
    else:
        over_under_value = st.number_input('Enter Over/Under Value', value=50.0)
    
    return selected_week, selected_team, selected_bet_type, selected_spread, over_under_value

# Check if user input is in session state
if "user_input" not in st.session_state:
    st.session_state.user_input = get_user_input(weeks, teams, bet_types, spread_values)

selected_week, selected_team, selected_bet_type, selected_spread, over_under_value = st.session_state.user_input

# Initialize the session state variables if they don't exist
if 'temp_matchups' not in st.session_state:
    st.session_state.temp_matchups = []

if 'temp_bets' not in st.session_state:
    st.session_state.temp_bets = []

# Add Match-up Logic
if st.button("Add Match-up"):
    opponent = matchup_mapping[selected_week].get(selected_team, "Unknown")
    st.session_state.temp_matchups.append(f"{selected_team} vs {opponent}")
    st.session_state.temp_bets.append({
        'type': selected_bet_type,
        'value': selected_spread if selected_bet_type == 'Spread' else over_under_value
    })

# Display Current Match-ups for New Ticket
st.subheader("Current Match-ups for New Ticket:")
for matchup, bet in zip(st.session_state.temp_matchups, st.session_state.temp_bets):
    st.write(f"{matchup} - {bet['type']} {bet['value']}")

# Finalize Ticket Logic
if st.button("Finalize Ticket"):
    ticket_manager.add_ticket(st.session_state.temp_matchups, st.session_state.temp_bets)
    st.session_state.temp_matchups.clear()
    st.session_state.temp_bets.clear()

# Display Tickets
with st.container():
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Ticket ID")
        for ticket_id in ticket_manager.get_all_tickets():
            st.write(ticket_id)

    with col2:
        st.subheader("Ticket Details")
        for ticket in ticket_manager.ordered_tickets():
            st.markdown(f"**Matchups:** {', '.join(ticket.matchups)}")
            st.markdown(f"**Bets:** {', '.join(['{} {}'.format(bet['type'], bet['value']) for bet in ticket.bets])}")
