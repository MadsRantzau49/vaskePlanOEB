from excel import *
from games import *
from order_algo import *

def sortObject(list,object):
    sorted_list = sorted(list, key=lambda x: x[object])
    return sorted_list



print("Starting Extracting Data From the Excel File")

excelFile = "vaskePlan.xlsx"
matchfile = "kampe.txt"

gameList = matches_to_lists(matchfile)

playerListDatabase = extract_excel(excelFile)
sortedPlayerListDatabase = sortObject(playerListDatabase,"washed")
for p in sortedPlayerListDatabase:
    print(p["washed"], " Times Washed. Name:", p["name"])

print("Start Finding All Players Based On the Matches Provided In kampe.txt")

for game in gameList:
    print(game,"Successfully Scraped Data")
    try:
        gameLinup = find_game_lineup(game)
        oebLinup = findOebLineup(gameLinup)
        playerListDatabase = appendUniquePlayer(oebLinup,playerListDatabase)
    except ValueError as e:
        print(game,e)

try:
    fair_player_list = determine_washing_order(playerListDatabase)
    update_excel(fair_player_list,excelFile)
    print("The Data Is Succesfully Updated In The VaskePlan.xlsx file")
except ValueError as e:
    print(e)

active_player_list = []
for player in fair_player_list:
        if isinstance(player["order"], int):
            active_player_list.append(player)

sorted_players = sortObject(active_player_list,"order")

print("\n\nHere Is The Most Fair List\n")
for player in sorted_players:
    print(player["order"], player["name"])


input("Press Enter to exit...")