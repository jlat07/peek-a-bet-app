# ticket_manager.py

class Ticket:
    def __init__(self, ticket_id, matchups, bets):
        self.ticket_id = ticket_id
        self.matchups = matchups
        self.bets = bets

    def display(self):
        # Convert bets to a string representation
        bet_str = ', '.join([f"{bet['type']} {bet['value']}" for bet in self.bets])
        return f"Ticket ID: {self.ticket_id}\nMatchups: {', '.join(self.matchups)}\nBets: {bet_str}"


# ticket_manager.py

class TicketManager:
    def __init__(self):
        self.tickets = {}
        self.next_ticket_id = 1
        self.ticket_order = []  # To keep track of ticket order

    def get_all_tickets(self):
        return list(self.tickets.keys())


    def add_ticket(self, matchups, bets):
        ticket = Ticket(self.next_ticket_id, matchups, bets)
        self.tickets[self.next_ticket_id] = ticket
        self.ticket_order.append(self.next_ticket_id)
        self.next_ticket_id += 1

    #... [other methods]

    def change_ticket_order(self, ticket_id, new_position):
        self.ticket_order.remove(ticket_id)
        self.ticket_order.insert(new_position, ticket_id)

    def ordered_tickets(self):
        return [self.tickets[ticket_id] for ticket_id in self.ticket_order]
