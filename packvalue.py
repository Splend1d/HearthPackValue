import random
# stats taken from https://hearthstone.gamepedia.com/Card_pack_statistics
_prob = {'common': 0.6998, 'rare': 0.2174, 'epic': 0.041, 'legendary': 0.0087,
         'golden_common': 0.0165, 'golden_rare': 0.0132, 'golden_epic': 0.0027,
         'golden_legendary': 0.0013}
# first ten packs are assumed to have twice the chance of getting a legendary/golden legendary
_prob_first_10 = {'common': 0.6927, 'rare': 0.2152, 'epic': 0.0406, 'legendary': 0.0174,
                  'golden_common': 0.0163, 'golden_rare': 0.01306, 'golden_epic': 0.00267, 'golden_legendary': 0.0026}

# different cards in a set
_varies = {'common': 49, 'rare': 36, 'epic': 27, 'legendary': 23}
# value of disenchanting
_dust_value = {'common': 5, 'rare': 20, 'epic': 100, 'legendary': 400,
               'golden_common': 50, 'golden_rare': 100, 'golden_epic': 400, 'golden_legendary': 1600}
# value of crafting
_craft_value = {'common': 40, 'rare': 100, 'epic': 400, 'legendary': 1600,
                'golden_common': 400, 'golden_rare': 800, 'golden_epic': 1600, 'golden_legendary': 6400}
# weighted percent of value of disenchanting considering golden

_weighted_dust_value = {'common': 0.977 * 5 + 0.023 * 50,
                        'rare': 0.9423 * 20 + 0.0567 * 100,
                        'epic': 0.9382 * 100 + 0.0618 * 400,
                        'legendary': 0.87 * 400 + 0.13 * 1600}


def openpacks(x):
    x = 5 * x
    out = {}
    if x >= 50:
        for k in _prob.keys():
            out[k] = _prob[k] * (x - 50) + _prob_first_10[k] * 50
        #print('avg_cards:', out)
        return out
    elif x >= 0:
        for k in _prob.keys():
            out[k] = _prob_first_10[k] * x
        #print('expected_cards:', out)
        return out
# uses a random assign model to calculate the expectated duplicates


def Nongold(cards):
    nongold = {'common': cards['common'] + cards['golden_common'],
               'rare': cards['rare'] + cards['golden_rare'],
               'epic': cards['epic'] + cards['golden_epic'],
               'legendary': cards['legendary'] + cards['golden_legendary']}

    return nongold


def card_assigner(cards):
    extra = {'common': 0, 'rare': 0, 'epic': 0, 'legendary': 0}
    usable = {'common': 0, 'rare': 0, 'epic': 0, 'legendary': 0}
    for n in range(10000):
        for k in list(cards.keys())[:-1]:
            collection_rarity = {}
            for x in range(int(cards[k]) + 1):
                this_card = random.randrange(0, _varies[k])
                try:
                    collection_rarity[this_card] += 1
                    if collection_rarity[this_card] >= 3:
                        if x == int(cards[k]):
                            extra[k] += cards[k] - int(cards[k])
                        else:
                            extra[k] += 1
                except:
                    collection_rarity[this_card] = 1
    for k in extra.keys():
        extra[k] /= 10000
        if k == 'legendary':
            usable[k] = min((cards[k] - extra[k]), _varies[k])
            break
        usable[k] = min((cards[k] - extra[k]), 2 * _varies[k])
    #print('avg collection usable:', usable)
    return usable


def packvalue(x):
    cards1 = Nongold(openpacks(x - 1))
    cards2 = Nongold(openpacks(x))
    u1 = card_assigner(cards1)
    u2 = card_assigner(cards2)
    diff = {'common': 0, 'rare': 0, 'epic': 0, 'legendary': 0}

    # the worth of ith pack is calculated by the formula
    # non duplicate cards * craft value + duplicate cards * disenchant value
    # in the ith pack
    worth = 0
    for k in u1:
        diff[k] = u2[k] - u1[k]
        worth += diff[k] * _craft_value[k] + (cards2[k] - cards1[k] - diff[k]) * _weighted_dust_value[k]
    print('worth:', worth)


# calculates the dust value of the ith pack
packvalue(100)
