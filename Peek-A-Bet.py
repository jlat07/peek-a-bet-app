import streamlit as st
from utils.ticket_manager import TicketManager


## 

# 1. Define the get_user_input function
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

# 2. Use the get_user_input function in session state
if "user_input" not in st.session_state:
    st.session_state.user_input = get_user_input(weeks, teams, bet_types, spread_values)

selected_week, selected_team, selected_bet_type, selected_spread, over_under_value = st.session_state.user_input


# Initialize Ticket Manager
ticket_manager = TicketManager()

st.title("Peek-A-Bet")

# Display Total potential win
total_win = len(ticket_manager.get_all_tickets()) * 100
st.write(f"Total potential win amount: ${total_win}")


# Initialize the session state variables if they don't exist
if 'temp_matchups' not in st.session_state:
    st.session_state.temp_matchups = []

if 'temp_bets' not in st.session_state:
    st.session_state.temp_bets = []

# This is a simplified mapping for demonstration. Enhance based on real data.
matchup_mapping = {
    'Week 1': {'Team A': 'Team B', 'Team C': 'Team D'},
    'Week 2': {'Team A': 'Team C', 'Team B': 'Team D'},
    # ... add more weeks as needed
}

weeks = ['Week 1', 'Week 2', 'Week 3']
teams = ['Team A', 'Team B', 'Team C', 'Team D']
bet_types = ['Spread', 'Over/Under']
spread_values = list(range(-10, 11))  # for simplicity, using -10 to +10 as spreads

# Temporary storage for match-ups and bets in the current ticket
# temp_matchups = []
# temp_bets = []

##----------BUTTONS--------

if st.button("Add Match-up"):
    # Use session state variables instead of the local ones
    opponent = matchup_mapping[selected_week].get(selected_team, "Unknown")
    st.session_state.temp_matchups.append(f"{selected_team} vs {opponent}")
    st.session_state.temp_bets.append({
        'type': selected_bet_type,
        'value': selected_spread if selected_bet_type == 'Spread' else over_under_value
    })

if st.button("Finalize Ticket"):
    ticket_manager.add_ticket(st.session_state.temp_matchups, st.session_state.temp_bets)
    # Clear the session state variables
    st.session_state.temp_matchups.clear()
    st.session_state.temp_bets.clear()


# Display current match-ups
st.subheader("Current Match-ups for New Ticket:")
for matchup, bet in zip(st.session_state.temp_matchups, st.session_state.temp_bets):
    st.write(f"{matchup} - {bet['type']} {bet['value']}")


# Display Ticket IDs and details
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

    with col3:
        st.subheader("Organize")
        for ticket_id in ticket_manager.get_all_tickets():
            new_position = st.selectbox(f'Position for {ticket_id}', list(range(1, len(ticket_manager.get_all_tickets())+1)), index=ticket_manager.ticket_order.index(ticket_id))
            ticket_manager.change_ticket_order(ticket_id, new_position-1)

if st.button("Reset Input"):
    if "user_input" in st.session_state:
        del st.session_state.user_input

