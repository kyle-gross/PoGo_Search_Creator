import pandas as pd
import json


class Search:

    type_list = [
        'normal', 'fire', 'water', 'grass', 'flying', 'fighting', 'poison',
        'electric', 'ground', 'rock', 'psychic', 'ice', 'bug', 'ghost',
        'steel', 'dragon', 'dark', 'fairy'
    ]
    league_list = ['GL', 'UL', 'ML']

    def __init__(self, pvp_top, pve_dps_tdo, personal_tags=[]):
        self.pvp_top = pvp_top
        self.pve_dps_tdo = pve_dps_tdo
        self.transfer_list = ['!4*', 'shiny', 'shadow', 'mythical', 'legendary', 'ultra beast', '@special']
        self.trade_list = ['!4*', 'shiny', 'shadow', 'traded', 'mythical']
        self.pvp_list = ['0attack,1attack', '2-3defense', '2-3hp', 'cp-1500']
        self.pve_list = ['4*', '3*']
        self.personal_tags = personal_tags
        self.transfer_str = ''
        self.trade_str = ''
        self.gl_str = ''
        self.ul_str = ''
        self.ml_str = ''
        self.pve_str = ''
        self.dex_names = self.get_full_dex()

    ### Search string generators ###
    def create_transfer_str(self):
        self.transfer_str = ' &!'.join(self.transfer_list)
        if self.personal_tags:
            self.transfer_str += ' &!'
            self.transfer_str += ' &!'.join(self.personal_tags)
        transfer_list = self.create_transfer_list()
        for pokemon in transfer_list:
            if pokemon is not None:
                self.transfer_str += ' &!+' + pokemon

    def create_trade_str(self):
        self.trade_str = ' &!'.join(self.trade_list)
        if self.personal_tags:
            self.trade_str += ' &!'
            self.trade_str += ' &!'.join(self.personal_tags)
        trade_list = self.create_trade_list()
        for pokemon in trade_list:
            if pokemon is not None:
                self.trade_str += ', +' + pokemon

    def create_pve_str(self):
        self.pve_str = ', '.join(self.pve_list) + ', '
        self.pve_str += ', '.join(self.create_pve_pvp_list(type='pve'))
    
    def create_pvp_str(self, league=None):
        if league is None:
            raise ValueError('Please specify a league value (\'GL\' or \'UL\'')
        if league not in ['GL', 'UL']:
            raise ValueError('Incorrect league. Please specify: \'GL\' or \'UL\'')
        league_list = self.create_pve_pvp_list(type='pvp', league=league)
        if league == 'GL':
            self.gl_str = ' &'.join(self.pvp_list) + ', '
            self.gl_str += ', +'.join(league_list)
        if league == 'UL':
            self.ul_str = ' &'.join(self.pvp_list) + ', '
            self.ul_str += ', +'.join(league_list)

    ### List generators ###
    def create_pve_pvp_list(self, type, league=None):
        if type == None:
            raise ValueError('Please specify \"pve\" or \"pvp\"')
        pkmn_list = []
        if type == 'pve':
            for type in Search.type_list:
                df = self.get_pve_data(type)
                pkmn_list.extend(df.Pokemon.tolist())
        if type == 'pvp':
            if league == None:
                for league in Search.league_list:
                    df = self.get_pvp_data(league)
                    pkmn_list.extend(df.Pokemon.tolist())
            else:
                df = self.get_pvp_data(league)
                pkmn_list.extend(df.Pokemon.to_list())
        return pkmn_list

    def create_transfer_list(self):
        pve_list = self.create_pve_pvp_list(type='pve')
        pvp_list = self.create_pve_pvp_list(type='pvp')
        combined = self.remove_legendaries(set(pve_list + pvp_list))
        return combined

    def create_trade_list(self):
        pve_list = self.create_pve_pvp_list(type='pve')
        pvp_list = self.create_pve_pvp_list(type='pvp')
        combined = self.remove_legendaries(
            set(pve_list + pvp_list), legendary=False, ultra_beast=False
        )
        return combined

    ### Process data ###
    def get_pvp_data(self, league):
        df = pd.read_csv('cache/csv/rankings_' + league + '.csv')
        df = df[:self.pvp_top]
        df = self.strip_name(df)
        df = df.drop_duplicates('Pokemon')
        return df

    def get_pve_data(self, type):
        df = pd.read_csv('cache/csv/dps_' + type + '.csv')
        df = df[df['DPS^3*TDO'] > self.pve_dps_tdo]
        df = self.strip_name(df)
        df = df.drop_duplicates('Pokemon')
        return df
    
    def strip_name(self, df):
        for name in df.Pokemon:
            if name not in self.dex_names:
                replace = self.get_dex_name(name)
                if replace is not None:
                    df['Pokemon'] = df['Pokemon'].replace(name, replace)
        return df

    def remove_legendaries(self, pkmn_list, legendary=True, mythical=True, ultra_beast=True):
        lg_list = []
        if legendary == True:
            lg_list += self.get_legendary_data('Legendary')
        if mythical == True:
            lg_list += self.get_legendary_data('Mythic')
        if ultra_beast == True:
            lg_list += self.get_legendary_data('Ultra beast')
        lg_list = set(lg_list)

        for legendary in lg_list:
            if legendary in pkmn_list:
                pkmn_list.remove(legendary)

        return pkmn_list

    def get_legendary_data(self, type):
        pkmn_list = []
        with open('cache/json/pokemon_rarity.json', 'r') as f:
            data = json.load(f)
        df = self.transpose_data(data)
        df = pd.DataFrame(df[type])
        new_df = pd.DataFrame(df)
        for pkmn in df[type]:
            if pkmn is not None:
                new_df = self.transpose_data(pkmn)
                pkmn_list.append(new_df['pokemon_name'].values[0])
        return pkmn_list

    @staticmethod
    def transpose_data(data):
        df = pd.DataFrame.from_dict(data, orient='index')
        return df.T

    ### Pokedex functions ###
    @staticmethod
    def get_full_dex():
        with open('cache/json/pokemon_names.json', 'r') as f:
            pokemon = json.load(f)
        return set([name[1]['name'] for name in pokemon.items()])

    def get_dex_name(self, name):
        '''Removes excess words from pokemon name (Shadow, Alolan, etc.)'''
        name_list = name.split(' ')
        for name in name_list:
            if name in self.dex_names:
                return name
        return None
