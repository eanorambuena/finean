# Finean Quick Start Guide

Get started with portfolio optimization in 5 minutes!

## Installation

```bash
git clone https://github.com/eanorambuena/finean.git
cd finean
pip install -r requirements.txt
```

## Run the Example

```bash
python examples/portfolio_optimization_example.py
```

This will:
- Generate sample data for 5 assets over 1000 days
- Use time series prediction to forecast returns
- Optimize for maximum Sharpe ratio and minimum volatility
- Calculate the efficient frontier
- Save a visualization to `examples/portfolio_optimization_results.png`

## Your First Portfolio Optimization

Create a file `my_portfolio.py`:

```python
import pandas as pd
import numpy as np
from finean import PortfolioOptimizer, TimeSeriesPredictor
from finean.utils import calculate_returns

# 1. Create sample data (replace with your own price data)
dates = pd.date_range('2020-01-01', periods=500, freq='D')
prices = pd.DataFrame({
    'AAPL': 150 + np.cumsum(np.random.randn(500) * 2),
    'GOOGL': 2800 + np.cumsum(np.random.randn(500) * 20),
    'MSFT': 300 + np.cumsum(np.random.randn(500) * 3),
    'AMZN': 3300 + np.cumsum(np.random.randn(500) * 25),
}, index=dates)

# 2. Calculate returns
returns = calculate_returns(prices)

# 3. Predict future returns using EWMA
predictor = TimeSeriesPredictor(method='ewma')
predictor.fit(returns, span=60)
predictions = predictor.get_predictions(annualize=True)

# 4. Optimize portfolio
optimizer = PortfolioOptimizer(
    expected_returns=predictions['returns'],
    covariance_matrix=predictions['covariance'],
    risk_free_rate=0.02
)

# Find optimal portfolio
result = optimizer.optimize_max_sharpe(
    constraints={'long_only': True, 'max_weight': 0.5}
)

# 5. Display results
print("\n" + "="*60)
print("OPTIMAL PORTFOLIO")
print("="*60)
for asset, weight in result['weights'].items():
    if weight > 0.01:
        print(f"{asset:10s}: {weight:6.2%}")
        
print(f"\nExpected Return: {result['expected_return']:6.2%}")
print(f"Volatility:      {result['volatility']:6.2%}")
print(f"Sharpe Ratio:    {result['sharpe_ratio']:6.3f}")
print("="*60)
```

Run it:

```bash
python my_portfolio.py
```

## Use Your Own Data

Replace the sample data with your own CSV file:

```python
# Load your price data
prices = pd.read_csv('your_prices.csv', index_col=0, parse_dates=True)
# CSV format: first column is date, other columns are asset prices
# Example:
# Date,AAPL,GOOGL,MSFT
# 2020-01-01,150.0,2800.0,300.0
# 2020-01-02,151.5,2810.0,301.2
# ...

# Then continue with step 2 above
returns = calculate_returns(prices)
# ... rest of the code
```

## Common Tasks

### Compare Different Optimization Strategies

```python
# Maximum Sharpe Ratio
max_sharpe = optimizer.optimize_max_sharpe()

# Minimum Volatility
min_vol = optimizer.optimize_min_volatility()

# Maximum return for 15% volatility
target_risk = optimizer.optimize_max_return_for_risk(target_volatility=0.15)

# Compare
print("Max Sharpe Ratio:", max_sharpe['sharpe_ratio'])
print("Min Volatility:", min_vol['volatility'])
print("Target Risk Return:", target_risk['expected_return'])
```

### Try Different Prediction Methods

```python
# EWMA (good for recent trends)
predictor_ewma = TimeSeriesPredictor(method='ewma')
predictor_ewma.fit(returns, span=60)

# Historical Mean (long-term average)
predictor_mean = TimeSeriesPredictor(method='historical_mean')
predictor_mean.fit(returns)

# Simple Moving Average
predictor_sma = TimeSeriesPredictor(method='sma')
predictor_sma.fit(returns, window=30)
```

### Visualize Efficient Frontier

```python
import matplotlib.pyplot as plt

# Calculate efficient frontier
frontier = optimizer.calculate_efficient_frontier(n_points=50)

# Plot
plt.figure(figsize=(10, 6))
plt.plot(frontier['volatility'] * 100, 
         frontier['expected_return'] * 100, 
         'b-', linewidth=2)
plt.scatter(result['volatility'] * 100,
           result['expected_return'] * 100,
           c='red', s=200, marker='*', 
           label='Max Sharpe', zorder=3)
plt.xlabel('Annual Volatility (%)')
plt.ylabel('Expected Annual Return (%)')
plt.title('Efficient Frontier')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('efficient_frontier.png', dpi=300)
plt.show()
```

## Next Steps

- Read [USAGE.md](USAGE.md) for detailed documentation
- Check [README.md](README.md) for API reference
- Run tests: `python -m unittest discover tests`
- Explore the example: `examples/portfolio_optimization_example.py`

## Tips

1. **Data**: Use at least 1-2 years of daily price data
2. **Rebalance**: Re-optimize monthly or quarterly
3. **Constraints**: Start with `max_weight=0.4` to ensure diversification
4. **Risk-Free Rate**: Use current T-bill rate (e.g., 0.02 for 2%)
5. **Method**: EWMA is good for recent trends, historical mean for stability

## Help & Support

- Issues: https://github.com/eanorambuena/finean/issues
- Documentation: See README.md and USAGE.md
- Tests: `python -m unittest discover tests -v`

Happy investing! 📈
