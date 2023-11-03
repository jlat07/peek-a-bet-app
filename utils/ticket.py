class Ticket:
    def __init__(self, ticket_id, matchups, bets):
        self.ticket_id = ticket_id
        self.matchups = matchups
        self.bets = bets

    def display(self):
        bet_str = ', '.join([f"{bet['type']} {bet['value']}" for bet in self.bets])
        return f"Ticket ID: {self.ticket_id}\nMatchups: {', '.join(self.matchups)}\nBets: {bet_str}"

    def validate(self):
        if not self.matchups:
            raise ValueError("Matchups should not be empty!")
        if not self.bets:
            raise ValueError("Bets should not be empty!")
        # Add other validation rules if necessary

    def compute_outcome(self, game_data):
        for bet in self.bets:
            bet_type = bet["type"]
            bet_value = float(bet["value"])
            
            if game_data["score_home"] == 0 and game_data["score_away"] == 0:
                bet["status"] = "pending"
                continue
            
            if bet_type == "spread":
                if self.matchups[0] == game_data["team_home"]:
                    delta = game_data["score_home"] - game_data["score_away"] + bet_value
                else:
                    delta = game_data["score_away"] - game_data["score_home"] - bet_value

                bet["delta"] = delta
                bet["status"] = "win" if delta > 0 else "lose"

            elif bet_type == "over_under":
                total_score = game_data["score_home"] + game_data["score_away"]
                delta = total_score - bet_value

                bet["delta"] = delta
                bet["status"] = "win" if (delta > 0 and bet_value == "over") or (delta < 0 and bet_value == "under") else "lose"
