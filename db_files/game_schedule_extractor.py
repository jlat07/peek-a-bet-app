import json

def transform_data(game_data):
    # Create a list to store the transformed data
    transformed_data = []

    for game in game_data:
        # Check if both 'AwayTeam' and 'HomeTeam' exist in the game record
        if "AwayTeam" not in game or "HomeTeam" not in game:
            continue

        # Skip 'BYE' week games
        if game["AwayTeam"] == "BYE" or game["HomeTeam"] == "BYE":
            continue

        # Replace None with NULL for specific columns
        game["GameID"] = game["GameID"] or "NULL"
        game["Date"] = f"'{game['Date']}'" if game["Date"] else "NULL"
        game["Status"] = f"'{game['Status']}'" if game["Status"] else "NULL"
        game["StadiumID"] = game["StadiumID"] or "NULL"
        game["Season"] = game["Season"] or "NULL"
        game["SeasonType"] = game["SeasonType"] or "NULL"
        game["AwayTeam"] = f"'{game['AwayTeam']}'"
        game["HomeTeam"] = f"'{game['HomeTeam']}'"
        game["Week"] = game["Week"] or "NULL"

        transformed_data.append(game)

    return transformed_data

def generate_sql_statements(transformed_data):
    statements = []
    for game in transformed_data:
        statement = f'''INSERT INTO games (game_id, season, season_type, status, date, away_team, home_team, stadium_id, week)
                        VALUES ({game["GameID"]}, {game["Season"]}, {game["SeasonType"]}, {game["Status"]}, {game["Date"]}, {game["AwayTeam"]}, {game["HomeTeam"]}, {game["StadiumID"]}, {game["Week"]});'''
        statements.append(statement)

    return statements


def generate_sql_statements(transformed_data):
    statements = []
    for game in transformed_data:
        statement = f'''INSERT INTO games (game_id, season, season_type, status, date, away_team, home_team, stadium_id, week)
                        VALUES ({game["GameID"]}, {game["Season"]}, {game["SeasonType"]}, {game["Status"]}, {game["Date"]}, {game["AwayTeam"]}, {game["HomeTeam"]}, {game["StadiumID"]}, {game["Week"]});'''
        statements.append(statement)
    print(statements[:5])  # print first 5 SQL statements
    return statements


if __name__ == "__main__":
    # Load the JSON data
    with open("games.json", "r") as file:
        game_data = json.load(file)
        print(game_data[:5])  # print first 5 records for a quick check
    
    # Transform the data
    transformed_data = transform_data(game_data)
    print(transformed_data[:5])  # print first 5 transformed records
    
    # Generate SQL statements
    sql_statements = generate_sql_statements(transformed_data)

    # Save or print the SQL statements
    with open("insert_statements.sql", "w") as output_file:
        for statement in sql_statements:
            output_file.write(statement + "\n")
