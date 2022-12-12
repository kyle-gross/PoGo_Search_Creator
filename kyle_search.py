from models.search import Search

personal_tags=[
    'Trade', 'Gym', 'Evolve', '98 (-1)', '96 (-2)', '93 (-3)', '91 (-4)', '89 (-5)',
    '87 (-6)', '84 (-7)', '82 (-8)', '80 (-9)', 'Pvp', 'GL', 'UL', 'Mega lvl up', 'Buddy',
    'Event Ev', '0%', 'Best Buddy'
]
search = Search(pvp_top=150, pve_dps_tdo=1250)

# Create transfer str
# search.create_transfer_str()
# with open('transfer2.txt', 'w') as f:
#     f.write(search.transfer_str)

# Create trade str
# search.create_trade_str()
# with open('trade2.txt', 'w') as f:
#     f.write(search.trade_str)

## NEED:
# GL_trade_list
# UL_trade_list
# PVE trade list
# Good potential PVE
search.create_pve_str()
with open('pve_str.txt', 'w') as f:
    f.write(search.pve_str)

# Good potential PVP (UL/GL)
# Potential GL str
search.create_pvp_str(league='GL')
with open('gl_str_potential.txt', 'w') as f:
    f.write(search.gl_str)

# Potential UL str
search.create_pvp_str(league='UL')
with open('ul_str_potential.txt', 'w') as f:
    f.write(search.ul_str)
