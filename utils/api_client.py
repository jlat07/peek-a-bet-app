import requests

class APIClient:
    def __init__(self, api_key, base_url="https://api.sportsopendata.net/v1/nfl"):
        self.api_key = api_key
        self.base_url = base_url

    def get_game_data(self, team, week):
        try:
            # Construct the endpoint URL
            endpoint_url = f"{self.base_url}/seasons/2023/weeks/{week}/events"
            headers = {
                "Authorization": f"Bearer {self.api_key}"
            }

            # Make the API call
            response = requests.get(endpoint_url, headers=headers)
            response.raise_for_status() 

            data = response.json()

            # Extract the game data for the specified team
            for match in data["events"]:
                if match["team_home"]["name"] == team or match["team_away"]["name"] == team:
                    return {
                        "team_home": match["team_home"]["name"],
                        "team_away": match["team_away"]["name"],
                        "score_home": match["result"]["score_home"],
                        "score_away": match["result"]["score_away"],
                    }
            return None 

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

