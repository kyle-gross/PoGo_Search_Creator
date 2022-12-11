import requests
import json


def get_request(url : str):
    r = requests.get(url)
    file_name = get_file_name(url)
    return json.loads(r.text), file_name

def get_file_name(url):
    return url.split('/')[-1]

def save(data, file_name):
    with open(file_name, 'w') as f:
        json.dump(data, f)

if __name__ == '__main__':
    main_url = 'https://pogoapi.net/api/v1/'
    paths = [
        'pokemon_names.json', 'released_pokemon.json', 'nesting_pokemon.json',
        'shiny_pokemon.json', 'raid_exclusive_pokemon.json', 'alolan_pokemon.json',
        'possible_ditto_pokemon.json', 'pokemon_stats.json', 'fast_moves.json',
        'charged_moves.json', 'pokemon_max_cp.json', 'pokemon_buddy_distances.json',
        'pokemon_candy_to_evolve.json', 'pokemon_encounter_data.json', 'pokemon_types.json',
        'weather_boosts.json', 'type_effectiveness.json', 'pokemon_rarity.json',
        'pokemon_powerup_requirements.json', 'pokemon_genders.json', 'player_xp_requirements.json',
        'pokemon_generations.json', 'shadow_pokemon.json', 'pokemon_forms.json',
        'current_pokemon_moves.json', 'pvp_exclusive_pokemon.json', 'galarian_pokemon.json',
        'cp_multiplier.json', 'community_days.json', 'pokemon_evolutions.json',
        'raid_bosses.json', 'research_task_exclusive_pokemon.json', 'mega_pokemon.json',
        'pokemon_height_weight_scale.json', 'levelup_rewards.json', 'badges.json',
        'gobattle_league_rewards.json', 'raid_settings.json', 'mega_evolution_settings.json',
        'friendship_level_settings.json', 'gobattle_ranking_settings.json', 'baby_pokemon.json',
        'pvp_fast_moves.json', 'pvp_charged_moves.json', 'time_limited_shiny_pokemon.json',
        'photobomb_exclusive_pokemon.json'

    ]
    for path in paths:
        response, file_name = get_request(main_url + path)
        save(response, 'cache/json/' + file_name)
