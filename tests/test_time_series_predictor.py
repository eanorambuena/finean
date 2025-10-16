"""
Unit tests for TimeSeriesPredictor.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
import numpy as np
import pandas as pd
from finean.time_series_predictor import TimeSeriesPredictor
from finean.utils import calculate_returns


class TestTimeSeriesPredictor(unittest.TestCase):
    """Test cases for TimeSeriesPredictor."""
    
    def setUp(self):
        """Set up test data."""
        # Create sample return data
        dates = pd.date_range('2020-01-01', periods=200, freq='D')
        np.random.seed(42)
        
        # Generate returns for 3 assets
        returns = pd.DataFrame({
            'Asset_A': np.random.randn(200) * 0.01 + 0.0005,
            'Asset_B': np.random.randn(200) * 0.015 + 0.0003,
            'Asset_C': np.random.randn(200) * 0.02 + 0.0008
        }, index=dates)
        
        self.returns = returns
    
    def test_predictor_initialization(self):
        """Test predictor initialization."""
        predictor = TimeSeriesPredictor(method='ewma')
        self.assertEqual(predictor.method, 'ewma')
        
        predictor2 = TimeSeriesPredictor(method='sma')
        self.assertEqual(predictor2.method, 'sma')
    
    def test_fit_method(self):
        """Test fitting the predictor."""
        predictor = TimeSeriesPredictor(method='ewma')
        predictor.fit(self.returns, span=60)
        
        # Check that returns and assets are stored
        self.assertTrue(hasattr(predictor, 'returns'))
        self.assertTrue(hasattr(predictor, 'assets'))
        self.assertEqual(len(predictor.assets), 3)
        self.assertEqual(predictor.span, 60)
    
    def test_predict_returns_ewma(self):
        """Test EWMA prediction."""
        predictor = TimeSeriesPredictor(method='ewma')
        predictor.fit(self.returns, span=60)
        
        predictions = predictor.predict_returns()
        
        # Check shape
        self.assertEqual(len(predictions), 3)
        
        # Check all values are finite
        self.assertTrue(np.isfinite(predictions).all())
    
    def test_predict_returns_sma(self):
        """Test SMA prediction."""
        predictor = TimeSeriesPredictor(method='sma')
        predictor.fit(self.returns, window=30)
        
        predictions = predictor.predict_returns()
        
        # Check shape
        self.assertEqual(len(predictions), 3)
        
        # Check all values are finite
        self.assertTrue(np.isfinite(predictions).all())
    
    def test_predict_returns_historical_mean(self):
        """Test historical mean prediction."""
        predictor = TimeSeriesPredictor(method='historical_mean')
        predictor.fit(self.returns)
        
        predictions = predictor.predict_returns()
        
        # Check shape
        self.assertEqual(len(predictions), 3)
        
        # Should be equal to mean
        expected = self.returns.mean()
        pd.testing.assert_series_equal(predictions, expected)
    
    def test_predict_covariance_sample(self):
        """Test sample covariance prediction."""
        predictor = TimeSeriesPredictor(method='ewma')
        predictor.fit(self.returns)
        
        cov = predictor.predict_covariance(method='sample')
        
        # Check shape
        self.assertEqual(cov.shape, (3, 3))
        
        # Check symmetry
        self.assertTrue(np.allclose(cov, cov.T))
        
        # Check positive diagonal
        self.assertTrue((np.diag(cov) > 0).all())
    
    def test_predict_covariance_shrinkage(self):
        """Test shrinkage covariance prediction."""
        predictor = TimeSeriesPredictor(method='ewma')
        predictor.fit(self.returns)
        
        cov = predictor.predict_covariance(method='shrinkage')
        
        # Check shape
        self.assertEqual(cov.shape, (3, 3))
        
        # Check symmetry
        self.assertTrue(np.allclose(cov, cov.T))
        
        # Check positive diagonal
        self.assertTrue((np.diag(cov) > 0).all())
    
    def test_get_predictions(self):
        """Test getting both returns and covariance."""
        predictor = TimeSeriesPredictor(method='ewma')
        predictor.fit(self.returns, span=60)
        
        predictions = predictor.get_predictions(annualize=True, periods_per_year=252)
        
        # Check keys
        self.assertIn('returns', predictions)
        self.assertIn('covariance', predictions)
        
        # Check shapes
        self.assertEqual(len(predictions['returns']), 3)
        self.assertEqual(predictions['covariance'].shape, (3, 3))
    
    def test_get_predictions_annualized(self):
        """Test that annualization scales properly."""
        predictor = TimeSeriesPredictor(method='historical_mean')
        predictor.fit(self.returns)
        
        pred_daily = predictor.get_predictions(annualize=False)
        pred_annual = predictor.get_predictions(annualize=True, periods_per_year=252)
        
        # Returns should be scaled by periods_per_year
        self.assertTrue(np.allclose(
            pred_annual['returns'].values,
            pred_daily['returns'].values * 252
        ))
        
        # Covariance should be scaled by periods_per_year
        self.assertTrue(np.allclose(
            pred_annual['covariance'].values,
            pred_daily['covariance'].values * 252
        ))
    
    def test_invalid_method(self):
        """Test that invalid method raises error."""
        predictor = TimeSeriesPredictor(method='invalid_method')
        predictor.fit(self.returns)
        
        with self.assertRaises(ValueError):
            predictor.predict_returns()


if __name__ == '__main__':
    unittest.main()
