# Moving-Average Crossover Backtest

Python backtest of a moving-average crossover strategy on five US stocks and indices, compared with buy & hold. The project tests two window pairs (20/50 and 50/200 days) to see how much the results depend on that choice.

## Objective

Test whether a simple trend-following rule improves the risk-return profile of an investment, and check how sensitive the answer is to its parameters.

## Data

- Source: Yahoo Finance, via the `yfinance` library
- Period: 2015-01-01 to the run date, daily closing prices
- Assets: Apple (AAPL), Goldman Sachs (GS), JP Morgan (JPM), Dow Jones (^DJI), Nasdaq Composite (^IXIC)
- Stocks are adjusted for splits and dividends; the two indices are price indices without dividends

## Method

1. Compute a short and a long moving average of the closing price.
2. Signal: invested when the short average is above the long one, otherwise in cash.
3. The signal is shifted by one day (`shift(1)`), so each day's position uses only information available the day before. This avoids look-ahead bias.
4. Compare strategy and buy & hold on four measures: annualised return, annualised volatility, Sharpe ratio (risk-free rate ignored) and maximum drawdown. Time invested is also reported.

## Results

### Moving averages 20/50

| Asset | Method | Annual return | Volatility | Sharpe | Max drawdown | Time invested |
|---|---|---|---|---|---|---|
| Apple | Strategy | 12.7% | 19.8% | 0.70 | -29.1% | 63% |
| Apple | Buy & hold | 25.2% | 28.7% | 0.93 | -38.5% | 100% |
| Goldman Sachs | Strategy | 11.7% | 20.3% | 0.65 | -47.4% | 61% |
| Goldman Sachs | Buy & hold | 16.0% | 29.4% | 0.65 | -48.7% | 100% |
| JP Morgan | Strategy | 12.8% | 18.0% | 0.76 | -23.8% | 65% |
| JP Morgan | Buy & hold | 18.4% | 26.8% | 0.76 | -43.6% | 100% |
| Dow Jones | Strategy | 5.5% | 10.8% | 0.55 | -18.8% | 67% |
| Dow Jones | Buy & hold | 9.6% | 17.2% | 0.62 | -37.1% | 100% |
| Nasdaq Composite | Strategy | 7.4% | 14.4% | 0.57 | -33.1% | 69% |
| Nasdaq Composite | Buy & hold | 15.7% | 21.4% | 0.79 | -36.4% | 100% |

<img width="1189" height="1339" alt="code test 2" src="https://github.com/user-attachments/assets/18830dda-b54c-4492-974b-a03cdcacdecb" />


### Moving averages 50/200

| Asset | Method | Annual return | Volatility | Sharpe | Max drawdown | Time invested |
|---|---|---|---|---|---|---|
| Apple | Strategy | 15.2% | 23.6% | 0.72 | -45.6% | 71% |
| Apple | Buy & hold | 25.2% | 28.7% | 0.93 | -38.5% | 100% |
| Goldman Sachs | Strategy | 11.3% | 23.4% | 0.58 | -45.8% | 59% |
| Goldman Sachs | Buy & hold | 16.0% | 29.4% | 0.65 | -48.7% | 100% |
| JP Morgan | Strategy | 12.4% | 21.3% | 0.65 | -43.6% | 72% |
| JP Morgan | Buy & hold | 18.4% | 26.8% | 0.76 | -43.6% | 100% |
| Dow Jones | Strategy | 2.8% | 13.6% | 0.27 | -39.6% | 76% |
| Dow Jones | Buy & hold | 9.6% | 17.2% | 0.62 | -37.1% | 100% |
| Nasdaq Composite | Strategy | 12.4% | 17.7% | 0.75 | -30.1% | 74% |
| Nasdaq Composite | Buy & hold | 15.7% | 21.4% | 0.79 | -36.4% | 100% |

<img width="1189" height="1339" alt="tedt 2" src="https://github.com/user-attachments/assets/4d687e3a-4374-4fa6-824b-e82014b6d77c" />


### Maximum drawdown across both tests

| Asset | Buy & hold | Strategy 20/50 | Strategy 50/200 |
|---|---|---|---|
| Apple | -38.5% | -29.1% | -45.6% |
| Goldman Sachs | -48.7% | -47.4% | -45.8% |
| JP Morgan | -43.6% | -23.8% | -43.6% |
| Dow Jones | -37.1% | -18.8% | -39.6% |
| Nasdaq Composite | -36.4% | -33.1% | -30.1% |

## Findings

- **What holds for both window pairs:** the strategy gives up return and lowers volatility on all five assets. Its Sharpe ratio is never better than buy & hold (equal for Goldman Sachs and JP Morgan with 20/50).
- **What changes:** with 20/50 the strategy cuts the maximum drawdown clearly for JP Morgan and the Dow Jones. With 50/200 that protection disappears: the strategy matches or exceeds the buy & hold drawdown on four of five assets. Annual returns also move with the window (Nasdaq 7.4% to 12.4%, Dow Jones 5.5% to 2.8%).
- **Visual reading of the charts (interpretation, not a tested result):** on the 50/200 charts, the Dow Jones and JP Morgan strategies appear to stay invested through the early-2020 crash and then remain in cash during the rebound, which is consistent with a slow signal reacting late. The Nasdaq is the exception: the strategy moves to cash during the 2022 decline and reduces its drawdown.
- **Conclusion:** the strategy trades return for lower volatility, but its protection against drawdowns depends strongly on the parameters.

## Limitations

- No transaction costs or taxes. A strategy that changes position often would look worse in practice.
- One period and two parameter pairs. Results may be sensitive to both and should not be generalised.
- Assets were chosen before running the test, but they are correlated (Goldman Sachs and JP Morgan are Dow Jones members; Apple weighs heavily in the Nasdaq).
- `^DJI` and `^IXIC` are price indices without dividends, while the stocks are adjusted for dividends and splits.
- The Sharpe ratio ignores the risk-free rate.
- The first 200 trading days are spent in cash while the long average warms up, which slightly penalises the 50/200 strategy.
- No out-of-sample test, so the parameters were not validated on unseen data.

## How to run

```bash
pip install yfinance pandas numpy matplotlib
python backtest_multi_v2.py
```

To change the test, edit `ASSETS` and `SHORT, LONG` at the top of the script. Outputs are named after the windows (`results_50_200.csv`, `backtest_50_200.png`), so runs do not overwrite each other.

## Files

- `backtest_multi_v2.py`: backtest script
- `results_20_50.csv`, `results_50_200.csv`: result tables
- `backtest_20_50.png`, `backtest_50_200.png`: charts

## Possible next steps

- Add transaction costs and test their effect.
- Test more window pairs and an out-of-sample period.
- Print the dates of signal changes around March 2020 to check the "late reaction" interpretation.
- Compare with a risk-adjusted benchmark that includes the risk-free rate.
