from finvizfinance.quote import finvizfinance

stock = finvizfinance('KO')
fundament = stock.ticker_fundament()
print("=== Key Metrics ===")
for key in ['P/E', 'Forward P/E', 'PEG', 'P/S', 'P/B', 'P/FCF', 'EPS (ttm)', 'EPS next Y', 'Dividend %', 'ROE', 'ROI', 'Beta', 'Target Price', 'Recom']:
    print(f"  {key}: {fundament.get(key, 'N/A')}")

print("\n=== Peers ===")
print(stock.ticker_peer())

print("\n=== News ===")
for item in stock.ticker_news()[:5]:
    print(f"  [{item[3]}] {item[1]}")
