# Finean Usage Guide

## Table of Contents
1. [Getting Started](#getting-started)
2. [Basic Workflow](#basic-workflow)
3. [Time Series Prediction](#time-series-prediction)
4. [Portfolio Optimization](#portfolio-optimization)
5. [Advanced Features](#advanced-features)

## Getting Started

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Or install as package
pip install -e .
```

### Import the Library

```python
from finean import PortfolioOptimizer, TimeSeriesPredictor
from finean.utils import calculate_returns, calculate_volatility, calculate_sharpe_ratio
```

## Basic Workflow

### Step 1: Prepare Your Data

Your data should be in a pandas DataFrame with:
- Index: Dates (datetime)
- Columns: Asset names
- Values: Asset prices

```python
import pandas as pd

# Load your price data
prices = pd.read_csv('prices.csv', index_col=0, parse_dates=True)

# Or create sample data
import numpy as np
dates = pd.date_range('2020-01-01', periods=1000, freq='D')
prices = pd.DataFrame({
    'Stock_A': np.cumsum(np.random.randn(1000)) + 100,
    'Stock_B': np.cumsum(np.random.randn(1000)) + 50,
    'Stock_C': np.cumsum(np.random.randn(1000)) + 150,
}, index=dates)
```

### Step 2: Calculate Returns

```python
from finean.utils import calculate_returns

# Calculate simple returns (recommended for portfolio optimization)
returns = calculate_returns(prices, method='simple')

# Or log returns
log_returns = calculate_returns(prices, method='log')
```

### Step 3: Predict Future Returns

```python
from finean import TimeSeriesPredictor

# Create predictor with EWMA method
predictor = TimeSeriesPredictor(method='ewma')

# Fit on historical data
predictor.fit(returns, span=60)

# Get predictions (annualized)
predictions = predictor.get_predictions(annualize=True, periods_per_year=252)
expected_returns = predictions['returns']
cov_matrix = predictions['covariance']
```

### Step 4: Optimize Portfolio

```python
from finean import PortfolioOptimizer

# Create optimizer
optimizer = PortfolioOptimizer(
    expected_returns=expected_returns,
    covariance_matrix=cov_matrix,
    risk_free_rate=0.02  # 2% annual risk-free rate
)

# Find optimal portfolio
result = optimizer.optimize_max_sharpe(
    constraints={'long_only': True, 'max_weight': 0.5}
)

# Print results
print(f"Optimal Weights:\n{result['weights']}")
print(f"Expected Return: {result['expected_return']:.2%}")
print(f"Volatility: {result['volatility']:.2%}")
print(f"Sharpe Ratio: {result['sharpe_ratio']:.3f}")
```

## Time Series Prediction

### Available Methods

#### 1. EWMA (Exponentially Weighted Moving Average)
Gives more weight to recent observations.

```python
predictor = TimeSeriesPredictor(method='ewma')
predictor.fit(returns, span=60)  # span controls decay rate
```

#### 2. SMA (Simple Moving Average)
Equal weight to all observations in window.

```python
predictor = TimeSeriesPredictor(method='sma')
predictor.fit(returns, window=30)
```

#### 3. EMA (Exponential Moving Average)
Similar to EWMA with different parameterization.

```python
predictor = TimeSeriesPredictor(method='ema')
predictor.fit(returns, window=30)
```

#### 4. Historical Mean
Uses overall average of historical returns.

```python
predictor = TimeSeriesPredictor(method='historical_mean')
predictor.fit(returns)
```

### Covariance Estimation

```python
# Sample covariance (default)
cov = predictor.predict_covariance(method='sample')

# EWMA covariance (more responsive to recent correlations)
cov = predictor.predict_covariance(method='ewma')

# Shrinkage estimator (more stable, less extreme)
cov = predictor.predict_covariance(method='shrinkage')
```

## Portfolio Optimization

### Optimization Strategies

#### 1. Maximum Sharpe Ratio
Maximizes risk-adjusted returns.

```python
result = optimizer.optimize_max_sharpe(
    constraints={
        'long_only': True,      # No short selling
        'max_weight': 0.5,      # Max 50% in any asset
        'min_weight': 0.0       # Min 0% in any asset
    }
)
```

#### 2. Minimum Volatility
Minimizes portfolio risk.

```python
result = optimizer.optimize_min_volatility(
    constraints={'long_only': True}
)
```

#### 3. Maximum Return for Target Risk
Maximizes return while keeping risk at target level.

```python
result = optimizer.optimize_max_return_for_risk(
    target_volatility=0.15,  # 15% annual volatility
    constraints={'long_only': True}
)
```

#### 4. Efficient Frontier
Calculate multiple optimal portfolios for different risk levels.

```python
frontier = optimizer.calculate_efficient_frontier(
    n_points=100,
    constraints={'long_only': True}
)

# frontier is a DataFrame with columns:
# - volatility
# - expected_return
# - sharpe_ratio
```

### Constraint Options

```python
constraints = {
    'long_only': True,      # If True, no short selling (weights >= 0)
    'max_weight': 0.5,      # Maximum weight per asset
    'min_weight': 0.05      # Minimum weight per asset
}
```

## Advanced Features

### Custom Portfolio Analysis

```python
# Define your own weights
custom_weights = pd.Series([0.4, 0.3, 0.3], index=['Stock_A', 'Stock_B', 'Stock_C'])

# Get statistics
stats = optimizer.get_portfolio_statistics(custom_weights)
print(stats)
# Output: {'expected_return': 0.12, 'volatility': 0.18, 'sharpe_ratio': 0.56}
```

### Visualization

```python
import matplotlib.pyplot as plt

# Plot efficient frontier
frontier = optimizer.calculate_efficient_frontier(n_points=50)

plt.figure(figsize=(10, 6))
plt.plot(frontier['volatility'] * 100, frontier['expected_return'] * 100, 'b-')
plt.xlabel('Volatility (%)')
plt.ylabel('Expected Return (%)')
plt.title('Efficient Frontier')
plt.grid(True)
plt.show()
```

### Compare Multiple Portfolios

```python
# Optimize with different strategies
max_sharpe = optimizer.optimize_max_sharpe()
min_vol = optimizer.optimize_min_volatility()
target_risk = optimizer.optimize_max_return_for_risk(0.15)

# Create comparison DataFrame
comparison = pd.DataFrame({
    'Max Sharpe': max_sharpe['weights'],
    'Min Volatility': min_vol['weights'],
    'Target Risk': target_risk['weights']
})

print(comparison)
```

### Working with Different Time Frequencies

The library works with any time frequency. Just adjust the `periods_per_year` parameter:

```python
# Daily data (default)
predictions = predictor.get_predictions(annualize=True, periods_per_year=252)

# Weekly data
predictions = predictor.get_predictions(annualize=True, periods_per_year=52)

# Monthly data
predictions = predictor.get_predictions(annualize=True, periods_per_year=12)
```

## Complete Example

```python
import pandas as pd
import numpy as np
from finean import PortfolioOptimizer, TimeSeriesPredictor
from finean.utils import calculate_returns

# 1. Load data
prices = pd.read_csv('prices.csv', index_col=0, parse_dates=True)

# 2. Calculate returns
returns = calculate_returns(prices)

# 3. Predict returns and covariance
predictor = TimeSeriesPredictor(method='ewma')
predictor.fit(returns, span=60)
predictions = predictor.get_predictions(annualize=True)

# 4. Optimize portfolio
optimizer = PortfolioOptimizer(
    expected_returns=predictions['returns'],
    covariance_matrix=predictions['covariance'],
    risk_free_rate=0.02
)

# 5. Get results
max_sharpe = optimizer.optimize_max_sharpe(
    constraints={'long_only': True, 'max_weight': 0.4}
)

# 6. Print results
print("Optimal Portfolio:")
print(f"Weights:\n{max_sharpe['weights']}")
print(f"\nExpected Annual Return: {max_sharpe['expected_return']:.2%}")
print(f"Annual Volatility: {max_sharpe['volatility']:.2%}")
print(f"Sharpe Ratio: {max_sharpe['sharpe_ratio']:.3f}")
```

## Tips and Best Practices

1. **Data Quality**: Ensure your price data is clean (no missing values, correct dates)
2. **Historical Period**: Use at least 1-2 years of data for reliable estimates
3. **Rebalancing**: Re-optimize periodically (e.g., monthly or quarterly)
4. **Risk-Free Rate**: Use current treasury bill rate or similar
5. **Constraints**: Start with simple constraints and adjust based on requirements
6. **Covariance Method**: Shrinkage method often provides more stable estimates
7. **Time Series Method**: EWMA is good for recent trends, historical mean for long-term stability

## Troubleshooting

### Optimization doesn't converge
- Try loosening constraints
- Check if expected returns and covariance are reasonable
- Increase maxiter in optimization (not directly configurable in current version)

### Negative Sharpe ratios
- Check if expected returns are below risk-free rate
- Verify data quality and calculation method

### Extreme weights
- Add max_weight constraint
- Consider min_weight constraint to ensure diversification
- Use shrinkage covariance estimator

## Further Reading

- Modern Portfolio Theory: Markowitz (1952)
- Sharpe Ratio: Sharpe (1966)
- Covariance Shrinkage: Ledoit & Wolf (2004)
