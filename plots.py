import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('datasets/extended_info.csv')

x_label = 'avg_damage'

# plt.plot(df.Elo.values[df['Matches'] > 500], df['Matches'].values[df['Matches'] > 500], 'bo', alpha=0.1)
plt.plot(df[x_label].values, df.elo.values, 'bo', alpha=0.1)
plt.ylabel('Elo')
plt.xlabel(x_label)
# plt.xlim(0, 30)
# plt.ylim(500, 2500)
# plt.show()
plt.savefig('dmgelo.png', dpi=1200)


# print(np.corrcoef(
#     [df['Elo'],  # 1
#      df['Average Kills'],  # 2
#      df['Average Assists'],  # 3
#      df['Average Deaths'],  # 4
#      df['Average Headshots'],  # 5
#      df['Headshots per Match'],  # 6
#      df['K/D Ratio (%)'],  # 7
#      df['K/R Ratio'],  # 8
#      df['Average MVPs'],  # 9
#      df['Average Penta Kills'],  # 10
#      df['Average Quadro Kills'],  # 11
#      df['Average Triple Kills'],  # 12
#      df['Matches'],  # 13
#      df['Wins'],  # 14
#      df['Winrate'],  # 15
#      df['Rounds'],  # 16
#      df['Elo']]  # 17
# ))

print(np.corrcoef(
 [
  df['elo'],
  df['avg_kills'],
  df['avg_deaths'],
  df['avg_assists'],
  df['avg_damage'],
  df['headshots'],
  df['avg_kd_ratio'],
  df['avg_kr_ratio'],
  df['avg_mvps'],
  df['avg_mk_2k'],
  df['avg_3k'],
  df['avg_4k'],
  df['avg_5k'],
  df['flash_thrown'],
  df['avg_useful_flash'],
  df['avg_flash_duration'],
  df['avg_he_thrown'],
  df['avg_useful_he'],
  df['avg_he_damage'],
  df['avg_kast'],
  df['avg_hltv'],
  df['avg_first_blood'],
  df['avg_first_death'],
  df['avg_bomb_planted'],
  df['avg_bomb_defused'],
  df['avg_bomb_actions_total'],
  df['matches_amount']]
))
