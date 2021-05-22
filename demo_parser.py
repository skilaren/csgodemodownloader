import datetime

from maps import map_mappings
from match import Rounds
from grenades import Flash, HE, Smoke
from match_info import MatchInfo

CT_TEAM = 3
T_TEAM = 2

EVENT_FLASHED = 'flashed'
EVENT_ROUND_ENDED = 'round_ended'
EVENT_ROUND_START = 'round_started'
EVENT_MATCH_START = 'match_started'
EVENT_GAME_PHASE_CHANGED = 'game_phase_changed'
EVENT_GRENADE_DESTROY = 'grenade_destroy'
EVENT_HURT = 'hurt'

EQUIP_MOLOTOV = 502
EQUIP_FLASH = 504
EQUIP_SMOKE = 505
EQUIP_HE = 506

NADE_POINT_RADIUS = 5
SMOKE_POINT_RADIUS = 20


def points_trajectory_to_tuples(trajectory):
    result = []
    for point in trajectory:
        result.append((point['x'], point['y']))
    return result


def get_players(dem):
    players = {}

    for player in dem['entities']:
        players[player['id']] = {}
        players[player['id']]['name'] = player['name']
        players[player['id']]['team'] = player['team']

    return players


def get_he_grenades(dem):
    """
    Get all HE grenades that were thrown in this match and necessary parameter of them

    NOTE: GRENADE DESTROY EVENT happens after 256 ticks for 64 tick demo after HURT EVENT for whatever reason, this
    method initially developed only for 64 tick demos so may need adjustments for other tick rates

    :param dem: json file of demo
    :return: list of all grenades
    """

    # Make set of players
    players = get_players(dem)

    events_ticks = dem['ticks']

    rounds = Rounds()
    grenades = []
    # Track the he nades
    last_nade = HE(0, False, [], 0, 0)
    for tick in events_ticks:
        for event in tick['events']:
            # Event when a grenade entity is destroyed
            # It contains trajectory and information about player who threw the nade
            if event['name'] == EVENT_GRENADE_DESTROY:
                attrs_array = event['attrs']
                attrs = {}
                for attr in attrs_array:
                    if attr['key'] == 'trajectory':
                        attrs[attr['key']] = attr['trajectory']
                    else:
                        attrs[attr['key']] = attr['numVal']
                if attrs['weapon'] == EQUIP_HE:
                    last_nade.thrower = attrs.get('player')
                    # last_nade.trajectory = attrs['trajectory']
                    last_nade.g_round = rounds.sum() + 1
                    grenades.append(last_nade)
                    last_nade = HE(0, False, [], 0, 0)

            # Event when some player is hurt
            # Used to track effectiveness of HE grenade
            if event['name'] == EVENT_HURT:
                attrs_array = event['attrs']
                attrs = {}
                for attr in attrs_array:
                    if 'numVal' in attr:
                        attrs[attr['key']] = attr['numVal']
                    else:
                        attrs[attr['key']] = 0

                if attrs['weapon'] == EQUIP_HE:
                    thrower = attrs['attacker']
                    last_nade.unique_id = attrs['entityId']
                    # HE grenade is effective if it hurts enemies' team player
                    if 'player' in attrs and thrower is not None and thrower != 0 \
                            and players[thrower]['team'] != players[attrs['player']]['team']:
                        last_nade.add_damage(attrs['health_damage'])
                        last_nade.effective = True

            # Event of ended round to track flashbangs by round
            if event['name'] == EVENT_ROUND_ENDED:
                attrs_array = event['attrs']
                attrs = {}
                for attr in attrs_array:
                    attrs[attr['key']] = attr['numVal']

                rounds.round_end(attrs['winner'])

    return grenades, players


def get_flashes(dem):

    # Make set of players
    players = get_players(dem)

    events_ticks = dem['ticks']

    rounds = Rounds()
    flashes = []

    # Track the flashes
    for tick in events_ticks:
        last_flash = Flash(0, False, [], 0)
        flash_existed = False
        for event in tick['events']:
            # Event when a grenade entity is destroyed
            # It contains trajectory and information about player who threw the nade
            if event['name'] == EVENT_GRENADE_DESTROY:
                attrs_array = event['attrs']
                attrs = {}
                for attr in attrs_array:
                    if attr['key'] == 'trajectory':
                        attrs[attr['key']] = attr['trajectory']
                        attrs[attr['key']] = attr['trajectory']
                    else:
                        attrs[attr['key']] = attr['numVal']
                if attrs['weapon'] == EQUIP_FLASH:
                    flash_existed = True
                    last_flash.thrower = attrs.get('player')
                    # last_flash.trajectory = attrs['trajectory']
                    last_flash.g_round = rounds.sum() + 1

            # Event when some player is flashed
            # Used to track effectiveness of flash grenade
            if event['name'] == EVENT_FLASHED:
                attrs_array = event['attrs']
                attrs = {}
                for attr in attrs_array:
                    attrs[attr['key']] = attr['numVal']

                thrower = last_flash.thrower
                # Flash is effective if it affects enemies' team player
                if 'player' in attrs and thrower is not None \
                        and players[thrower]['team'] != players[attrs['player']]['team']:
                    last_flash.effective = True
                    last_flash.add_flash_duration(attrs['flashDuration'])

            # Event of ended round to track flashbangs by round
            if event['name'] == EVENT_ROUND_ENDED:
                attrs_array = event['attrs']
                attrs = {}
                for attr in attrs_array:
                    attrs[attr['key']] = attr['numVal']

                rounds.round_end(attrs['winner'])
        if flash_existed:
            flashes.append(last_flash)

    # To check if there is flashes with no thrower
    unidentified_flashes = 0
    for flash in flashes:
        if flash.thrower == 0 or flash.thrower is None:
            unidentified_flashes += 1

    if unidentified_flashes > 0:
        print(f'There is {unidentified_flashes} flashes with no thrower')

    return flashes, players


