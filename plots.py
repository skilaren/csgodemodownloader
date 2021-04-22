import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('results11.csv')

x_label = 'Average Kills'

# plt.plot(df.Elo.values[df['Matches'] > 500], df['Matches'].values[df['Matches'] > 500], 'bo', alpha=0.1)
plt.plot(df[x_label].values, df.Elo.values, 'bo', alpha=0.05)
print(np.mean(df.Matches))
print(np.mean(df.Winrate))
plt.ylabel('Elo')
plt.xlabel(x_label)
plt.xlim(0, 30)
# plt.ylim(500, 2500)
# plt.show()
plt.savefig('killselo.png', dpi=1200)


print(np.corrcoef(
    [df['Elo'],  # 1
     df['Average Kills'],  # 2
     df['Average Assists'],  # 3
     df['Average Deaths'],  # 4
     df['Average Headshots'],  # 5
     df['Headshots per Match'],  # 6
     df['K/D Ratio (%)'],  # 7
     df['K/R Ratio'],  # 8
     df['Average MVPs'],  # 9
     df['Average Penta Kills'],  # 10
     df['Average Quadro Kills'],  # 11
     df['Average Triple Kills'],  # 12
     df['Matches'],  # 13
     df['Wins'],  # 14
     df['Winrate'],  # 15
     df['Rounds'],  # 16
     df['Elo']]  # 17
))
