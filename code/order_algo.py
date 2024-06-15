def determine_washing_order(players):
    # Calculate the average gameCounter
    average_games = sum(player['gameCounter'] for player in players) / len(players)
    
    # Identify players who should be considered active
    active_players = [player for player in players if player['gameCounter'] >= 0.75 * average_games]
    
    # Sort active players by 'washed' (ascending) and 'gameCounter' (descending) in case of ties
    sorted_active_players = sorted(active_players, key=lambda p: (p['washed'], -p['gameCounter']))
    
    # Assign the order for active players
    for idx, player in enumerate(sorted_active_players):
        player['order'] = idx + 1
    
    # Assign 'inactive' for players who are not active
    for player in players:
        if player not in sorted_active_players:
            player['order'] = 'inactive'
    if not players:
        raise ValueError("Something Went Wrong While Calculating The Washing Order---- ERROR ERROR ERROR----")
    return players