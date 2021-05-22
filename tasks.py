import os
import pprint
import subprocess

import psycopg2
from celery import Celery
from celery.utils.log import get_task_logger

from csparser import DemoParser
from requester import Requester

app = Celery('tasks', broker='pyamqp://guest@13.49.67.1')


logger = get_task_logger(__name__)


#@app.task(acks_late=True)
def load_and_store_stats(match_id, player_faceit_id):
    req = Requester()
    logger.warning(f'[STARTED] match: {match_id} for player: {player_faceit_id}')
    file_name = req.download_demo(match_id)
    try:
        out_file_name = f'matches/{file_name}.json'
        subprocess.run(['./csminify.exe', '-demo', f'matches/{file_name}.dem',
                        '-format', 'json',
                        '-freq', '8',
                        '-out', out_file_name])
        logger.warning(f'[DEMO PARSED] match: {match_id} for player: {player_faceit_id}')
        faceit_stats, player_nickname = req.get_match_stats(match_id, player_faceit_id)
        result = DemoParser.parse(out_file_name, chosen_player=player_nickname)
        pprint.pprint(result)
        return None
        logger.warning(f'[PARSED] match: {match_id} for player: {player_faceit_id}')

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
                             he_thrown = {result['grenades']['grenades_amount']},
                             useful_he = {result['grenades']['successful_grenades_amount']},
                             he_damage = {result['grenades']['total_damage']}
                             WHERE faceit_id = '{match_id}' AND player_faceit_id = '{player_faceit_id}'
                            """
        con = psycopg2.connect("host=13.53.197.126 port=5432 dbname=csgo user=csgo password=csgo")
        cur = con.cursor()
        cur.execute(sql, ())
        cur.close()
        con.commit()
        con.close()
    except Exception as ex:
        logger.warning(f'[ERROR] match: {match_id} for player: {player_faceit_id}')
        logger.warning(ex)
        raise ex
    finally:
        if os.path.exists(f'matches/{file_name}.json'):
            os.remove(f'matches/{file_name}.json')
        if os.path.exists(f'matches/{file_name}.dem'):
            os.remove(f'matches/{file_name}.dem')
        if os.path.exists(f'matches/{file_name}.dem.gz'):
            os.remove(f'matches/{file_name}.dem.gz')
    logger.warning(f'[ENDED] match: {match_id} for player: {player_faceit_id}')
