from bs4 import BeautifulSoup
import requests
import re

def matches_to_lists(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            string_lists = [line.strip() for line in lines]
            return string_lists
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return []


#Webscrape the player list from DBU webiste
def find_game_lineup(match_id):
    team_lineup_url = "https://www.dbu.dk/resultater/kamp/" + match_id +"/kampinfo"

    #request html code from dbu.dk
    team_lineup_html_request = requests.get(team_lineup_url)
    
    # Parse HTML using BeautifulSoup
    soup = BeautifulSoup(team_lineup_html_request.text, 'html.parser')

    # Find all team lineup information
    team_lineup_info = soup.find_all("div", {"class": "sr--match--team-cards dbu-grid"})
    if not team_lineup_info:
        raise ValueError("Match Not Found")
    
    # Extract text from HTML elements
    team_lineup_text = [info.get_text() for info in team_lineup_info]
    team_lineup_text_string = ""
    for elements in team_lineup_text:
        team_lineup_text_string += elements
    
    team_lineup_text_string = re.sub(r'\n\s*\n', '\n', team_lineup_text_string).strip()

    return team_lineup_text_string


def findOebLineup(gameLinup):
    gameLinupList =gameLinup.strip().split("\n")
    players = []
    savePlayer = False
    for e in gameLinupList:
        if savePlayer:
            if "Officials" in e:
                break
            else:
                players.append(e)

        if "Øster Sundby" in e:
            savePlayer = True
            
    # Extract players if the pattern is found
    if players:
        return players
    else:
        raise ValueError("No players found")


def appendUniquePlayer(playerList, playerListDatabase):
    for player in playerList:
        player_exists = False
        for existingPlayer in playerListDatabase:
            if existingPlayer["name"] == player:
                existingPlayer["gameCounter"] += 1
                player_exists = True
                break
        if not player_exists:
            playerListDatabase.append({"name": player, "gameCounter": 1, "washed": 0, "order":None})
    return playerListDatabase

