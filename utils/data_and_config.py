from datetime import date

# Settings
USE_MOCK_DATA = True  # Set to False to use live API data

# Constants
bet_types = ['Spread', 'Over/Under']
spread_values = list(range(-20, 20))
over_under_values = list(range(30, 71))


# Mock data
mock_game_data = {
    'Week 1': {
        'Detroit Lions vs Kansas City Chiefs': {
            'team_home': 'Detroit Lions',
            'score_home': 24,
            'team_away': 'Kansas City Chiefs',
            'score_away': 27
        },
        'Carolina Panthers vs Atlanta Falcons': {
            'team_home': 'Carolina Panthers',
            'score_home': 17,
            'team_away': 'Atlanta Falcons',
            'score_away': 20
        },
        'Houston Texans vs Baltimore Ravens': {
            'team_home': 'Houston Texans',
            'score_home': 14,
            'team_away': 'Baltimore Ravens',
            'score_away': 28
        },
        # ... continue for all matchups ...
        'Dallas Cowboys vs New York Giants': {
            'team_home': 'Dallas Cowboys',
            'score_home': 31,
            'team_away': 'New York Giants',
            'score_away': 17
        },
        'Bills vs Jets': {
            'team_home': 'Bills',
            'score_home': 23,
            'team_away': 'Jets',
            'score_away': 16
        }
    },
}



# Data
matchup_mapping = {
    'Week 1': {
        'teams': {
            'Detroit Lions': 'Kansas City Chiefs',
            'Carolina Panthers': 'Atlanta Falcons',
            'Houston Texans': 'Baltimore Ravens',
            'Cincinnati Bengals': 'Cleveland Browns',
            'Jacksonville Jaguars': 'Indianapolis Colts',
            'Tampa Bay Buccaneers': 'Minnesota Vikings',
            'Tennessee Titans': 'New Orleans Saints',
            'San Francisco 49ers': 'Pittsburgh Steelers',
            'Arizona Cardinals': 'Washington Commanders',
            'Green Bay Packers': 'Chicago Bears',
            'Las Vegas Raiders': 'Denver Broncos',
            'Miami Dolphins': 'Los Angeles Chargers',
            'Philadelphia Eagles': 'New England Patriots',
            'Los Angeles Rams': 'Seattle Seahawks',
            'Dallas Cowboys': 'New York Giants',
            'Bills': 'Jets'
        },
        'dates': (date(2023, 9, 7), date(2023, 9, 11))
    },
    'Week 2': {
        'teams': {
            'Minnesota Vikings': 'Philadelphia Eagles',
            'Green Bay Packers': 'Atlanta Falcons',
            'Las Vegas Raiders': 'Buffalo Bills',
            'Baltimore Ravens': 'Cincinnati Bengals',
            'Seattle Seahawks': 'Detroit Lions',
            'Indianapolis Colts': 'Houston Texans',
            'Kansas City Chiefs': 'Jacksonville Jaguars',
            'Chicago Bears': 'Tampa Bay Buccaneers',
            'Los Angeles Chargers': 'Tennessee Titans',
            'New York Giants': 'Arizona Cardinals',
            'San Francisco 49ers': 'Los Angeles Rams',
            'New York Jets': 'Dallas Cowboys',
            'Washington Commanders': 'Denver Broncos',
            'Miami Dolphins': 'New England Patriots',
            'New Orleans Saints': 'Carolina Panthers',
            'Cleveland Browns': 'Pittsburgh Steelers'
        },
        'dates': (date(2023, 9, 14), date(2023, 9, 18))
    },
    # ... [Add more weeks as needed]
}


weeks = list(matchup_mapping.keys())
teams = list({team for week in matchup_mapping.values() for team in week['teams'].keys()})