def get_smokes(dem):
    # Make set of players
    players = get_players(dem)

    events_ticks = dem['ticks']

    rounds = Rounds()
    smokes = []

    # Track the flashes
    for tick in events_ticks:
        last_smoke = Smoke(0, [], 0)
        smoke_existed = False
        for event in tick['events']:
            # Event when a grenade entity is destroyed
            # It contains trajectory and information about player who threw the grenade
            if event['name'] == EVENT_GRENADE_DESTROY:
                attrs_array = event['attrs']
                attrs = {}
                for attr in attrs_array:
                    if attr['key'] == 'trajectory':
                        attrs[attr['key']] = attr['trajectory']
                    else:
                        attrs[attr['key']] = attr['numVal']
                if attrs['weapon'] == EQUIP_SMOKE:
                    smoke_existed = True
                    last_smoke.thrower = attrs.get('player')
                    last_smoke.trajectory = attrs['trajectory']
                    last_smoke.g_round = rounds.sum() + 1

            # Event of ended round to track flashbangs by round
            if event['name'] == EVENT_ROUND_ENDED:
                attrs_array = event['attrs']
                attrs = {}
                for attr in attrs_array:
                    attrs[attr['key']] = attr['numVal']

                rounds.round_end(attrs['winner'])
        if smoke_existed:
            smokes.append(last_smoke)

    # To check if there is flashes with no thrower
    unidentified_smokes = 0
    for smoke in smokes:
        if smoke.thrower == 0 or smoke.thrower is None:
            unidentified_smokes += 1

    if unidentified_smokes > 0:
        print(f'There is {unidentified_smokes} smokes with no thrower')

    return smokes, players


def track_player(players, grenades, player_to_track):
    return [x for x in grenades if x.thrower is not None and player_to_track == players[x.thrower]['name']]


def print_event_flashed(attacker, player, players):
    if attacker is not None and player is not None:
        print(
            f'[{players[attacker]["team"]}]{players[attacker]["name"]} flashed [{players[player]["team"]}]{players[player]["name"]}')


def print_flashes(flashes, players_set, player=''):
    print(players_set)
    for flash in flashes:
        if flash.thrower is not None and players_set[flash.thrower]['name'] == player:
            print(f'Round {flash.round}')
            if flash.effective:
                print(f'You blinded enemies')
            else:
                print(f'Your flash is bullshit')


def deaths_with_knife(dem, players):
    deaths = {}
    for player in players:
        deaths[player] = 0
    for tick in dem['ticks']:
        for event in tick['events']:
            if event['name'] == 'kill':
                attrs = {}
                for attr in event['attrs']:
                    attrs[attr['key']] = attr['numVal']
                if attrs['victim_weapon'] == 405:
                    deaths[attrs['victim']] += 1
    return deaths


def get_all_stats(dem):
    players = get_players(dem)
    overall_stats = MatchInfo(players)
    game_started = False
    knife_round_played = False

    # Count KDA
    for tick in dem['ticks']:
        for event in tick['events']:
            if game_started and knife_round_played:
                if event['name'] == 'kill':
                    attrs = {}
                    for attr in event['attrs']:
                        attrs[attr['key']] = attr['numVal']
                    if 'victim' in attrs:
                        overall_stats.add_death(victim=attrs['victim'], killer=attrs.get('killer'))
                    if 'killer' in attrs:
                        overall_stats.add_kill(attrs['killer'])
                    if 'assister' in attrs:
                        overall_stats.add_assist(attrs['assister'])
                if event['name'] == 'hurt':
                    attrs = {}
                    for attr in event['attrs']:
                        if 'numVal' in attr:
                            attrs[attr['key']] = attr['numVal']
                        else:
                            attrs[attr['key']] = 0
                    if 'attacker' in attrs:
                        if attrs['attacker'] != attrs['player']:
                            overall_stats.add_damage(attrs['attacker'], min(attrs['health_damage'], 100))
                if event['name'] == EVENT_ROUND_ENDED:
                    attrs_array = event['attrs']
                    attrs = {}
                    for attr in attrs_array:
                        attrs[attr['key']] = attr['numVal']

                    overall_stats.new_round(attrs['winner'])
                if event['name'] in ['bomb_planted', 'bomb_defused']:
                    attrs = {}
                    for attr in event['attrs']:
                        attrs[attr['key']] = attr['numVal']
                    if event['name'] == 'bomb_planted':
                        overall_stats.add_bomb_planted(attrs['entityId'])
                    if event['name'] == 'bomb_defused':
                        overall_stats.add_bomb_defused(attrs['entityId'])
            if game_started and event['name'] == EVENT_MATCH_START:
                knife_round_played = True
            if event['name'] == EVENT_MATCH_START:
                game_started = True

    return overall_stats.get_stats()


def get_score(dem):
    events_ticks = dem['ticks']

    rounds = Rounds()
    game_started = False
    knife_round_played = False

    for tick in events_ticks:
        for event in tick['events']:
            if game_started and knife_round_played:
                if event['name'] == EVENT_ROUND_ENDED:
                    attrs_array = event['attrs']
                    attrs = {}
                    for attr in attrs_array:
                        attrs[attr['key']] = attr['numVal']

                    rounds.round_end(attrs['winner'])
            if game_started and event['name'] == EVENT_MATCH_START:
                knife_round_played = True
            if event['name'] == EVENT_MATCH_START:
                game_started = True

    return {1: rounds.t1_score, 2: rounds.t2_score}
