# Finean - Financial Analysis and Portfolio Optimization

A Python library for investment portfolio optimization using maximum yield given variability, with time series predictions for asset returns.

## Features

- **Portfolio Optimization**: Multiple optimization strategies including:
  - Maximum Sharpe Ratio (risk-adjusted return maximization)
  - Minimum Volatility (risk minimization)
  - Maximum Return for given risk level
  - Efficient Frontier calculation

- **Time Series Prediction**: Forecast asset returns using:
  - Exponentially Weighted Moving Average (EWMA)
  - Simple Moving Average (SMA)
  - Exponential Moving Average (EMA)
  - Historical Mean
  - Covariance matrix estimation with shrinkage methods

- **Financial Utilities**: Calculate key metrics:
  - Returns (simple and log)
  - Volatility (annualized and non-annualized)
  - Sharpe Ratio
  - Covariance and Correlation matrices

## Installation

```bash
pip install -r requirements.txt
```

### Requirements

- numpy >= 1.21.0
- pandas >= 1.3.0
- scipy >= 1.7.0
- matplotlib >= 3.4.0

## Quick Start

```python
import numpy as np
import pandas as pd
from finean import PortfolioOptimizer, TimeSeriesPredictor
from finean.utils import calculate_returns

# 1. Load or generate historical price data
prices = pd.read_csv('your_price_data.csv', index_col=0, parse_dates=True)

# 2. Calculate returns
returns = calculate_returns(prices, method='simple')

# 3. Use time series predictor to forecast returns
predictor = TimeSeriesPredictor(method='ewma')
predictor.fit(returns, span=60)
predictions = predictor.get_predictions(annualize=True, periods_per_year=252)

# 4. Optimize portfolio
optimizer = PortfolioOptimizer(
    expected_returns=predictions['returns'],
    covariance_matrix=predictions['covariance'],
    risk_free_rate=0.02
)

# Find maximum Sharpe ratio portfolio
result = optimizer.optimize_max_sharpe(
    constraints={'long_only': True, 'max_weight': 0.5}
)

print(f"Optimal Weights:\n{result['weights']}")
print(f"Expected Return: {result['expected_return']:.2%}")
print(f"Volatility: {result['volatility']:.2%}")
print(f"Sharpe Ratio: {result['sharpe_ratio']:.3f}")
```

## Usage Examples

### Portfolio Optimization

```python
from finean import PortfolioOptimizer

# Create optimizer with expected returns and covariance matrix
optimizer = PortfolioOptimizer(
    expected_returns=expected_returns,  # pd.Series
    covariance_matrix=cov_matrix,       # pd.DataFrame
    risk_free_rate=0.02
)

# 1. Maximum Sharpe Ratio Portfolio
max_sharpe = optimizer.optimize_max_sharpe(
    constraints={'long_only': True, 'max_weight': 0.4}
)

# 2. Minimum Volatility Portfolio
min_vol = optimizer.optimize_min_volatility()

# 3. Maximum Return for Target Risk
target_risk = optimizer.optimize_max_return_for_risk(target_volatility=0.15)

# 4. Calculate Efficient Frontier
frontier = optimizer.calculate_efficient_frontier(n_points=100)
```

### Time Series Prediction

```python
from finean import TimeSeriesPredictor

# Create predictor
predictor = TimeSeriesPredictor(method='ewma')

# Fit on historical returns
predictor.fit(returns, span=60)

# Get predictions
expected_returns = predictor.predict_returns()
cov_matrix = predictor.predict_covariance(method='shrinkage')

# Or get both at once
predictions = predictor.get_predictions(annualize=True)
```

### Financial Calculations

```python
from finean.utils import (
    calculate_returns,
    calculate_volatility,
    calculate_sharpe_ratio,
    calculate_covariance_matrix
)

# Calculate returns
returns = calculate_returns(prices, method='simple')

# Calculate volatility
vol = calculate_volatility(returns, annualize=True, periods_per_year=252)

# Calculate Sharpe ratio
sharpe = calculate_sharpe_ratio(returns, risk_free_rate=0.02, annualize=True)

# Calculate covariance matrix
cov = calculate_covariance_matrix(returns, annualize=True)
```

## Running the Example

A comprehensive example is provided in `examples/portfolio_optimization_example.py`:

```bash
python examples/portfolio_optimization_example.py
```

This will:
1. Generate sample historical price data
2. Calculate returns and use time series prediction
3. Optimize portfolios using different strategies
4. Calculate the efficient frontier
5. Create visualizations showing the results

## Testing

Run the test suite to verify the installation:

```bash
python -m unittest discover tests -v
```

All tests should pass, covering:
- Utility functions
- Time series prediction methods
- Portfolio optimization algorithms

## API Reference

### PortfolioOptimizer

Main class for portfolio optimization.

**Methods:**
- `optimize_max_sharpe(constraints=None)`: Find portfolio with maximum Sharpe ratio
- `optimize_min_volatility(constraints=None)`: Find minimum volatility portfolio
- `optimize_max_return_for_risk(target_volatility, constraints=None)`: Maximize return for given risk
- `calculate_efficient_frontier(n_points=100, constraints=None)`: Calculate efficient frontier
- `get_portfolio_statistics(weights)`: Calculate statistics for a given portfolio

**Constraints:**
- `max_weight`: Maximum weight per asset (default: 1.0)
- `min_weight`: Minimum weight per asset (default: 0.0)
- `long_only`: Boolean, whether to allow short selling (default: True)

### TimeSeriesPredictor

Class for time series prediction of asset returns.

**Methods:**
- `fit(returns, **kwargs)`: Fit predictor on historical returns
- `predict_returns(horizon=1)`: Predict expected returns
- `predict_covariance(method='sample')`: Predict covariance matrix
- `get_predictions(annualize=True, periods_per_year=252)`: Get both returns and covariance

**Prediction Methods:**
- `ewma`: Exponentially Weighted Moving Average
- `sma`: Simple Moving Average
- `ema`: Exponential Moving Average
- `historical_mean`: Historical mean returns

**Covariance Methods:**
- `sample`: Sample covariance
- `ewma`: Exponentially weighted covariance
- `shrinkage`: Ledoit-Wolf shrinkage estimator

## Mathematical Background

### Portfolio Optimization

The library implements Modern Portfolio Theory (MPT) optimization:

**Maximum Sharpe Ratio:**
Maximizes: (E[R] - Rf) / σ

Where:
- E[R] = Expected portfolio return
- Rf = Risk-free rate
- σ = Portfolio standard deviation (volatility)

**Subject to:**
- Sum of weights = 1
- Optional constraints on individual weights

**Minimum Volatility:**
Minimizes: σ = sqrt(w' Σ w)

Where:
- w = Portfolio weights
- Σ = Covariance matrix

**Efficient Frontier:**
The set of optimal portfolios offering the highest expected return for each level of risk.

### Time Series Prediction

The library uses various methods to predict future returns:

- **EWMA**: Gives more weight to recent observations
- **Moving Averages**: Simple or exponential averaging
- **Covariance Estimation**: Sample, EWMA, or shrinkage methods for better risk estimates

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Author

Fenian level finance
