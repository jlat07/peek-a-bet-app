import streamlit as st
from utils.ticket import Ticket
from utils.data_and_config import matchup_mapping, weeks, teams, bet_types, spread_values, over_under_values
from utils.ticket_manager import TicketManager
from utils.api_client import APIClient

# Initialize Ticket Manager and API Client
ticket_manager = TicketManager()
api_client = APIClient(api_key="YOUR_API_KEY", base_url="YOUR_BASE_URL")

# Setup Session State
if 'draft_ticket' not in st.session_state:
    st.session_state.draft_ticket = {
        'matchups': [],
        'bets': []
    }

if 'delete_buttons' not in st.session_state:
    st.session_state.delete_buttons = [False] * len(st.session_state.draft_ticket['bets'])
        
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
    opponent = matchup_mapping[selected_week]['teams'][selected_team]
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
        st.session_state.tickets.append(st.session_state.draft_ticket.copy())  # Use copy to ensure you're not appending a reference
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
    # The button is bound to a specific slot in the session state list
    if st.button(f"Remove Bet {i+1}"):
        st.session_state.delete_buttons[i] = True

# Handle bet deletions after displaying them all
for i, delete_clicked in reversed(list(enumerate(st.session_state.delete_buttons))):
    if delete_clicked:
        del st.session_state.draft_ticket['matchups'][i]
        del st.session_state.draft_ticket['bets'][i]
        st.session_state.delete_buttons[i] = False  # Reset the button state

# Reset the delete_buttons list length to match the number of current bets
st.session_state.delete_buttons = [False] * len(st.session_state.draft_ticket['bets'])



# Finalize Ticket Button
if st.button("Finalize Ticket"):
    finalize_ticket()

# Display All Tickets

# # Note: This assumes you already have a function or method that checks the ticket's outcome based on game data.

# for i, ticket in enumerate(st.session_state.tickets):
#     st.subheader(f"Ticket ID: {i + 1}")
#     ticket_data = []

#     # Placeholder game data. This should come from your API call or some source of truth.
#     game_data = {
#         "team_home": "Baltimore Ravens",
#         "score_home": 35,
#         "team_away": "Cincinnati Bengals",
#         "score_away": 30
#     }

#     for matchup, bet in zip(ticket['matchups'], ticket['bets']):
#         status, delta = "Playing", None
#         if bet['type'] == "Spread":
#             if bet['type'] == "Spread":
#                 if matchup.split(" vs ")[0] == game_data["team_home"]:
#                     delta = (game_data["score_home"] + bet['value']) - game_data["score_away"]
#                 else:
#                     delta = (game_data["score_away"] + bet['value']) - game_data["score_home"]

#                 status = "Covered" if delta > 0 else "Not Covered"

#         elif bet['type'] == "Over/Under":
#             total_score = game_data["score_home"] + game_data["score_away"]
#             delta = total_score - bet['value']
#             if delta > 0:
#                 status = "Over"
#             else:
#                 status = "Under"

#         status_color = "green" if status in ["Over", "Under"] else "red"
#         status_md = f"<span style='color:{status_color}'>{status}</span>"

#         ticket_data.append({
#             "Matchup": matchup,
#             "Bet Type": bet['type'],
#             "Bet Value": bet['value'],
#             "Status": status_md,
#             "Delta": delta
#         })

#     st.table(ticket_data)

#### OLD PEEK-A-BET Styling

# for ticket in st.session_state.tickets:
#     st.write(f"Ticket ID: ...")  # Displaying ticket ID for reference
#     for matchup, bet in zip(ticket['matchups'], ticket['bets']):
        
#         # Assuming the 'bet' dictionary contains a 'status' key. 
#         # This status can be 'win', 'lose', 'pending', etc.
#         # Replace with actual logic or data structure if different
#         status = bet.get('status', 'pending')

#         status_color = "gray"
#         border_style = "none"
        
#         if status == "win":
#             status_color = "green"
#             border_style = "2px solid black"
#         elif status == "lose":
#             status_color = "red"
#             border_style = "2px solid black"

#         col1, col2, col3, col4 = st.columns([3, 2, 2, 1])  # Adjust the column widths as per your needs
        
#         with col1:
#             st.write(matchup)  # e.g. "Team A vs Team B"
        
