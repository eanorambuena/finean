"""
Example script demonstrating portfolio optimization with time series predictions.

This example shows how to:
1. Generate or load historical price data
2. Use time series prediction to forecast returns
3. Optimize portfolio for maximum Sharpe ratio
4. Calculate the efficient frontier
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from finean import PortfolioOptimizer, TimeSeriesPredictor
from finean.utils import calculate_returns


def generate_sample_data(n_days: int = 1000, n_assets: int = 5) -> pd.DataFrame:
    """
    Generate sample price data for demonstration.
    
    Parameters:
    -----------
    n_days : int
        Number of days of historical data
    n_assets : int
        Number of assets
        
    Returns:
    --------
    pd.DataFrame
        Sample price data
    """
    np.random.seed(42)
    
    # Generate asset names
    assets = [f'Asset_{i+1}' for i in range(n_assets)]
    
    # Parameters for each asset
    initial_prices = np.random.uniform(50, 150, n_assets)
    annual_returns = np.random.uniform(0.05, 0.20, n_assets)
    annual_vols = np.random.uniform(0.15, 0.35, n_assets)
    
    # Daily parameters
    daily_returns = annual_returns / 252
    daily_vols = annual_vols / np.sqrt(252)
    
    # Generate correlation matrix
    corr_matrix = np.random.uniform(-0.5, 0.8, (n_assets, n_assets))
    corr_matrix = (corr_matrix + corr_matrix.T) / 2
    np.fill_diagonal(corr_matrix, 1.0)
    
    # Generate returns using multivariate normal
    returns = np.random.multivariate_normal(
        daily_returns,
        np.outer(daily_vols, daily_vols) * corr_matrix,
        n_days
    )
    
    # Convert to prices
    prices = np.zeros((n_days, n_assets))
    prices[0] = initial_prices
    
    for i in range(1, n_days):
        prices[i] = prices[i-1] * (1 + returns[i])
    
    # Create DataFrame
    dates = pd.date_range(start='2020-01-01', periods=n_days, freq='D')
    price_df = pd.DataFrame(prices, index=dates, columns=assets)
    
    return price_df


def main():
    """Main function demonstrating portfolio optimization."""
    
    print("=" * 80)
    print("Investment Portfolio Optimization Example")
    print("Maximum Yield Given Variability with Time Series Predictions")
    print("=" * 80)
    print()
    
    # Step 1: Generate or load historical price data
    print("Step 1: Generating sample price data...")
    prices = generate_sample_data(n_days=1000, n_assets=5)
    print(f"Generated {len(prices)} days of data for {len(prices.columns)} assets")
    print(f"Date range: {prices.index[0].date()} to {prices.index[-1].date()}")
    print()
    
    # Calculate returns
    print("Step 2: Calculating historical returns...")
    returns = calculate_returns(prices, method='simple')
    print(f"Returns shape: {returns.shape}")
    print(f"Mean daily returns:\n{returns.mean()}")
    print()
    
    # Step 3: Use time series predictor to forecast returns
    print("Step 3: Using time series predictor to forecast returns...")
    predictor = TimeSeriesPredictor(method='ewma')
    predictor.fit(returns, span=60)
    
    predictions = predictor.get_predictions(annualize=True, periods_per_year=252)
    expected_returns = predictions['returns']
    cov_matrix = predictions['covariance']
    
    print("Expected Annual Returns:")
    for asset, ret in expected_returns.items():
        print(f"  {asset}: {ret*100:.2f}%")
    print()
    
    # Step 4: Optimize portfolio
    print("Step 4: Optimizing portfolio for maximum Sharpe ratio...")
    optimizer = PortfolioOptimizer(
        expected_returns=expected_returns,
        covariance_matrix=cov_matrix,
        risk_free_rate=0.02  # 2% risk-free rate
    )
    
    # Maximum Sharpe ratio portfolio
    max_sharpe_result = optimizer.optimize_max_sharpe(
        constraints={'long_only': True, 'min_weight': 0.0, 'max_weight': 0.5}
    )
    
    print("\nMaximum Sharpe Ratio Portfolio:")
    print("-" * 60)
    print("Optimal Weights:")
    for asset, weight in max_sharpe_result['weights'].items():
        if weight > 0.001:  # Only show non-negligible weights
            print(f"  {asset}: {weight*100:.2f}%")
    print(f"\nExpected Annual Return: {max_sharpe_result['expected_return']*100:.2f}%")
    print(f"Annual Volatility: {max_sharpe_result['volatility']*100:.2f}%")
    print(f"Sharpe Ratio: {max_sharpe_result['sharpe_ratio']:.3f}")
    print()
    
    # Minimum volatility portfolio
    print("Step 5: Finding minimum volatility portfolio...")
    min_vol_result = optimizer.optimize_min_volatility(
        constraints={'long_only': True}
    )
    
    print("\nMinimum Volatility Portfolio:")
    print("-" * 60)
    print("Optimal Weights:")
    for asset, weight in min_vol_result['weights'].items():
        if weight > 0.001:
            print(f"  {asset}: {weight*100:.2f}%")
    print(f"\nExpected Annual Return: {min_vol_result['expected_return']*100:.2f}%")
    print(f"Annual Volatility: {min_vol_result['volatility']*100:.2f}%")
    print(f"Sharpe Ratio: {min_vol_result['sharpe_ratio']:.3f}")
    print()
    
    # Step 6: Calculate efficient frontier
    print("Step 6: Calculating efficient frontier...")
    efficient_frontier = optimizer.calculate_efficient_frontier(
        n_points=50,
        constraints={'long_only': True}
    )
    print(f"Calculated {len(efficient_frontier)} points on the efficient frontier")
    print()
    
    # Step 7: Visualize results
    print("Step 7: Creating visualization...")
    try:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Plot 1: Efficient Frontier
        ax1.plot(efficient_frontier['volatility'] * 100, 
                efficient_frontier['expected_return'] * 100,
                'b-', linewidth=2, label='Efficient Frontier')
        ax1.scatter(max_sharpe_result['volatility'] * 100,
                   max_sharpe_result['expected_return'] * 100,
                   c='red', s=200, marker='*', label='Max Sharpe Ratio', zorder=3)
        ax1.scatter(min_vol_result['volatility'] * 100,
                   min_vol_result['expected_return'] * 100,
                   c='green', s=200, marker='s', label='Min Volatility', zorder=3)
        ax1.set_xlabel('Annual Volatility (%)', fontsize=12)
        ax1.set_ylabel('Expected Annual Return (%)', fontsize=12)
        ax1.set_title('Efficient Frontier', fontsize=14, fontweight='bold')
        ax1.legend(fontsize=10)
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Portfolio Weights
        weights_df = pd.DataFrame({
            'Max Sharpe': max_sharpe_result['weights'],
            'Min Volatility': min_vol_result['weights']
        })
        
        weights_df.plot(kind='bar', ax=ax2)
        ax2.set_xlabel('Assets', fontsize=12)
        ax2.set_ylabel('Weight', fontsize=12)
        ax2.set_title('Optimal Portfolio Weights', fontsize=14, fontweight='bold')
        ax2.legend(fontsize=10)
        ax2.grid(True, alpha=0.3, axis='y')
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        
        # Save figure
        output_path = os.path.join(os.path.dirname(__file__), 'portfolio_optimization_results.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Visualization saved to: {output_path}")
        
    except Exception as e:
        print(f"Could not create visualization: {e}")
    
    print()
    print("=" * 80)
    print("Portfolio Optimization Complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()
