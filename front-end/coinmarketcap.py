from coinmarketcap import Market


c = Market()
c.ticker(start=0, limit=5, convert='USD')