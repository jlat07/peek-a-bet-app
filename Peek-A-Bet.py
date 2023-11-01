# Peek-A-Bet.py

import streamlit as st
from utils.ticket_manager import TicketManager

# Initialize Ticket Manager
ticket_manager = TicketManager()

st.title("Peek-A-Bet")

\
# This is a simplified mapping for demonstration. This should be enhanced based on real data.
matchup_mapping = {
    'Week 1': {'Team A': 'Team B', 'Team C': 'Team D'},
    'Week 2': {'Team A': 'Team C', 'Team B': 'Team D'},
    # ... add more weeks as needed
}


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
    opponent = matchup_mapping[selected_week].get(selected_team, "Unknown")
    temp_matchups.append(f"{selected_team} vs {opponent}")
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
# Peek-A-Bet.py

#... [existing code]

with st.beta_container():
    col1, col2, col3 = st.beta_columns(3)
    
    with col1:
        st.subheader("Ticket ID")
        for ticket_id in ticket_manager.get_all_tickets():
            st.write(ticket_id)

    with col2:
        st.subheader("Ticket Details")
        for ticket in ticket_manager.ordered_tickets():
            st.markdown(f"**Matchups:** {', '.join(ticket.matchups)}")
            st.markdown(f"**Bets:** {', '.join([f'{bet['type']} {bet['value']}' for bet in ticket.bets])}")


    with col3:
        st.subheader("Organize")
        for ticket_id in ticket_manager.get_all_tickets():
            new_position = st.selectbox(f'Position for {ticket_id}, list(range(1, len(ticket_manager.get_all_tickets())+1)), index=ticket_manager.ticket_order.index(ticket_id))
            ticket_manager.change_ticket_order(ticket_id, new_position-1)







# Peek-A-Bet.py

#... [existing code]

total_win = len(ticket_manager.get_all_tickets()) * 100
st.write(f"Total potential win amount: ${total_win}")


# Peek-A-Bet.py

#... [existing code]

selected_week = st.selectbox("Select a Week", list(matchup_mapping.keys()))
teams_for_week = list(matchup_mapping[selected_week].keys())
selected_team = st.selectbox("Select a Team", teams_for_week)
