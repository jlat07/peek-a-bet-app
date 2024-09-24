from utils.ticket import Ticket

class TicketManager:
    def __init__(self):
        self.tickets = {}
        self.ticket_order = []

    def add_ticket(self, matchups, bets):
        ticket_id = len(self.tickets) + 1
        new_ticket = Ticket(ticket_id, matchups, bets)
        new_ticket.validate()
        self.tickets[ticket_id] = new_ticket
        self.ticket_order.append(ticket_id)

    def get_ticket(self, ticket_id):
        return self.tickets.get(ticket_id)

    def ordered_tickets(self):
        return [self.tickets[ticket_id] for ticket_id in self.ticket_order]

# from utils.ticket import Ticket

# class TicketManager:
#     def __init__(self):
#         self.tickets = {}
#         self.next_ticket_id = 1
#         self.ticket_order = []
# 
    # def get_all_tickets(self):
    #     return list(self.tickets.keys())

    # def add_ticket(self, matchups, bets):
    #     new_ticket = Ticket(self.next_ticket_id, matchups, bets)
    #     new_ticket.validate()  # Validates the ticket
    #     self.tickets[self.next_ticket_id] = new_ticket
    #     self.ticket_order.append(self.next_ticket_id)
    #     self.next_ticket_id += 1

    # def change_ticket_order(self, ticket_id, new_position):
    #     if ticket_id in self.ticket_order:
    #         # Ensure new_position is within valid range
    #         new_position = min(max(0, new_position), len(self.ticket_order) - 1)
    #         self.ticket_order.remove(ticket_id)
    #         self.ticket_order.insert(new_position, ticket_id)

    # def ordered_tickets(self):
    #     return [self.tickets[ticket_id] for ticket_id in self.ticket_order if ticket_id in self.tickets]

    # def delete_ticket(self, ticket_id):
    #     if ticket_id in self.tickets:
    #         del self.tickets[ticket_id]
    #     if ticket_id in self.ticket_order:
    #         self.ticket_order.remove(ticket_id)