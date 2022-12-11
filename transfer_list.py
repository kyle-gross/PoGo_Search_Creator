import pandas
import json
from legendary_check import legendary_list

TYPE_LIST = [
    'normal', 'fire', 'water', 'grass', 'flying', 'fighting', 'poison',
    'electric', 'ground', 'rock', 'psychic', 'ice', 'bug', 'ghost',
    'steel', 'dragon', 'dark', 'fairy'
]
LEAGUE_LIST = ['GL', 'UL', 'ML']

def get_dex_name(name, dex_names):
    name_list = name.split(' ')
    for name in name_list:
        if name in dex_names:
            return name

def get_full_dex():
    with open('cache/pokemon_names.json', 'r') as f:
        pokemon = json.load(f)
    return set([name[1]['name'] for name in pokemon.items()])

def strip_name(df, dex_names):
    for name in df.Pokemon:
        if name not in dex_names:
            replace = get_dex_name(name, dex_names)
            df['Pokemon'] = df['Pokemon'].replace(name, replace)
    return df

def create_pve_list(top):
    name_list = []
    dex_names = get_full_dex()
    for type in TYPE_LIST:
        df = pandas.read_csv('csv/dps_'+type+'.csv')
        df = df[df['DPS^3*TDO'] > top]

        df = strip_name(df, dex_names)
        df = df.drop_duplicates('Pokemon')
        name_list.extend(df.Pokemon.tolist())

    return name_list

def create_pvp_list(top):
    name_list = []
    dex_names = get_full_dex()
    for league in LEAGUE_LIST:
        df = pandas.read_csv('csv/rankings_'+league+'.csv')
        df = df[:top]
        df = strip_name(df, dex_names)
        df = df.drop_duplicates('Pokemon')
        name_list.extend(df.Pokemon.tolist())
    
    return name_list

def create_list(pvp_top, pve_top):
    pve_list = create_pve_list(pve_top)
    pvp_list = create_pvp_list(pvp_top)
    combined = set(pve_list + pvp_list)
    legendaries = legendary_list()
    for legendary in legendaries:
        if legendary in combined:
            combined.remove(legendary)
    return combined

def transfer(pvp_top, pve_dps_tdo, tag_list):
        # IVs, Shiny, Shadow, Mythical, Legendary, Ultra beast
        search_list = [
            '!4*', 'shiny', 'shadow', 'mythical', 'legendary', 'ultra beast'
        ]
        for tag in tag_list:
            search_list.append(tag)
        search_list = ' &!'.join(search_list)
        pokemon_list = create_list(pvp_top, pve_dps_tdo)
        for pokemon in pokemon_list:
            if pokemon is not None:
                search_list += ' &!+' + pokemon
        return search_list

if __name__ == '__main__':
    search_list = transfer(
        150, 1500, 
        [
            'Trade', 'Gym', 'Evolve', '98 (-1)', '96 (-2)', '93 (-3)', '91 (-4)', '89 (-5)',
            '87 (-6)', '84 (-7)', '82 (-8)', '80 (-9)', 'Pvp', 'GL', 'UL', 'MEGA', 'Buddy', 'Event Ev', '0%'
        ]
    )
    print(len(search_list.split( )))