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

### 1. Session State Adjustments
if 'draft_ticket' not in st.session_state:
    st.session_state.draft_ticket = {
        'matchups': [],
        'bets': []
    }

if 'tickets' not in st.session_state:
    st.session_state.tickets = []

# User Input Function
# def get_user_input(weeks, teams, bet_types, spread_values, over_under_values):
#     selected_week = st.selectbox('Select Week', weeks, key='select_week_key')
#     selected_team = st.selectbox('Select Team', teams, key='select_team_key')
#     selected_bet_type = st.selectbox('Bet Type', bet_types, key='select_bet_types_key')
    
#     if selected_bet_type == 'Spread':
#         selected_value = st.selectbox('Select Spread', spread_values, key='select_spread_values_key')
#     else:
#         selected_value = st.selectbox('Select Over/Under Value', over_under_values, key='select_over_under_values_key')
    
#     return selected_week, selected_team, selected_bet_type, selected_value

def get_user_input():
    # Select Week
    selected_week = st.selectbox('Select Week', list(matchup_mapping.keys()))

    # Select Team
    selected_team = st.selectbox('Select Team', sorted(matchup_mapping[selected_week]['teams'].keys()))

    # Opponent team (displayed for user's information)
    opponent_team = matchup_mapping[selected_week]['teams'][selected_team]
    st.write(f'Opponent: {opponent_team}')

    # Slider for Spread
    spread_slider = st.slider('Select Spread (Slider)', min_value=-50.0, max_value=50.0, value=0.0, step=0.5)
    st.write(f"You selected a spread of: {spread_slider}")

    # Input for Spread
    spread_input = st.number_input('Enter Spread (Input)', min_value=-50.0, max_value=50.0, value=0.0, step=0.5)
    st.write(f"You entered a spread of: {spread_input}")

    # Slider for Over/Under
    ou_slider = st.slider('Select Over/Under (Slider)', min_value=0.0, max_value=200.0, value=50.0, step=0.5)
    st.write(f"You selected an Over/Under of: {ou_slider}")

    # Input for Over/Under
    ou_input = st.number_input('Enter Over/Under (Input)', min_value=0.0, max_value=200.0, value=50.0, step=0.5)
    st.write(f"You entered an Over/Under of: {ou_input}")

    # Depending on which input method (slider or input box) you decide to use,
    # return the appropriate values for spread and over/under.
    return selected_week, selected_team, spread_input, ou_input


### 2. Modifying Bet Adding Logic
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

### 3. Finalizing a Ticket
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
selected_week, selected_team, selected_bet_type, selected_value = get_user_input(weeks, teams, bet_types, spread_values, over_under_values)

if st.button("Add Bet"):
    add_bet_to_draft(selected_week, selected_team, selected_bet_type, selected_value)

### 4. Display Draft Ticket and Finalized Tickets
# Display Draft Ticket
st.subheader("Draft Ticket")
for i, (matchup, bet) in enumerate(zip(st.session_state.draft_ticket['matchups'], st.session_state.draft_ticket['bets'])):
    st.write(f"{matchup} - {bet['type']} {bet['value']}")
    if st.button(f"Remove Bet {i+1}"):
        del st.session_state.draft_ticket['matchups'][i]
        del st.session_state.draft_ticket['bets'][i]

if st.button("Finalize Ticket"):
    finalize_ticket()

tickets_data = [{'Ticket ID': i + 1, "Matchups": ', '.join(ticket['matchups']), "Bets": ', '.join([f"{bet['type']} {bet['value']}" for bet in ticket['bets']])} for i, ticket in enumerate(st.session_state.tickets)]
st.table(tickets_data)

# Check Scores Button and Logic
st.write("Check Ticket Status")
if st.button("Check Scores"):
    try:
        # Accessing the saved values from session state
        selected_week = st.session_state.user_input[0]
        selected_team = st.session_state.user_input[1]

        game_data = api_client.get_game_data(team=selected_team, week=selected_week)
        
        if game_data:
            st.write(f"Match: {game_data['team_home']} vs {game_data['team_away']}")
            st.write(f"Score: {game_data['score_home']} - {game_data['score_away']}")
            st.write(f"Ticket Status: Green (This is just an example. Replace with actual logic.)")
            st.write(f"Score Delta: +4 (Again, an example. Replace with actual logic.)")
            
        else:
            st.warning(f"No game data found for {selected_team} in week {selected_week}.")

    except Exception as e:
        st.error(f"Error: {str(e)}")


## Debug
st.write("print teams")
st.write(teams)

