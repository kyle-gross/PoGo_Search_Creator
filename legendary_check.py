import pandas as pd
import json

def get_list(type):
    with open('cache/pokemon_rarity.json', 'r') as f:
        data = json.load(f)
    df = pd.DataFrame.from_dict(data, orient='index')
    df = df.T
    df = pd.DataFrame(df[type])
    new_df = pd.DataFrame(df)
    names = []
    for row in df[type]:
        if row is not None:
            new_df = pd.DataFrame.from_dict(row, orient='index')
            new_df = new_df.T
            names.append(new_df['pokemon_name'].values[0])
    return names

def legendary_list():
    names = []
    names += get_list('Legendary')
    names += get_list('Mythic')
    names += get_list('Ultra beast')
    return set(names)
