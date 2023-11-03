import requests
from urllib.parse import quote
from utils.data_and_config import USE_MOCK_DATA, MOCK_GAME_DATA

class APIClient:
    def __init__(self, api_key, base_url="https://api.sportsopendata.net/v1/nfl"):
        self.api_key = api_key
        self.base_url = base_url

    def get_game_data(self, team, week):
        try:
            if USE_MOCK_DATA:
                return MOCK_GAME_DATA

            # Construct the endpoint URL with URL encoding for the week
            endpoint_url = f"{self.base_url}/seasons/2023/weeks/{quote(week)}/events"
            headers = {
                "Authorization": f"Bearer {self.api_key}"
            }

            # Make the API call
            response = requests.get(endpoint_url, headers=headers)
            response.raise_for_status()

            data = response.json()

            # Ensure the "events" key is in the response
            if "events" not in data:
                raise ValueError("Invalid API response format: 'events' key missing.")

            # Extract the game data for the specified team
            for match in data["events"]:
                if match["team_home"]["name"] == team or match["team_away"]["name"] == team:
                    return {
                        "team_home": match["team_home"]["name"],
                        "team_away": match["team_away"]["name"],
                        "score_home": match["result"]["score_home"],
                        "score_away": match["result"]["score_away"],
                    }
            else:
                raise ValueError(f"No match found for team {team} in week {week}.")

        except requests.ConnectionError:
            # Handle connection errors
            raise ConnectionError("Failed to connect to the API. Please check your internet connection and try again.")

        except requests.Timeout:
            # Handle request timeout errors
            raise TimeoutError("The request to the API timed out. Please try again later.")

        except requests.RequestException as e:
            # Handle other request-related errors
            raise Exception(f"An error occurred while fetching data from the API: {str(e)}")

        except ValueError as e:
            # Handle issues related to the data format or content
            raise ValueError(f"Data extraction error: {str(e)}")

