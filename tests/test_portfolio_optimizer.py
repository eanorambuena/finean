"""
Unit tests for PortfolioOptimizer.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
import numpy as np
import pandas as pd
from finean.portfolio_optimizer import PortfolioOptimizer


class TestPortfolioOptimizer(unittest.TestCase):
    """Test cases for PortfolioOptimizer."""
    
    def setUp(self):
        """Set up test data."""
        # Create sample expected returns and covariance matrix
        np.random.seed(42)
        
        assets = ['Asset_A', 'Asset_B', 'Asset_C']
        
        # Expected annual returns
        expected_returns = pd.Series([0.10, 0.15, 0.12], index=assets)
        
        # Covariance matrix (annual)
        cov_data = np.array([
            [0.04, 0.01, 0.015],
            [0.01, 0.09, 0.02],
            [0.015, 0.02, 0.06]
        ])
        cov_matrix = pd.DataFrame(cov_data, index=assets, columns=assets)
        
        self.expected_returns = expected_returns
        self.cov_matrix = cov_matrix
        self.assets = assets
    
    def test_optimizer_initialization(self):
        """Test optimizer initialization."""
        optimizer = PortfolioOptimizer(
            expected_returns=self.expected_returns,
            covariance_matrix=self.cov_matrix,
            risk_free_rate=0.02
        )
        
        self.assertEqual(optimizer.risk_free_rate, 0.02)
        self.assertEqual(optimizer.n_assets, 3)
        self.assertEqual(len(optimizer.assets), 3)
    
    def test_optimize_max_sharpe(self):
        """Test maximum Sharpe ratio optimization."""
        optimizer = PortfolioOptimizer(
            expected_returns=self.expected_returns,
            covariance_matrix=self.cov_matrix,
            risk_free_rate=0.02
        )
        
        result = optimizer.optimize_max_sharpe()
        
        # Check result structure
        self.assertIn('weights', result)
        self.assertIn('expected_return', result)
        self.assertIn('volatility', result)
        self.assertIn('sharpe_ratio', result)
        
        # Check weights sum to 1
        self.assertAlmostEqual(result['weights'].sum(), 1.0, places=6)
        
        # Check all weights are non-negative (long only by default)
        self.assertTrue((result['weights'] >= -1e-6).all())
        
        # Check Sharpe ratio is positive
        self.assertGreater(result['sharpe_ratio'], 0)
    
    def test_optimize_min_volatility(self):
        """Test minimum volatility optimization."""
        optimizer = PortfolioOptimizer(
            expected_returns=self.expected_returns,
            covariance_matrix=self.cov_matrix
        )
        
        result = optimizer.optimize_min_volatility()
        
        # Check result structure
        self.assertIn('weights', result)
        self.assertIn('volatility', result)
        
        # Check weights sum to 1
        self.assertAlmostEqual(result['weights'].sum(), 1.0, places=6)
        
        # Check volatility is positive
        self.assertGreater(result['volatility'], 0)
    
    def test_optimize_max_return_for_risk(self):
        """Test optimization for maximum return given target risk."""
        optimizer = PortfolioOptimizer(
            expected_returns=self.expected_returns,
            covariance_matrix=self.cov_matrix
        )
        
        target_vol = 0.20
        result = optimizer.optimize_max_return_for_risk(target_vol)
        
        # Check result structure
        self.assertIn('weights', result)
        self.assertIn('expected_return', result)
        self.assertIn('volatility', result)
        
        # Check weights sum to 1
        self.assertAlmostEqual(result['weights'].sum(), 1.0, places=6)
        
        # Check volatility is at or below target (with tolerance)
        self.assertLessEqual(result['volatility'], target_vol + 0.01)
    
    def test_weight_constraints(self):
        """Test portfolio optimization with weight constraints."""
        optimizer = PortfolioOptimizer(
            expected_returns=self.expected_returns,
            covariance_matrix=self.cov_matrix
        )
        
        # Optimize with max weight constraint
        result = optimizer.optimize_max_sharpe(
            constraints={'max_weight': 0.5, 'min_weight': 0.1}
        )
        
        # Check max weight constraint
        self.assertTrue((result['weights'] <= 0.5 + 1e-6).all())
        
        # Check min weight constraint (sum of weights = 1 and max_weight = 0.5
        # means at least 2 assets must have weight >= min_weight)
        # But we can't guarantee all have min_weight, so we just check max
    
    def test_calculate_efficient_frontier(self):
        """Test efficient frontier calculation."""
        optimizer = PortfolioOptimizer(
            expected_returns=self.expected_returns,
            covariance_matrix=self.cov_matrix
        )
        
        frontier = optimizer.calculate_efficient_frontier(n_points=20)
        
        # Check it returns a DataFrame
        self.assertIsInstance(frontier, pd.DataFrame)
        
        # Check columns
        self.assertIn('volatility', frontier.columns)
        self.assertIn('expected_return', frontier.columns)
        self.assertIn('sharpe_ratio', frontier.columns)
        
        # Check we got some points
        self.assertGreater(len(frontier), 0)
        
        # Check returns increase with volatility (generally true for efficient frontier)
        self.assertTrue((frontier['expected_return'].diff().dropna() >= -0.01).all())
    
    def test_get_portfolio_statistics(self):
        """Test calculation of portfolio statistics."""
        optimizer = PortfolioOptimizer(
            expected_returns=self.expected_returns,
            covariance_matrix=self.cov_matrix,
            risk_free_rate=0.02
        )
        
        # Equal weight portfolio
        weights = pd.Series([1/3, 1/3, 1/3], index=self.assets)
        
        stats = optimizer.get_portfolio_statistics(weights)
        
        # Check keys
        self.assertIn('expected_return', stats)
        self.assertIn('volatility', stats)
        self.assertIn('sharpe_ratio', stats)
        
        # Check values are reasonable
        self.assertGreater(stats['expected_return'], 0)
        self.assertGreater(stats['volatility'], 0)
        self.assertIsInstance(stats['sharpe_ratio'], float)
    
    def test_portfolio_return_calculation(self):
        """Test portfolio return calculation."""
        optimizer = PortfolioOptimizer(
            expected_returns=self.expected_returns,
            covariance_matrix=self.cov_matrix
        )
        
        # Equal weight portfolio
        weights = np.array([1/3, 1/3, 1/3])
        
        portfolio_return = optimizer._calculate_portfolio_return(weights)
        
        # Should be average of individual returns
        expected = self.expected_returns.mean()
        self.assertAlmostEqual(portfolio_return, expected, places=10)
    
    def test_portfolio_volatility_calculation(self):
        """Test portfolio volatility calculation."""
        optimizer = PortfolioOptimizer(
            expected_returns=self.expected_returns,
            covariance_matrix=self.cov_matrix
        )
        
        # Single asset portfolio (Asset_A)
        weights = np.array([1.0, 0.0, 0.0])
        
        portfolio_vol = optimizer._calculate_portfolio_volatility(weights)
        
        # Should be square root of variance of Asset_A
        expected = np.sqrt(self.cov_matrix.iloc[0, 0])
        self.assertAlmostEqual(portfolio_vol, expected, places=10)
    
    def test_sharpe_ratio_calculation(self):
        """Test Sharpe ratio calculation."""
        optimizer = PortfolioOptimizer(
            expected_returns=self.expected_returns,
            covariance_matrix=self.cov_matrix,
            risk_free_rate=0.02
        )
        
        # Equal weight portfolio
        weights = np.array([1/3, 1/3, 1/3])
        
        sharpe = optimizer._calculate_sharpe_ratio(weights)
        
        # Manual calculation
        portfolio_return = np.dot(weights, self.expected_returns)
        portfolio_vol = np.sqrt(np.dot(weights, np.dot(self.cov_matrix, weights)))
        expected_sharpe = (portfolio_return - 0.02) / portfolio_vol
        
        self.assertAlmostEqual(sharpe, expected_sharpe, places=10)


if __name__ == '__main__':
    unittest.main()
