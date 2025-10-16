"""
Utility functions for financial calculations and data processing.
"""

import numpy as np
import pandas as pd
from typing import Union, Optional


def calculate_returns(prices: Union[pd.Series, pd.DataFrame], 
                     method: str = 'simple') -> Union[pd.Series, pd.DataFrame]:
    """
    Calculate returns from price data.
    
    Parameters:
    -----------
    prices : pd.Series or pd.DataFrame
        Price data (can be single asset or multiple assets)
    method : str, default='simple'
        Method to calculate returns ('simple' or 'log')
        
    Returns:
    --------
    pd.Series or pd.DataFrame
        Returns data
    """
    if method == 'simple':
        returns = prices.pct_change()
    elif method == 'log':
        returns = np.log(prices / prices.shift(1))
    else:
        raise ValueError(f"Unknown method: {method}. Use 'simple' or 'log'")
    
    return returns.dropna()


def calculate_volatility(returns: Union[pd.Series, pd.DataFrame], 
                        annualize: bool = True,
                        periods_per_year: int = 252) -> Union[float, pd.Series]:
    """
    Calculate volatility (standard deviation) of returns.
    
    Parameters:
    -----------
    returns : pd.Series or pd.DataFrame
        Returns data
    annualize : bool, default=True
        Whether to annualize the volatility
    periods_per_year : int, default=252
        Number of periods per year (252 for daily, 52 for weekly, 12 for monthly)
        
    Returns:
    --------
    float or pd.Series
        Volatility (annualized if specified)
    """
    vol = returns.std()
    
    if annualize:
        vol = vol * np.sqrt(periods_per_year)
    
    return vol


def calculate_sharpe_ratio(returns: Union[pd.Series, pd.DataFrame],
                          risk_free_rate: float = 0.0,
                          annualize: bool = True,
                          periods_per_year: int = 252) -> Union[float, pd.Series]:
    """
    Calculate Sharpe ratio.
    
    Parameters:
    -----------
    returns : pd.Series or pd.DataFrame
        Returns data
    risk_free_rate : float, default=0.0
        Risk-free rate (annualized)
    annualize : bool, default=True
        Whether to annualize the Sharpe ratio
    periods_per_year : int, default=252
        Number of periods per year
        
    Returns:
    --------
    float or pd.Series
        Sharpe ratio
    """
    mean_return = returns.mean()
    std_return = returns.std()
    
    if annualize:
        mean_return = mean_return * periods_per_year
        std_return = std_return * np.sqrt(periods_per_year)
    
    # Adjust for risk-free rate
    excess_return = mean_return - risk_free_rate
    
    # Handle zero volatility case
    if isinstance(std_return, pd.Series):
        sharpe = excess_return / std_return.replace(0, np.nan)
    else:
        sharpe = excess_return / std_return if std_return != 0 else np.nan
    
    return sharpe


def calculate_covariance_matrix(returns: pd.DataFrame,
                               annualize: bool = True,
                               periods_per_year: int = 252) -> pd.DataFrame:
    """
    Calculate covariance matrix of returns.
    
    Parameters:
    -----------
    returns : pd.DataFrame
        Returns data for multiple assets
    annualize : bool, default=True
        Whether to annualize the covariance
    periods_per_year : int, default=252
        Number of periods per year
        
    Returns:
    --------
    pd.DataFrame
        Covariance matrix
    """
    cov_matrix = returns.cov()
    
    if annualize:
        cov_matrix = cov_matrix * periods_per_year
    
    return cov_matrix


def calculate_correlation_matrix(returns: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate correlation matrix of returns.
    
    Parameters:
    -----------
    returns : pd.DataFrame
        Returns data for multiple assets
        
    Returns:
    --------
    pd.DataFrame
        Correlation matrix
    """
    return returns.corr()
