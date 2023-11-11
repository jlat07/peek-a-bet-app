import os
import requests
from supabase import create_client, Client
import postgrest

# Initialize Supabase client
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

NFL_API_BASE_URL = os.environ.get("NFL_API_BASE_URL")
NFL_API_KEY = os.environ.get("NFL_API_KEY")

# API Call Values
season_year = 2023  # Eventually you'd want to modify this to be dynamic, for now, it's hardcoded

# Loop through all weeks of the NFL season (assuming 17 weeks for simplicity)
for week in range(1, 18):
    response = requests.get(f"{NFL_API_BASE_URL}/{season_year}REG/{week}", headers={"Ocp-Apim-Subscription-Key": NFL_API_KEY})

    if response.status_code != 200:
        raise Exception(f"API request failed with status {response.status_code}: {response.text}")

    data = response.json()

    for game in data:
        game_id = game["GameID"]
        game_key = game["GameKey"]
        week_number = game["Week"]
        
        # Convert the Date and DateTimeUTC fields to just date and time parts
        date_part = game["Date"].split("T")[0]
        time_part = game["DateTimeUTC"].split("T")[1]

        # Update the ETL process based on the new fields in your table
        try:
            # Checking if the game already exists in the database
            existing_game = supabase.table('games').select('game_id').eq('game_id', game_id).execute()
            
            # If the game exists, we update it with the new information
            if existing_game.data:
                supabase.table('games').update({
                    "home_team": game["HomeTeam"],
                    "away_team": game["AwayTeam"],
                    "home_score": game["HomeScore"],
                    "away_score": game["AwayScore"],
                    "date": date_part,
                    "time": time_part,
                    "status": game["Status"],
                    "quarter": game.get("Quarter"),
                    "time_remaining": game.get("TimeRemaining"),
                    "quarter_description": game.get("QuarterDescription"),
                    "last_updated": game["LastUpdated"],
                    "week": week_number
                }).eq('game_id', game_id).execute()
            else:
                # If the game does not exist, we insert it into the database
                insert_response = supabase.table('games').insert({
                    "game_id": game_id,
                    "game_key": game_key,
                    "home_team": game["HomeTeam"],
                    "away_team": game["AwayTeam"],
                    "home_score": game["HomeScore"],
                    "away_score": game["AwayScore"],
                    "date": date_part,
                    "time": time_part,
                    "status": game["Status"],
                    "quarter": game.get("Quarter"),
                    "time_remaining": game.get("TimeRemaining"),
                    "quarter_description": game.get("QuarterDescription"),
                    "last_updated": game["LastUpdated"],
                    "week": week_number
                }).execute()

                if insert_response.status_code != 201:
                    print(f"Failed to insert data: {insert_response.status_code}")
                    print(f"Response: {insert_response.text}")

        except postgrest.exceptions.APIError as e:
            print(f"An API error occurred: {e.message}, Details: {e.details}, Hint: {e.hint}")
        except Exception as e:
            print(f"An error occurred: {e}")

print("Games table updated successfully!")