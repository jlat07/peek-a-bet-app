# ticket_manager.py

class Ticket:
    def __init__(self, ticket_id, matchups, bets):
        self.ticket_id = ticket_id
        self.matchups = matchups
        self.bets = bets

    def display(self):
        # Dummy method for now
        return f"Ticket ID: {self.ticket_id}, Matchups: {self.matchups}, Bets: {self.bets}"


class TicketManager:
    def __init__(self):
        self.tickets = {}

    def add_ticket(self, matchups, bets):
        ticket_id = len(self.tickets) + 1
        self.tickets[ticket_id] = Ticket(ticket_id, matchups, bets)

    def get_all_tickets(self):
        return self.tickets

    def delete_ticket(self, ticket_id):
        if ticket_id in self.tickets:
            del self.tickets[ticket_id]
