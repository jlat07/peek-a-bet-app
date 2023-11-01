import unittest
from utils.ticket_manager import TicketManager


class TestPeekABet(unittest.TestCase):

    def setUp(self):
        # This method is called before every test
        self.ticket_manager = TicketManager()

    def test_add_ticket(self):
        matchups = ["Team A vs Team B"]
        bets = [{'type': 'Spread', 'value': '-5'}]

        # Add a ticket and assert that it's added
        self.ticket_manager.add_ticket(matchups, bets)
        self.assertEqual(len(self.ticket_manager.get_all_tickets()), 1)

    def test_change_ticket_order(self):
        matchups = ["Team A vs Team B", "Team C vs Team D"]
        bets = [{'type': 'Spread', 'value': '-5'}, {'type': 'Over/Under', 'value': '50'}]

        # Add two tickets
        self.ticket_manager.add_ticket(matchups[:1], bets[:1])
        self.ticket_manager.add_ticket(matchups[1:], bets[1:])

        # Change the order of the first ticket
        first_ticket_id = self.ticket_manager.get_all_tickets()[0]
        self.ticket_manager.change_ticket_order(first_ticket_id, 1)
        
        # Assert that the ticket is now in the second position
        self.assertEqual(self.ticket_manager.get_all_tickets()[1], first_ticket_id)

    # Add more test cases as necessary

if __name__ == "__main__":
    unittest.main()
