"""
Unit tests for utility functions.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
import numpy as np
import pandas as pd
from finean.utils import (
    calculate_returns,
    calculate_volatility,
    calculate_sharpe_ratio,
    calculate_covariance_matrix,
    calculate_correlation_matrix
)


class TestUtils(unittest.TestCase):
    """Test cases for utility functions."""
    
    def setUp(self):
        """Set up test data."""
        # Create sample price data
        dates = pd.date_range('2020-01-01', periods=100, freq='D')
        np.random.seed(42)
        
        # Generate prices for 3 assets
        prices = pd.DataFrame({
            'Asset_A': 100 + np.cumsum(np.random.randn(100)),
            'Asset_B': 50 + np.cumsum(np.random.randn(100) * 0.5),
            'Asset_C': 150 + np.cumsum(np.random.randn(100) * 1.5)
        }, index=dates)
        
        self.prices = prices
        self.returns = calculate_returns(prices)
    
    def test_calculate_returns_simple(self):
        """Test simple returns calculation."""
        returns = calculate_returns(self.prices, method='simple')
        
        # Check shape
        self.assertEqual(returns.shape[0], self.prices.shape[0] - 1)
        self.assertEqual(returns.shape[1], self.prices.shape[1])
        
        # Check no NaN values
        self.assertFalse(returns.isna().any().any())
        
        # Manual calculation for first return
        expected_first = (self.prices.iloc[1, 0] / self.prices.iloc[0, 0]) - 1
        self.assertAlmostEqual(returns.iloc[0, 0], expected_first, places=10)
    
    def test_calculate_returns_log(self):
        """Test log returns calculation."""
        returns = calculate_returns(self.prices, method='log')
        
        # Check shape
        self.assertEqual(returns.shape[0], self.prices.shape[0] - 1)
        
        # Manual calculation for first return
        expected_first = np.log(self.prices.iloc[1, 0] / self.prices.iloc[0, 0])
        self.assertAlmostEqual(returns.iloc[0, 0], expected_first, places=10)
    
    def test_calculate_returns_invalid_method(self):
        """Test that invalid method raises error."""
        with self.assertRaises(ValueError):
            calculate_returns(self.prices, method='invalid')
    
    def test_calculate_volatility(self):
        """Test volatility calculation."""
        vol = calculate_volatility(self.returns, annualize=False)
        
        # Check that we get a value for each asset
        self.assertEqual(len(vol), 3)
        
        # Check all positive
        self.assertTrue((vol > 0).all())
        
        # Check annualized is different from non-annualized
        vol_annual = calculate_volatility(self.returns, annualize=True, periods_per_year=252)
        self.assertGreater(vol_annual.iloc[0], vol.iloc[0])
    
    def test_calculate_sharpe_ratio(self):
        """Test Sharpe ratio calculation."""
        sharpe = calculate_sharpe_ratio(self.returns, risk_free_rate=0.0, annualize=False)
        
        # Check that we get a value for each asset
        self.assertEqual(len(sharpe), 3)
        
        # Check values are finite
        self.assertTrue(np.isfinite(sharpe).all())
    
    def test_calculate_sharpe_ratio_with_rf(self):
        """Test Sharpe ratio with risk-free rate."""
        sharpe_no_rf = calculate_sharpe_ratio(self.returns, risk_free_rate=0.0, annualize=True)
        sharpe_with_rf = calculate_sharpe_ratio(self.returns, risk_free_rate=0.02, annualize=True)
        
        # Sharpe with positive RF should be lower
        self.assertTrue((sharpe_with_rf <= sharpe_no_rf).all())
    
    def test_calculate_covariance_matrix(self):
        """Test covariance matrix calculation."""
        cov_matrix = calculate_covariance_matrix(self.returns, annualize=False)
        
        # Check shape
        self.assertEqual(cov_matrix.shape, (3, 3))
        
        # Check symmetry
        self.assertTrue(np.allclose(cov_matrix, cov_matrix.T))
        
        # Check diagonal is positive (variances)
        self.assertTrue((np.diag(cov_matrix) > 0).all())
        
        # Check annualized is larger
        cov_annual = calculate_covariance_matrix(self.returns, annualize=True, periods_per_year=252)
        self.assertGreater(cov_annual.iloc[0, 0], cov_matrix.iloc[0, 0])
    
    def test_calculate_correlation_matrix(self):
        """Test correlation matrix calculation."""
        corr_matrix = calculate_correlation_matrix(self.returns)
        
        # Check shape
        self.assertEqual(corr_matrix.shape, (3, 3))
        
        # Check symmetry
        self.assertTrue(np.allclose(corr_matrix, corr_matrix.T))
        
        # Check diagonal is 1 (self-correlation)
        self.assertTrue(np.allclose(np.diag(corr_matrix), 1.0))
        
        # Check values are between -1 and 1
        self.assertTrue((corr_matrix >= -1).all().all())
        self.assertTrue((corr_matrix <= 1).all().all())


if __name__ == '__main__':
    unittest.main()
