import streamlit as st
from utils.ticket import Ticket
from utils.ticket_manager import TicketManager
from utils.api_client import APIClient

# Initialize Ticket Manager
ticket_manager = TicketManager()

# Instantiate the API client
api_client = APIClient(api_key="YOUR_API_KEY", base_url="YOUR_BASE_URL")

# Global Constants/Variables Initialization
matchup_mapping = {
    'Week 1': {'Team A': 'Team B', 'Team C': 'Team D'},
    'Week 2': {'Team A': 'Team C', 'Team B': 'Team D'},
    # ... [Add more weeks as needed]
}

weeks = ['Week 1', 'Week 2', 'Week 3']
teams = ['Team A', 'Team B', 'Team C', 'Team D']
bet_types = ['Spread', 'Over/Under']
spread_values = list(range(-10, 11))

# User Input Function
def get_user_input(weeks, teams, bet_types, spread_values, over_under_values):
    selected_week = st.selectbox('Select Week', weeks, key='select_week_key')
    selected_team = st.selectbox('Select Team', teams, key='select_team_key')
    selected_bet_type = st.selectbox('Bet Type', bet_types, key='select_bet_types_key')
    
    if selected_bet_type == 'Spread':
        selected_value = st.selectbox('Select Spread', spread_values, key='select_spread_values_key')
    else:
        selected_value = st.selectbox('Select Over/Under Value', over_under_values, key='select_over_under_values_key')
    
    return selected_week, selected_team, selected_bet_type, selected_spread, over_under_value



# ... [Your code for adding matchups and finalizing tickets]

st.subheader("Check Ticket Status")
if st.button("Check Scores"):
    try:
        game_data = api_client.get_game_data(team=selected_team, week=selected_week)
        if game_data:
            # Your logic to determine ticket status and deltas based on fetched scores
            # and user's ticket data goes here

            # For demonstration purposes:
            st.write(f"Match: {game_data['team_home']} vs {game_data['team_away']}")
            st.write(f"Score: {game_data['score_home']} - {game_data['score_away']}")
            st.write(f"Ticket Status: Green (This is just an example. Replace with actual logic.)")
            st.write(f"Score Delta: +4 (Again, an example. Replace with actual logic.)")
            
        else:
            st.warning(f"No game data found for {selected_team} in week {selected_week}.")

    except Exception as e:
        st.error(f"Error: {str(e)}")

def add_matchup_to_session(selected_week, selected_team, selected_bet_type, selected_value):
    opponent = matchup_mapping[selected_week].get(selected_team)
    if not opponent:
        st.warning(f"No matchup found for {selected_team} in {selected_week}.")
        return

    st.session_state.temp_matchups.append(f"{selected_team} vs {opponent}")
    st.session_state.temp_bets.append({
        'type': selected_bet_type,
        'value': selected_value
    })

def finalize_ticket():
    ticket_manager.add_ticket(st.session_state.temp_matchups, st.session_state.temp_bets)
    st.session_state.temp_matchups.clear()
    st.session_state.temp_bets.clear()

over_under_values = list(range(30, 71))

# Check if user input is in session state
... # [The previous logic for session state goes here]

# Add Match-up Logic
if st.button("Add Match-up"):
    st.session_state.user_input = get_user_input(weeks, teams, bet_types, spread_values, over_under_values)
    add_matchup_to_session(*st.session_state.user_input)

# Display Current Match-ups for New Ticket
... # [The previous logic to display match-ups goes here]

# Finalize Ticket Logic
if st.button("Finalize Ticket"):
    finalize_ticket()

# Display Tickets in a Table
tickets_data = []
for ticket in ticket_manager.ordered_tickets():
    tickets_data.append({
        "Ticket ID": ticket.ticket_id,
        "Matchups": ', '.join(ticket.matchups),
        "Bets": ', '.join([f"{bet['type']} {bet['value']}" for bet in ticket.bets])
    })

st.table(tickets_data)
