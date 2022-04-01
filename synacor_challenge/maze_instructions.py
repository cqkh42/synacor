import itertools


COIN_VALUES = {
    9: 'blue',
    2: 'red',
    5: 'shiny',
    3: 'corroded',
    7: 'concave'
}

for a, b, c, d, e in itertools.permutations(COIN_VALUES):
    if a + (b*c**2) + d**3 - e == 399:
        coin_order = [COIN_VALUES[coin] for coin in [a,b,c,d,e]]
        coin_strings = [f'use {coin} coin' for coin in coin_order]
        break

instructions = list('\n'.join([
    'take tablet',
    'use tablet',
    'doorway',
    'north',
    'north',
    'bridge',
    'continue',
    'down',
    'east',
    'take empty lantern',
    'west',
    'west',
    'passage',
    'ladder',
    'west',
    'south',
    'north',
    'take can',
    'use can',
    'use lantern',
    'west',
    'ladder',
    'darkness',
    'continue',
    'west',
    'west',
    'west',
    'west',
    'north',
    'take red coin',
    'north',
    'east',
    'take concave coin',
    'down',
    'take corroded coin',
    'up',
    'west',
    'west',
    'take blue coin',
    'up',
    'take shiny coin',
    'down',
    'east',
    *coin_strings,
    'north',
    'take teleporter',
    'use teleporter',
    'take business card',
    'take strange book',
    'look strange book',
    'use teleporter'
]) + '\n')