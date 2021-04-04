import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('results.csv')

x_label = 'Headshots per Match'

# plt.plot(df.Elo.values[df['Matches'] > 500], df['Matches'].values[df['Matches'] > 500], 'bo', alpha=0.1)
plt.plot(df[x_label].values, df.Elo.values, 'bo', alpha=0.1)
plt.ylabel('Elo')
plt.xlabel(x_label)
x_min, x_max = plt.xlim()
plt.ylim(500, 2500)
# plt.show()
plt.savefig('hsmatchelo.png', dpi=1200)


print(np.corrcoef(
    [df['Elo'],
     df['Average Kills'],
     df['Average Assists'],
     df['Average Deaths'],
     df['Average Headshots'],
     df['Headshots per Match'],
     df['K/D Ratio'],
     df['K/R Ratio'],
     df['Average MVPs'],
     df['Average Penta Kills'],
     df['Average Quadro Kills'],
     df['Average Triple Kills'],
     df['Matches'],
     df['Wins'],
     df['Winrate'],
     df['Rounds'],
     df['Elo']]
))
