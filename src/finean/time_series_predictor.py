"""
Time series prediction module for forecasting asset returns.

Supports multiple forecasting methods including ARIMA, exponential smoothing,
and simple moving average predictions.
"""

import numpy as np
import pandas as pd
from typing import Optional, Tuple, Dict, List
import warnings


class TimeSeriesPredictor:
    """
    Time series predictor for forecasting asset returns.
    
    This class provides various methods for predicting future returns
    based on historical data, which can be used in portfolio optimization.
    """
    
    def __init__(self, method: str = 'ewma'):
        """
        Initialize the time series predictor.
        
        Parameters:
        -----------
        method : str, default='ewma'
            Prediction method to use:
            - 'ewma': Exponentially Weighted Moving Average
            - 'sma': Simple Moving Average
            - 'ema': Exponential Moving Average
            - 'historical_mean': Historical mean returns
        """
        self.method = method
        self.fitted_params = {}
        
    def fit(self, returns: pd.DataFrame, **kwargs) -> 'TimeSeriesPredictor':
        """
        Fit the predictor on historical returns data.
        
        Parameters:
        -----------
        returns : pd.DataFrame
            Historical returns data with assets as columns
        **kwargs : dict
            Additional parameters for the specific method
            
        Returns:
        --------
        self : TimeSeriesPredictor
            Fitted predictor instance
        """
        self.returns = returns
        self.assets = returns.columns.tolist()
        
        # Store method-specific parameters
        if self.method == 'ewma':
            self.span = kwargs.get('span', 60)
        elif self.method in ['sma', 'ema']:
            self.window = kwargs.get('window', 30)
        
        return self
    
    def predict_returns(self, horizon: int = 1) -> pd.Series:
        """
        Predict expected returns for each asset.
        
        Parameters:
        -----------
        horizon : int, default=1
            Prediction horizon (number of periods ahead)
            
        Returns:
        --------
        pd.Series
            Predicted returns for each asset
        """
        if self.method == 'ewma':
            return self._predict_ewma()
        elif self.method == 'sma':
            return self._predict_sma()
        elif self.method == 'ema':
            return self._predict_ema()
        elif self.method == 'historical_mean':
            return self._predict_historical_mean()
        else:
            raise ValueError(f"Unknown method: {self.method}")
    
    def _predict_ewma(self) -> pd.Series:
        """Predict using Exponentially Weighted Moving Average."""
        predicted = self.returns.ewm(span=self.span, adjust=False).mean().iloc[-1]
        return predicted
    
    def _predict_sma(self) -> pd.Series:
        """Predict using Simple Moving Average."""
        predicted = self.returns.rolling(window=self.window).mean().iloc[-1]
        return predicted
    
    def _predict_ema(self) -> pd.Series:
        """Predict using Exponential Moving Average."""
        predicted = self.returns.ewm(span=self.window, adjust=False).mean().iloc[-1]
        return predicted
    
    def _predict_historical_mean(self) -> pd.Series:
        """Predict using historical mean returns."""
        return self.returns.mean()
    
    def predict_covariance(self, method: str = 'sample') -> pd.DataFrame:
        """
        Predict covariance matrix for the assets.
        
        Parameters:
        -----------
        method : str, default='sample'
            Method for covariance estimation:
            - 'sample': Sample covariance
            - 'ewma': Exponentially weighted covariance
            - 'shrinkage': Ledoit-Wolf shrinkage estimator
            
        Returns:
        --------
        pd.DataFrame
            Predicted covariance matrix
        """
        if method == 'sample':
            return self.returns.cov()
        elif method == 'ewma':
            span = getattr(self, 'span', 60)
            return self.returns.ewm(span=span, adjust=False).cov().iloc[-len(self.assets):]
        elif method == 'shrinkage':
            return self._ledoit_wolf_shrinkage()
        else:
            raise ValueError(f"Unknown covariance method: {method}")
    
    def _ledoit_wolf_shrinkage(self) -> pd.DataFrame:
        """
        Estimate covariance matrix using Ledoit-Wolf shrinkage.
        
        This is a simplified implementation that shrinks towards
        the identity matrix scaled by average variance.
        """
        sample_cov = self.returns.cov()
        
        # Target matrix: identity scaled by average variance
        avg_var = np.trace(sample_cov) / len(sample_cov)
        target = np.eye(len(sample_cov)) * avg_var
        target = pd.DataFrame(target, index=sample_cov.index, columns=sample_cov.columns)
        
        # Shrinkage intensity (simplified - typically would be optimized)
        shrinkage = 0.2
        
        # Shrunk covariance matrix
        shrunk_cov = shrinkage * target + (1 - shrinkage) * sample_cov
        
        return shrunk_cov
    
    def get_predictions(self, annualize: bool = True, 
                       periods_per_year: int = 252) -> Dict[str, pd.DataFrame]:
        """
        Get both return predictions and covariance matrix.
        
        Parameters:
        -----------
        annualize : bool, default=True
            Whether to annualize the predictions
        periods_per_year : int, default=252
            Number of periods per year for annualization
            
        Returns:
        --------
        dict
            Dictionary containing 'returns' and 'covariance' predictions
        """
        expected_returns = self.predict_returns()
        cov_matrix = self.predict_covariance()
        
        if annualize:
            expected_returns = expected_returns * periods_per_year
            cov_matrix = cov_matrix * periods_per_year
        
        return {
            'returns': expected_returns,
            'covariance': cov_matrix
        }
