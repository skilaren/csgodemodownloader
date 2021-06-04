import psycopg2

from tasks import load_and_store_stats

sql = "SELECT faceit_id, player_faceit_id FROM matches WHERE kills is null;"
con = psycopg2.connect("host=13.53.197.126 port=5432 dbname=csgo user=csgo password=csgo")
cur = con.cursor()
cur.execute(sql, ())
res = cur.fetchall()

for r in res:
    load_and_store_stats.delay(r[0], r[1])

cur.close()
con.close()
