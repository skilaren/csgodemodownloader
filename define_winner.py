import psycopg2

from requester import Requester
from tasks import load_and_store_stats

sql = "SELECT faceit_id, player_faceit_id FROM matches;"
con = psycopg2.connect("host=13.53.197.126 port=5432 dbname=csgo user=csgo password=csgo")
cur = con.cursor()
cur.execute(sql, ())
res = cur.fetchall()
cur.close()


req = Requester()


def get_player_team(teams, player_id):
    for team in teams:
        for player in team['players']:
            if player['player_id'] == player_id:
                return team['team_id']


for i, r in enumerate(res):
    try:
        stats = req.get(f'matches/{r[0]}/stats')['rounds'][0]
        winner = stats['round_stats']['Winner']
        if winner == get_player_team(stats['teams'], r[1]):
            sql = f"UPDATE matches SET win = true WHERE faceit_id = '{r[0]}' AND player_faceit_id = '{r[1]}'"
            cur = con.cursor()
            cur.execute(sql, ())
            con.commit()
            cur.close()
        if i % 50 == 0:
            print(i)
    except Exception as ex:
        print(ex)
        continue


con.close()

