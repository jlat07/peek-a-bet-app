import os
import requests
from supabase import create_client

# Initialize Supabase client
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Define the API endpoint and key
API_ENDPOINT = "https://api.sportsdata.io/v3/nfl/scores/json/ScoresBasic/2023REG/{week}"
API_KEY = "edadf2ee6ab24f4083fd64606859c27c"

def fetch_and_store_schedule():
    for week in range(1, 19):  # For weeks 1 to 18
        response = requests.get(API_ENDPOINT.format(week=week), params={"key": API_KEY})

        # Ensure the API request was successful
        if response.status_code != 200:
            print(f"Failed to fetch data for week {week}")
            continue

        games = response.json()
        for game in games:
            # Check if game already exists in the database
            existing_game, _ = supabase.table('Games').select().eq('game_id', game['GameID']).execute()
            
            if not existing_game:
                # Insert game details into the Games table
                data = {
                    "game_id": game["GameID"],
                    "team1": game["AwayTeam"],
                    "team2": game["HomeTeam"],
                    "date": game["Date"][:10],  # Extract only the date part
                    "time": game["Date"][11:19],  # Extract only the time part
                }
                supabase.table('Games').insert(data).execute()

fetch_and_store_schedule()
