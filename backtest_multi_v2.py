"""Moving-average crossover backtest on several assets vs buy-and-hold.

Run: python backtest_multi_v2.py
Needs: pip install yfinance pandas numpy matplotlib
In Google Colab: run `!pip install yfinance` first, then paste this code in a cell.

To change the test, edit ASSETS and SHORT/LONG below.
Output files are named after the windows, so runs do not overwrite each other.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

ASSETS = {
    "Apple": "AAPL",
    "Goldman Sachs": "GS",
    "JP Morgan": "JPM",
    "Dow Jones": "^DJI",           # price index (no dividends)
    "Nasdaq Composite": "^IXIC",   # price index (no dividends)
}
START = "2015-01-01"
SHORT, LONG = 50, 200  # moving-average windows (days). First run used 20, 50.


def load_prices(ticker):
    """Daily closing prices (adjusted for splits and dividends when available)."""
    df = yf.download(ticker, start=START, auto_adjust=True, progress=False)
    return df["Close"].squeeze().dropna()


def backtest(prices):
    """Return (strategy returns, buy-and-hold returns, position signal)."""
    returns = prices.pct_change().dropna()
    short_ma = prices.rolling(SHORT).mean()
    long_ma = prices.rolling(LONG).mean()
    # Invested (1) when short MA > long MA, else cash (0).
    # shift(1): trade on yesterday's signal, which avoids look-ahead bias.
    signal = (short_ma > long_ma).astype(int).shift(1)
    signal = signal.reindex(returns.index).fillna(0)
    return signal * returns, returns, signal


def metrics(r):
    cumulative = (1 + r).cumprod()
    annual_return = cumulative.iloc[-1] ** (252 / len(r)) - 1
    volatility = r.std() * np.sqrt(252)
    sharpe = r.mean() / r.std() * np.sqrt(252) if r.std() > 0 else np.nan  # risk-free rate ignored
    max_drawdown = (cumulative / cumulative.cummax() - 1).min()
    return annual_return, volatility, sharpe, max_drawdown


def main():
    rows = []
    curves = {}
    for name, ticker in ASSETS.items():
        try:
            prices = load_prices(ticker)
        except Exception as exc:  # network or ticker problem
            print(f"Skipping {name} ({ticker}): {exc}")
            continue
        if len(prices) < LONG + 252:
            print(f"Skipping {name} ({ticker}): not enough data")
            continue

        strat, bh, signal = backtest(prices)
        curves[name] = ((1 + strat).cumprod(), (1 + bh).cumprod())

        for label, r in [("Strategy", strat), ("Buy & hold", bh)]:
            ann, vol, sharpe, dd = metrics(r)
            rows.append({
                "Asset": name,
                "Ticker": ticker,
                "Method": label,
                "Annual return": f"{ann:.1%}",
                "Volatility": f"{vol:.1%}",
                "Sharpe": f"{sharpe:.2f}",
                "Max drawdown": f"{dd:.1%}",
                "Time invested": f"{signal.mean():.0%}" if label == "Strategy" else "100%",
            })

    if not rows:
        print("No data downloaded. Check your internet connection and try again.")
        return

    print(f"\nMoving averages {SHORT}/{LONG}, data from {START}\n")
    table = pd.DataFrame(rows)
    print(table.to_string(index=False))
    csv_name = f"results_{SHORT}_{LONG}.csv"
    table.to_csv(csv_name, index=False)

    # Chart: one panel per asset
    n = len(curves)
    cols = 2
    nrows = (n + cols - 1) // cols
    fig, axes = plt.subplots(nrows, cols, figsize=(12, 4.5 * nrows), squeeze=False)
    for ax, (name, (strat_curve, bh_curve)) in zip(axes.flat, curves.items()):
        strat_curve.plot(ax=ax, label=f"MA {SHORT}/{LONG} strategy")
        bh_curve.plot(ax=ax, label="Buy & hold")
        ax.set_title(name)
        ax.set_ylabel("Growth of 1 unit invested")
        ax.legend()
    for ax in list(axes.flat)[n:]:
        ax.axis("off")
    fig.tight_layout()
    png_name = f"backtest_{SHORT}_{LONG}.png"
    fig.savefig(png_name, dpi=150)
    print(f"\nSaved {csv_name} and {png_name}")
    plt.show()


if __name__ == "__main__":
    main()
