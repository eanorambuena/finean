"""
Script avanzado de optimización de portafolio con múltiples estrategias.

Este script permite:
1. Descargar datos históricos de acciones reales
2. Optimizar para Máximo Sharpe Ratio
3. Optimizar para Mínima Volatilidad
4. Comparar ambas estrategias
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
from finean import PortfolioOptimizer
from finean.utils import calculate_returns, calculate_volatility


def download_stock_data(tickers: list, period: str = '2y', interval: str = '1d') -> pd.DataFrame:
    """Descarga datos históricos de acciones usando yfinance."""
    print(f"\n{'='*70}")
    print(f"Descargando datos históricos para: {', '.join(tickers)}")
    print(f"Periodo: {period}, Intervalo: {interval}")
    print(f"{'='*70}\n")
    
    try:
        data = yf.download(tickers, period=period, interval=interval, progress=False, auto_adjust=True)
        
        if len(tickers) == 1:
            prices = data['Close'].to_frame()
            prices.columns = tickers
        else:
            prices = data['Close']
        
        prices = prices.dropna()
        
        print(f"✓ Datos descargados exitosamente")
        print(f"  - Periodo: {prices.index[0].date()} a {prices.index[-1].date()}")
        print(f"  - Días de trading: {len(prices)}")
        print(f"  - Activos: {len(tickers)}\n")
        
        return prices
    
    except Exception as e:
        print(f"✗ Error al descargar datos: {e}")
        raise


def calculate_portfolio_metrics(prices: pd.DataFrame, risk_free_rate: float = 0.02) -> tuple:
    """Calcula retornos esperados y matriz de covarianza."""
    print(f"{'='*70}")
    print("Calculando métricas del portafolio...")
    print(f"{'='*70}\n")
    
    returns = calculate_returns(prices, method='simple')
    expected_returns = returns.mean() * 252
    covariance_matrix = returns.cov() * 252
    
    print("Retornos Esperados Anualizados:")
    print("-" * 70)
    for ticker, ret in expected_returns.items():
        print(f"  {ticker:8s}: {ret*100:7.2f}%")
    
    print(f"\nVolatilidad Anualizada:")
    print("-" * 70)
    volatilities = np.sqrt(np.diag(covariance_matrix))
    for ticker, vol in zip(expected_returns.index, volatilities):
        print(f"  {ticker:8s}: {vol*100:7.2f}%")
    
    print(f"\nMatriz de Correlación:")
    print("-" * 70)
    correlation_matrix = returns.corr()
    print(correlation_matrix.round(3))
    print()
    
    return expected_returns, covariance_matrix


def print_portfolio_results(title: str, result: dict):
    """Imprime los resultados de optimización de forma legible."""
    print(f"{'='*70}")
    print(f"{title}")
    print(f"{'='*70}\n")
    
    if not result['optimization_success']:
        print("⚠️  ADVERTENCIA: La optimización no convergió completamente\n")
    
    print("Pesos del Portafolio:")
    print("-" * 70)
    weights = result['weights']
    
    # Ordenar por peso descendente
    sorted_weights = weights.sort_values(ascending=False)
    
    for ticker, weight in sorted_weights.items():
        if weight > 0.001:  # Solo mostrar pesos significativos
            bar = '█' * int(weight * 50)
            print(f"  {ticker:8s}: {weight*100:6.2f}% {bar}")
    
    print(f"\nMétricas del Portafolio:")
    print("-" * 70)
    print(f"  Retorno Esperado:  {result['expected_return']*100:7.2f}% anual")
    print(f"  Volatilidad:       {result['volatility']*100:7.2f}% anual")
    print(f"  Ratio de Sharpe:   {result['sharpe_ratio']:7.2f}")
    print()


def compare_strategies(max_sharpe_result: dict, min_vol_result: dict):
    """Compara las dos estrategias de optimización."""
    print(f"{'='*70}")
    print("COMPARACIÓN DE ESTRATEGIAS")
    print(f"{'='*70}\n")
    
    print(f"{'Métrica':<25} {'Max Sharpe':>15} {'Min Volatilidad':>15} {'Diferencia':>12}")
    print("-" * 70)
    
    ret_sharpe = max_sharpe_result['expected_return'] * 100
    ret_minvol = min_vol_result['expected_return'] * 100
    print(f"{'Retorno Esperado (%)':<25} {ret_sharpe:>15.2f} {ret_minvol:>15.2f} {ret_sharpe-ret_minvol:>12.2f}")
    
    vol_sharpe = max_sharpe_result['volatility'] * 100
    vol_minvol = min_vol_result['volatility'] * 100
    print(f"{'Volatilidad (%)':<25} {vol_sharpe:>15.2f} {vol_minvol:>15.2f} {vol_sharpe-vol_minvol:>12.2f}")
    
    sharpe_sharpe = max_sharpe_result['sharpe_ratio']
    sharpe_minvol = min_vol_result['sharpe_ratio']
    print(f"{'Ratio de Sharpe':<25} {sharpe_sharpe:>15.2f} {sharpe_minvol:>15.2f} {sharpe_sharpe-sharpe_minvol:>12.2f}")
    
    print(f"\n{'='*70}\n")
    
    # Recomendación
    print("RECOMENDACIÓN:")
    print("-" * 70)
    if sharpe_sharpe > sharpe_minvol * 1.1:
        print("✓ El portafolio de MÁXIMO SHARPE ofrece mejor retorno ajustado por riesgo.")
        print("  Recomendado para inversores que buscan maximizar eficiencia.")
    elif vol_minvol < vol_sharpe * 0.8:
        print("✓ El portafolio de MÍNIMA VOLATILIDAD ofrece mucho menor riesgo.")
        print("  Recomendado para inversores conservadores que priorizan estabilidad.")
    else:
        print("≈ Ambas estrategias ofrecen perfiles similares de riesgo-retorno.")
        print("  La elección depende de tu tolerancia al riesgo personal.")
    
    print(f"\n{'='*70}\n")


def main():
    """Función principal para ejecutar la optimización avanzada."""
    print("\n" + "="*70)
    print(" "*10 + "OPTIMIZACIÓN AVANZADA DE PORTAFOLIO - FINEAN")
    print("="*70 + "\n")
    
    # ========================================================================
    # CONFIGURACIÓN
    # ========================================================================
    
    # Lista de tickers
    TICKERS = [
        'GLD',    # SPDR Gold Trust (Oro)
        'SPY',    # SPDR S&P 500 ETF (Acciones USA)
        'BIL',    # SPDR Bloomberg 1-3 Month T-Bill ETF (Bonos corto plazo)
    ]
    
    # Parámetros
    PERIOD = '2y'
    INTERVAL = '1d'
    RISK_FREE_RATE = 0.04
    MIN_WEIGHT = 0.0
    MAX_WEIGHT = 0.40
    
    # ========================================================================
    
    try:
        # Paso 1: Descargar datos
        prices = download_stock_data(TICKERS, period=PERIOD, interval=INTERVAL)
        
        # Paso 2: Calcular métricas
        expected_returns, covariance_matrix = calculate_portfolio_metrics(
            prices, 
            risk_free_rate=RISK_FREE_RATE
        )
        
        # Paso 3: Crear optimizador
        optimizer = PortfolioOptimizer(
            expected_returns=expected_returns,
            covariance_matrix=covariance_matrix,
            risk_free_rate=RISK_FREE_RATE
        )
        
        constraints = {
            'min_weight': MIN_WEIGHT,
            'max_weight': MAX_WEIGHT,
            'long_only': True
        }
        
        # Paso 4: Optimización para Máximo Sharpe
        print(f"{'='*70}")
        print("ESTRATEGIA 1: Maximizar Ratio de Sharpe")
        print(f"{'='*70}\n")
        print("Optimizando para mejor retorno ajustado por riesgo...\n")
        
        max_sharpe_result = optimizer.optimize_max_sharpe(constraints=constraints)
        print_portfolio_results("PORTAFOLIO ÓPTIMO: MÁXIMO SHARPE RATIO", max_sharpe_result)
        
        # Paso 5: Optimización para Mínima Volatilidad
        print(f"{'='*70}")
        print("ESTRATEGIA 2: Minimizar Volatilidad")
        print(f"{'='*70}\n")
        print("Optimizando para mínimo riesgo...\n")
        
        min_vol_result = optimizer.optimize_min_volatility(constraints=constraints)
        print_portfolio_results("PORTAFOLIO ÓPTIMO: MÍNIMA VOLATILIDAD", min_vol_result)
        
        # Paso 6: Comparar estrategias
        compare_strategies(max_sharpe_result, min_vol_result)
        
        # Información adicional
        print("NOTAS:")
        print("-" * 70)
        print("• El portafolio de Máximo Sharpe busca la mejor eficiencia (retorno/riesgo)")
        print("• El portafolio de Mínima Volatilidad busca reducir el riesgo al mínimo")
        print("• Los retornos son anualizados basados en datos históricos")
        print("• La optimización está sujeta a las restricciones de peso configuradas")
        print(f"  (mín: {MIN_WEIGHT*100:.0f}%, máx: {MAX_WEIGHT*100:.0f}% por activo)")
        print(f"\n{'='*70}\n")
        
    except Exception as e:
        print(f"\n✗ Error durante la ejecución: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
