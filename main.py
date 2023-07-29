import pandas as pd
import matplotlib.pyplot as plt

# Set the style for plots
plt.style.use('fivethirtyeight')

# Read the dataset into pandas
dec6 = pd.read_csv('datasets/coinmarketcap_06122017.csv')

# Filter out rows without a market capitalization
cap = dec6[dec6['market_cap_usd'] > 0]

# Get the top 10 market capitalization coins
cap10 = cap.nlargest(10, 'market_cap_usd').set_index('id')

# Calculate the percentage of market capitalization for each coin
cap10['market_cap_perc'] = (cap10['market_cap_usd'] / cap['market_cap_usd'].sum()) * 100

# Custom colors for the bar plots
COLORS = ['orange', 'green', 'red', 'cyan', 'blue', 'gray', 'purple', 'brown', 'pink', 'lightblue']

# Plot the top 10 market capitalization coins
ax = cap10['market_cap_perc'].plot.bar(title='Top 10 Market Capitalization', color=COLORS)
ax.set_ylabel('% of Total Cap')

# Add commas to y-axis labels for better readability
ax.set_yticklabels(['{:,}'.format(int(x)) for x in ax.get_yticks()])

plt.show()

# Plot market_cap_usd with log scale on the y-axis
ax = cap10['market_cap_usd'].plot.bar(title='Top 10 Market Capitalization', logy=True, color=COLORS)
ax.set_ylabel('USD (log scale)')
ax.set_xlabel('')
ax.set_yticklabels(['{:,}'.format(int(x)) for x in ax.get_yticks()])

plt.show()

# Select coins with non-null percent_change_24h and percent_change_7d
volatility = dec6[['id', 'percent_change_24h', 'percent_change_7d']].dropna()

# Sort by percent_change_24h in ascending order
volatility = volatility.sort_values(by='percent_change_24h')


# Function to plot top 10 losers and winners
def top10_subplot(volatility_series, title):
    colors_losers = ['darkred'] * 10
    colors_winners = ['darkblue'] * 10
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10, 6))
    ax = volatility_series[:10].plot.bar(color=colors_losers, ax=axes[0])
    fig.suptitle(title)
    ax.set_ylabel('% Change')
    ax = volatility_series[-10:].plot.bar(color=colors_winners, ax=axes[1])
    ax.set_ylabel('% Change')
    plt.tight_layout()
    return fig, ax


# Plot top 10 losers and winners based on percent_change_24h
DTITLE = "24 hours Top Losers and Winners"
fig, ax = top10_subplot(volatility['percent_change_24h'], DTITLE)
plt.show()

# Sort by percent_change_7d in ascending order
volatility7d = volatility.sort_values(by='percent_change_7d')

# Plot top 10 losers and winners based on percent_change_7d
WTITLE = "Weekly Top Losers and Winners"
fig, ax = top10_subplot(volatility7d['percent_change_7d'], WTITLE)
plt.show()

# Select coins with market_cap_usd greater than 10 billion
largecaps = cap[cap['market_cap_usd'] > 1E10]


# Count different market cap sizes
def capcount(query_string):
    return cap.query(query_string).shape[0]


# Labels for the plot
LABELS = ["Biggish", "Micro", "Nano"]

# Count the cryptocurrencies in each market cap size category
biggish = capcount("market_cap_usd > 3E+8")
micro = capcount("market_cap_usd >= 5E+7 & market_cap_usd < 3E+8")
nano = capcount("market_cap_usd < 5E+7")

# Plot the market cap size distribution
values = [biggish, micro, nano]
colors = ['purple', 'orange', 'green']

plt.bar(range(len(values)), values, tick_label=LABELS, color=colors)

# Add labels to the bars
for i, v in enumerate(values):
    plt.text(i, v + 20, str(v), ha='center', va='bottom', fontweight='bold')

plt.title('Market Cap Size Distribution')
plt.ylabel('Number of Cryptocurrencies')

plt.show()
