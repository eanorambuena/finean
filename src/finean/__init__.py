"""
Finean - Financial Analysis and Portfolio Optimization Library

A library for investment portfolio optimization using maximum yield given variability,
with time series predictions for asset returns.
"""

from .portfolio_optimizer import PortfolioOptimizer
from .time_series_predictor import TimeSeriesPredictor
from .utils import calculate_returns, calculate_volatility, calculate_sharpe_ratio

__version__ = "0.1.0"
__all__ = [
    "PortfolioOptimizer",
    "TimeSeriesPredictor",
    "calculate_returns",
    "calculate_volatility",
    "calculate_sharpe_ratio",
]
