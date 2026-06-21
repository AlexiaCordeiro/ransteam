import argparse
import random
import requests
import os
from dotenv import load_dotenv

load_dotenv()
STEAM_KEY = os.getenv('STEAM_KEY')

if not STEAM_KEY:
    print("ERRO: Você precisa definir sua própria STEAM_KEY no arquivo .env")
    print("Siga as instruções no README para criar a sua chave.")
    exit(1)

FORMAT = 'xml'
INTERFACE_NAME = 'GetOwnedGames/v0001' #Returns a list of games a player owns along with some playtime information, if the profile is publicly visible
PARAMETER = {
    'include_appinfo': 'true'
} 
parser = argparse.ArgumentParser(
                    prog='RANSTEAM',
                    description='Get a random game from a Steam user\'s library',
                    )

parser.add_argument('--steamid', '-s', help='Steam ID of the user')
parser.add_argument('--most-played', '-m', help='Get the most played game from the user\'s library', action='store_true')
parser.add_argument('--least-played', '-l', help='Get the least played game from the user\'s library', action='store_true')
args = parser.parse_args()
STEAM_ID = args.steamid

#Example URL: https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=XXXXXXXXXXXXXXXXX&steamid=76561197960434622&format=json
response = requests.get(f'http://api.steampowered.com/IPlayerService/{INTERFACE_NAME}/?key={STEAM_KEY}&steamid={STEAM_ID}&format={FORMAT}', 
                 params=PARAMETER,
                 headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}, 
                 )
response.raise_for_status()

game = {}
current_appid = None
sum = 0
for line in response.text.splitlines():
    line = line.strip()
    
    if '<appid>' in line:
        appid = line.replace('<appid>', '').replace('</appid>', '').strip()
        game[appid] = {}
        current_appid = appid
        
    elif current_appid is not None and '<name>' in line:
        name = line.replace('<name>', '').replace('</name>', '').strip()
        game[current_appid]['name'] = name
        
    elif current_appid is not None and '<playtime_forever>' in line:
        playtime = int(line.replace('<playtime_forever>', '').replace('</playtime_forever>', '').strip())
        game[current_appid]['playtime'] = playtime
        sum += playtime

def get_rand_time(condition=None):
    if condition:
        choice = [values for values in game.values() if condition(values['playtime'])]
    elif condition is None:
        choice = game.values()

    return random.choice(list(choice))

mean = sum/len(game)

if args.least_played:
    print(f"Getting random game from least hours played.")
    rand_game = get_rand_time(lambda played: played <= mean)
elif args.most_played:
    print(f"Getting random game from most hours played.")
    rand_game = get_rand_time(lambda played: played > mean)
else:
    print(f"Getting random game.")
    rand_game = get_rand_time()

if rand_game:
    print(f"Random game: {rand_game['name']} with {rand_game['playtime']} minutes played")
