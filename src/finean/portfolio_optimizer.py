"""
Portfolio optimization module for maximizing yield given variability constraints.

Implements various portfolio optimization strategies including:
- Maximum Sharpe Ratio (risk-adjusted return)
- Minimum Volatility
- Maximum Return for given risk
- Efficient Frontier calculation
"""

import numpy as np
import pandas as pd
from typing import Optional, Dict, List, Tuple
from scipy.optimize import minimize
import warnings


class PortfolioOptimizer:
    """
    Portfolio optimizer for finding optimal asset allocations.
    
    This class implements portfolio optimization techniques to maximize
    yield given variability constraints, using predicted returns and
    covariance from time series analysis.
    """
    
    def __init__(self, expected_returns: pd.Series, 
                 covariance_matrix: pd.DataFrame,
                 risk_free_rate: float = 0.0):
        """
        Initialize the portfolio optimizer.
        
        Parameters:
        -----------
        expected_returns : pd.Series
            Expected returns for each asset (annualized)
        covariance_matrix : pd.DataFrame
            Covariance matrix of asset returns (annualized)
        risk_free_rate : float, default=0.0
            Risk-free rate (annualized)
        """
        self.expected_returns = expected_returns
        self.cov_matrix = covariance_matrix
        self.risk_free_rate = risk_free_rate
        self.assets = expected_returns.index.tolist()
        self.n_assets = len(self.assets)
        
        # Validate inputs
        if not np.allclose(self.cov_matrix, self.cov_matrix.T):
            warnings.warn("Covariance matrix is not symmetric. Symmetrizing it.")
            self.cov_matrix = (self.cov_matrix + self.cov_matrix.T) / 2
    
    def optimize_max_sharpe(self, constraints: Optional[Dict] = None) -> Dict:
        """
        Optimize portfolio for maximum Sharpe ratio.
        
        This finds the portfolio that maximizes risk-adjusted returns
        (return per unit of risk).
        
        Parameters:
        -----------
        constraints : dict, optional
            Additional constraints:
            - 'max_weight': Maximum weight per asset (default: 1.0)
            - 'min_weight': Minimum weight per asset (default: 0.0)
            - 'long_only': Boolean, whether to allow short selling (default: True)
            
        Returns:
        --------
        dict
            Optimization results including:
            - 'weights': Optimal portfolio weights
            - 'expected_return': Expected portfolio return
            - 'volatility': Portfolio volatility
            - 'sharpe_ratio': Portfolio Sharpe ratio
        """
        # Set default constraints
        if constraints is None:
            constraints = {}
        
        max_weight = constraints.get('max_weight', 1.0)
        min_weight = constraints.get('min_weight', 0.0)
        long_only = constraints.get('long_only', True)
        
        # Initial guess: equal weights
        x0 = np.array([1.0 / self.n_assets] * self.n_assets)
        
        # Bounds for weights
        if long_only:
            bounds = tuple((min_weight, max_weight) for _ in range(self.n_assets))
        else:
            bounds = tuple((-max_weight, max_weight) for _ in range(self.n_assets))
        
        # Constraints: weights sum to 1
        constraint = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1.0}
        
        # Objective: negative Sharpe ratio (to minimize)
        def neg_sharpe(weights):
            return -self._calculate_sharpe_ratio(weights)
        
        # Optimize
        result = minimize(
            neg_sharpe,
            x0,
            method='SLSQP',
            bounds=bounds,
            constraints=constraint,
            options={'maxiter': 1000, 'ftol': 1e-9}
        )
        
        if not result.success:
            warnings.warn(f"Optimization did not converge: {result.message}")
        
        # Extract results
        optimal_weights = pd.Series(result.x, index=self.assets)
        portfolio_return = self._calculate_portfolio_return(result.x)
        portfolio_vol = self._calculate_portfolio_volatility(result.x)
        sharpe = self._calculate_sharpe_ratio(result.x)
        
        return {
            'weights': optimal_weights,
            'expected_return': portfolio_return,
            'volatility': portfolio_vol,
            'sharpe_ratio': sharpe,
            'optimization_success': result.success
        }
    
    def optimize_min_volatility(self, constraints: Optional[Dict] = None) -> Dict:
        """
        Optimize portfolio for minimum volatility.
        
        This finds the portfolio with the lowest risk.
        
        Parameters:
        -----------
        constraints : dict, optional
            Additional constraints (same as optimize_max_sharpe)
            
        Returns:
        --------
        dict
            Optimization results
        """
        # Set default constraints
        if constraints is None:
            constraints = {}
        
        max_weight = constraints.get('max_weight', 1.0)
        min_weight = constraints.get('min_weight', 0.0)
        long_only = constraints.get('long_only', True)
        
        # Initial guess: equal weights
        x0 = np.array([1.0 / self.n_assets] * self.n_assets)
        
        # Bounds for weights
        if long_only:
            bounds = tuple((min_weight, max_weight) for _ in range(self.n_assets))
        else:
            bounds = tuple((-max_weight, max_weight) for _ in range(self.n_assets))
        
        # Constraints: weights sum to 1
        constraint = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1.0}
        
        # Objective: portfolio volatility
        def portfolio_vol(weights):
            return self._calculate_portfolio_volatility(weights)
        
        # Optimize
        result = minimize(
            portfolio_vol,
            x0,
            method='SLSQP',
            bounds=bounds,
            constraints=constraint,
            options={'maxiter': 1000, 'ftol': 1e-9}
        )
        
        if not result.success:
            warnings.warn(f"Optimization did not converge: {result.message}")
        
        # Extract results
        optimal_weights = pd.Series(result.x, index=self.assets)
        portfolio_return = self._calculate_portfolio_return(result.x)
        portfolio_vol = self._calculate_portfolio_volatility(result.x)
        sharpe = self._calculate_sharpe_ratio(result.x)
        
        return {
            'weights': optimal_weights,
            'expected_return': portfolio_return,
            'volatility': portfolio_vol,
            'sharpe_ratio': sharpe,
            'optimization_success': result.success
        }
    
    def optimize_max_return(self, constraints: Optional[Dict] = None) -> Dict:
        """
        Optimize portfolio for maximum return (without risk adjustment).
        
        This finds the portfolio with the highest expected return,
        without considering risk or the Sharpe ratio. This typically
        results in concentrated positions in the highest-return assets.
        
        Parameters:
        -----------
        constraints : dict, optional
            Additional constraints (same as optimize_max_sharpe)
            
        Returns:
        --------
        dict
            Optimization results
        """
        # Set default constraints
        if constraints is None:
            constraints = {}
        
        max_weight = constraints.get('max_weight', 1.0)
        min_weight = constraints.get('min_weight', 0.0)
        long_only = constraints.get('long_only', True)
        
        # Initial guess: equal weights
        x0 = np.array([1.0 / self.n_assets] * self.n_assets)
        
        # Bounds for weights
        if long_only:
            bounds = tuple((min_weight, max_weight) for _ in range(self.n_assets))
        else:
            bounds = tuple((-max_weight, max_weight) for _ in range(self.n_assets))
        
        # Constraints: weights sum to 1
        constraint = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1.0}
        
        # Objective: negative return (to minimize)
        def neg_return(weights):
            return -self._calculate_portfolio_return(weights)
        
        # Optimize
        result = minimize(
            neg_return,
            x0,
            method='SLSQP',
            bounds=bounds,
            constraints=constraint,
            options={'maxiter': 1000, 'ftol': 1e-9}
        )
        
        if not result.success:
            warnings.warn(f"Optimization did not converge: {result.message}")
        
        # Extract results
        optimal_weights = pd.Series(result.x, index=self.assets)
        portfolio_return = self._calculate_portfolio_return(result.x)
        portfolio_vol = self._calculate_portfolio_volatility(result.x)
        sharpe = self._calculate_sharpe_ratio(result.x)
        
        return {
            'weights': optimal_weights,
            'expected_return': portfolio_return,
            'volatility': portfolio_vol,
            'sharpe_ratio': sharpe,
            'optimization_success': result.success
        }
    
    def optimize_max_return_for_risk(self, target_volatility: float,
                                     constraints: Optional[Dict] = None) -> Dict:
        """
        Optimize portfolio for maximum return given a target volatility.
        
        This finds the portfolio that maximizes return while keeping
        volatility at or below the target level.
        
        Parameters:
        -----------
        target_volatility : float
            Target portfolio volatility (standard deviation)
        constraints : dict, optional
            Additional constraints (same as optimize_max_sharpe)
            
        Returns:
        --------
        dict
            Optimization results
        """
        # Set default constraints
        if constraints is None:
            constraints = {}
        
        max_weight = constraints.get('max_weight', 1.0)
        min_weight = constraints.get('min_weight', 0.0)
        long_only = constraints.get('long_only', True)
        
        # Initial guess: equal weights
        x0 = np.array([1.0 / self.n_assets] * self.n_assets)
        
        # Bounds for weights
        if long_only:
            bounds = tuple((min_weight, max_weight) for _ in range(self.n_assets))
        else:
            bounds = tuple((-max_weight, max_weight) for _ in range(self.n_assets))
        
        # Constraints: weights sum to 1, volatility <= target
        constraints_list = [
            {'type': 'eq', 'fun': lambda x: np.sum(x) - 1.0},
            {'type': 'ineq', 'fun': lambda x: target_volatility - self._calculate_portfolio_volatility(x)}
        ]
        
        # Objective: negative return (to minimize)
        def neg_return(weights):
            return -self._calculate_portfolio_return(weights)
        
        # Optimize
        result = minimize(
            neg_return,
            x0,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints_list,
            options={'maxiter': 1000, 'ftol': 1e-9}
        )
        
        if not result.success:
            warnings.warn(f"Optimization did not converge: {result.message}")
        
        # Extract results
        optimal_weights = pd.Series(result.x, index=self.assets)
        portfolio_return = self._calculate_portfolio_return(result.x)
        portfolio_vol = self._calculate_portfolio_volatility(result.x)
        sharpe = self._calculate_sharpe_ratio(result.x)
        
        return {
            'weights': optimal_weights,
            'expected_return': portfolio_return,
            'volatility': portfolio_vol,
            'sharpe_ratio': sharpe,
            'optimization_success': result.success
        }
    
    def calculate_efficient_frontier(self, n_points: int = 100,
                                     constraints: Optional[Dict] = None) -> pd.DataFrame:
        """
        Calculate the efficient frontier.
        
        The efficient frontier represents the set of optimal portfolios
        that offer the highest expected return for a given level of risk.
        
        Parameters:
        -----------
        n_points : int, default=100
            Number of points to calculate on the efficient frontier
        constraints : dict, optional
            Additional constraints (same as optimize_max_sharpe)
            
        Returns:
        --------
        pd.DataFrame
            DataFrame with columns: volatility, expected_return, sharpe_ratio
        """
        # Find min and max volatility portfolios
        min_vol_result = self.optimize_min_volatility(constraints)
        max_sharpe_result = self.optimize_max_sharpe(constraints)
        
        min_vol = min_vol_result['volatility']
        max_vol = max_sharpe_result['volatility'] * 2  # Extend beyond max Sharpe
        
        # Generate target volatilities
        target_vols = np.linspace(min_vol, max_vol, n_points)
        
        # Calculate optimal portfolios for each target volatility
        results = []
        for target_vol in target_vols:
            try:
                result = self.optimize_max_return_for_risk(target_vol, constraints)
                results.append({
                    'volatility': result['volatility'],
                    'expected_return': result['expected_return'],
                    'sharpe_ratio': result['sharpe_ratio']
                })
            except:
                # Skip if optimization fails for this point
                continue
        
        return pd.DataFrame(results)
    
    def _calculate_portfolio_return(self, weights: np.ndarray) -> float:
        """Calculate expected portfolio return."""
        return np.dot(weights, self.expected_returns)
    
    def _calculate_portfolio_volatility(self, weights: np.ndarray) -> float:
        """Calculate portfolio volatility (standard deviation)."""
        variance = np.dot(weights, np.dot(self.cov_matrix, weights))
        return np.sqrt(variance)
    
    def _calculate_sharpe_ratio(self, weights: np.ndarray) -> float:
        """Calculate portfolio Sharpe ratio."""
        portfolio_return = self._calculate_portfolio_return(weights)
        portfolio_vol = self._calculate_portfolio_volatility(weights)
        
        if portfolio_vol == 0:
            return 0.0
        
        return (portfolio_return - self.risk_free_rate) / portfolio_vol
    
    def get_portfolio_statistics(self, weights: pd.Series) -> Dict:
        """
        Calculate statistics for a given portfolio.
        
        Parameters:
        -----------
        weights : pd.Series
            Portfolio weights
            
        Returns:
        --------
        dict
            Portfolio statistics
        """
        weights_array = weights.values
        
        return {
            'expected_return': self._calculate_portfolio_return(weights_array),
            'volatility': self._calculate_portfolio_volatility(weights_array),
            'sharpe_ratio': self._calculate_sharpe_ratio(weights_array)
        }
