def group_grenades_by_player(all_grenades, players):
    result = {}
    for player in players:
        grenades = [x for x in all_grenades if x.thrower is not None and player == x.thrower]
        result[player] = grenades
    return result
