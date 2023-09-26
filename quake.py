with open('qgames.log', 'r') as file:
    rows = list(file)

death_causes = {
    "MOD_UNKNOWN",
    "MOD_SHOTGUN",
    "MOD_GAUNTLET",
    "MOD_MACHINEGUN",
    "MOD_GRENADE",
    "MOD_GRENADE_SPLASH",
    "MOD_ROCKET",
    "MOD_ROCKET_SPLASH",
    "MOD_PLASMA",
    "MOD_PLASMA_SPLASH",
    "MOD_RAILGUN",
    "MOD_LIGHTNING",
    "MOD_BFG",
    "MOD_BFG_SPLASH",
    "MOD_WATER",
    "MOD_SLIME",
    "MOD_LAVA",
    "MOD_CRUSH",
    "MOD_TELEFRAG",
    "MOD_FALLING",
    "MOD_SUICIDE",
    "MOD_TARGET_LASER",
    "MOD_TRIGGER_HURT",
    "MOD_NAIL",
    "MOD_CHAINGUN",
    "MOD_PROXIMITY_MINE",
    "MOD_KAMIKAZE",
    "MOD_JUICED",
    "MOD_GRAPPLE"
}

games = {}
count_games = 0
for line in rows:
    line = line[7:].strip()
    if line.startswith('InitGame:'):
        count_games+=1
        games[f'games_{count_games}'] = {
            'total_kills' : 0,
            'players' : set(),
            'kills' : {},
            'kills_by_means' : {cause: 0 for cause in death_causes}
        }

    if line.startswith('Kill:'):
        line = line.split(": ")[-1]
        splitted_line = line.split(' killed ')
        killer = splitted_line[0]
        killed, mod = splitted_line[1].split(' by ')
        games[f'games_{count_games}']['players'].add(killed)
        games[f'games_{count_games}']['total_kills'] +=1
        if killer == '<world>':
            games[f'games_{count_games}']['kills'][killed] = games[f'games_{count_games}']['kills'].get(killed, 0) - 1
        else:
            games[f'games_{count_games}']['kills'][killer] = games[f'games_{count_games}']['kills'].get(killer, 0) + 1
        games[f'games_{count_games}']['kills_by_means'][mod] +=1

for game in games:
    games[game]['players'] = list(games[game]['players'])
    games[game]['kills_by_means'] = dict(sorted(games[game]['kills_by_means'].items(), key=lambda item: -item[1]))

import json

with open('report.json', 'w') as file:
    json.dump(games, file, indent=4)
  