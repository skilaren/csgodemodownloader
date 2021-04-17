import sqlite3
import subprocess

from celery import Celery

from csparser import DemoParser
from requester import Requester

app = Celery('tasks', broker='pyamqp://guest@localhost//')


@app.task
def load_and_store_stats(match_id, player_nickname, player_faceit_id):
    req = Requester()
    file_name = req.download_demo(match_id)
    out_file_name = f'{file_name.split(".")[0]}'
    subprocess.run(['./csminify.exe', '-demo', file_name,
                    '-format', 'json',
                    '-freq', '8',
                    '-out', out_file_name])
    result = DemoParser.parse(out_file_name, chosen_player=player_nickname)
    faceit_stats = req.get_match_stats(match_id, player_faceit_id)

    sql = f"""
                UPDATE matches SET 
                 kills = {result['stats']['kills']},
                 deaths = {result['stats']['deaths']},
                 assists = {result['stats']['assists']},
                 damage = {result['stats']['adr']},
                 headshots = {faceit_stats['Headshots %']},
                 mk_2k = {result['stats']['2k']},
                 mk_3k = {result['stats']['3k']},
                 mk_4k = {result['stats']['4k']},
                 mk_5k = {result['stats']['5k']},
                 mvps = {faceit_stats['MVPs']},
                 kd_ratio = {faceit_stats['K/D Ratio']},
                 kr_ratio = {faceit_stats['K/R Ratio']},
                 first_blood = {result['stats']['f_blood']},
                 first_death = {result['stats']['f_death']},
                 kast = {result['stats']['kast']},
                 hltv = {result['stats']['hltv_rating']},
                 flash_thrown = {result['flashes']['flashes_amount']},
                 useful_flash = {result['flashes']['successful_flashes_amount']},
                 flash_duration = {result['flashes']['total_duration']},
                 he_thrown = {result['he']['he_amount']},
                 useful_he = {result['he']['successful_grenades_amount']},
                 he_damage = {result['he']['total_damage']},
                 WHERE faceit_id = '{match_id}' AND player_faceit_id = '{player_faceit_id}'
                """
    con = sqlite3.connect('identifier.sqlite')
    cur = con.cursor()
    cur.execute(sql)
    cur.close()
    con.commit()
    con.close()
