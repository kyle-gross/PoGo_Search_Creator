from models.search import Search
personal_tags=[
    'Trade', 'Gym', 'Evolve', '98 (-1)', '96 (-2)', '93 (-3)', '91 (-4)', '89 (-5)',
    '87 (-6)', '84 (-7)', '82 (-8)', '80 (-9)', 'Pvp', 'GL', 'UL', 'MEGA', 'Buddy',
    'Event Ev', '0%', 'Best Buddy'
]
search = Search(pvp_top=150, pve_dps_tdo=1250)

search.create_transfer_str()
with open('transfer2.txt', 'w') as f:
    f.write(search.transfer_str)

search.create_trade_str()
with open('trade2.txt', 'w') as f:
    f.write(search.trade_str)