#         with col2:
#             st.write(bet['type'])  # e.g. "Spread" or "Over/Under"
        
#         with col3:
#             st.write(bet['value'])  # e.g. "+5" or "50"
        
#         with col4:
#             st.markdown(f"<div style='background-color: {status_color}; border: {border_style}; padding: 10px;'>{status.capitalize()}</div>", unsafe_allow_html=True)
        
#     st.write("---")  # A separator line after each ticket for better clarity


### 3rd times a charm

...

# Existing code above...

### Display Finalized Tickets with Enhanced Styling ###

st.subheader("Finalized Tickets")

for ticket in st.session_state.tickets:
    st.markdown("### Ticket ID")
    
    # Extract the matchups and bets from the ticket
    matchups = ticket['matchups']
    bets = ticket['bets']
    
    for matchup, bet in zip(matchups, bets):
        # Get the game data based on the matchup
        teams = matchup.split(" vs ")
        game_data = api_client.get_game_data(teams[0], selected_week)
        
        # Default to gray (0-0 score)
        status_color = "gray"
        border_style = "none"
        
        # Check if there's a score
        if game_data and game_data.get('score_home') != 0 and game_data.get('score_away') != 0:
            # Evaluate the bet condition here and update status_color
            # This is a placeholder, and the actual evaluation will depend on your bet's conditions.
            if bet["type"] == "Spread":
                # Example for Spread
                if game_data['score_home'] + bet['value'] > game_data['score_away']:
                    status_color = "green"
                else:
                    status_color = "red"
            elif bet["type"] == "Over/Under":
                # Example for Over/Under
                if game_data['score_home'] + game_data['score_away'] > bet['value']:
                    status_color = "green"
                else:
                    status_color = "red"
            border_style = "2px solid black"

        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(matchup)
        with col2:
            st.write(f"{bet['type']} {bet['value']}")
        with col3:
            st.markdown(f"<div style='background-color: {status_color}; border: {border_style}; padding: 10px;'>Status</div>", unsafe_allow_html=True)

    st.write("---")  # Separator after each ticket



# st.write("Check Ticket Status")
# if st.button("Check Scores"):
#     for ticket in st.session_state.tickets:
#         matchups = ticket['matchups']
#         for matchup in matchups:
#             team = matchup.split(" vs ")[0]  # Assuming the format "TeamA vs TeamB"
#             try:
#                 game_data = api_client.get_game_data(team=team, week=selected_week)
#                 if game_data:
#                     st.write(f"Match: {game_data['team_home']} vs {game_data['team_away']}")
#                     st.write(f"Score: {game_data['score_home']} - {game_data['score_away']}")
#                 else:
#                     st.warning(f"No game data found for {team} in week {selected_week}.")
#             except Exception as e:
#                 st.error(f"Error: {str(e)}")

st.write("Check Ticket Status")
if st.button("Check Scores"):
    for ticket in st.session_state.tickets:
        for matchup in ticket['matchups']:
            # Assuming each matchup is formatted as "Team1: Team2"
            team1, team2 = matchup.split(": ")
            try:
                game_data = api_client.get_game_data(team=team1) # Modify to accommodate team2 if necessary
                
                if game_data is not None:
                    st.write(f"Debug: {game_data}")  # Debugging line
                    st.write(f"Match: {game_data['team_home']} vs {game_data['team_away']}")
                    st.write(f"Score: {game_data['score_home']} - {game_data['score_away']}")
                    ticket_obj = Ticket(ticket_id="TemporaryID", matchups=ticket['matchups'], bets=ticket['bets']) # Replace "TemporaryID" with an actual ID if available
                    ticket_obj.compute_outcome(game_data) # This updates the status of each bet
                else:
                    st.warning(f"No game data found for {team1} vs {team2}.")
            except Exception as e:
                st.error(f"Error: {str(e)}")


# Debugging: Displaying Teams
# st.write("Matchup Mapping")
# st.write(matchup_mapping)
# st.write("Selected Week")
# st.write(selected_week)
# st.write("Teams")
# st.write(teams)
# st.write("Weeks")
# st.write(weeks)
st.write(st.session_state.tickets)
st.write(f"Debug: {game_data}")
