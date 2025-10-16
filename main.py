"""
Main script para optimización de portafolio con datos reales de mercado.

Este script permite:
1. Descargar datos históricos de acciones reales usando yfinance
2. Calcular retornos esperados y matriz de covarianza
3. Optimizar el portafolio para maximizar el ratio de Sharpe
4. Mostrar los pesos óptimos y métricas del portafolio
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
    """
    Descarga datos históricos de acciones usando yfinance.
    
    Parameters:
    -----------
    tickers : list
        Lista de símbolos de acciones (ej: ['AAPL', 'GOOGL', 'MSFT'])
    period : str
        Periodo de datos ('1y', '2y', '5y', etc.)
    interval : str
        Intervalo de tiempo ('1d', '1wk', '1mo')
    
    Returns:
    --------
    pd.DataFrame
        DataFrame con precios de cierre ajustados
    """
    print(f"\n{'='*70}")
    print(f"Descargando datos históricos para: {', '.join(tickers)}")
    print(f"Periodo: {period}, Intervalo: {interval}")
    print(f"{'='*70}\n")
    
    try:
        # Descargar datos
        data = yf.download(tickers, period=period, interval=interval, progress=False, auto_adjust=True)
        
        # Si hay un solo ticker, yfinance devuelve una estructura diferente
        if len(tickers) == 1:
            prices = data['Close'].to_frame()
            prices.columns = tickers
        else:
            # Usar precios de cierre (auto_adjust=True ya ajusta los precios)
            prices = data['Close']
        
        # Eliminar filas con datos faltantes
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
    """
    Calcula retornos esperados y matriz de covarianza a partir de precios.
    
    Parameters:
    -----------
    prices : pd.DataFrame
        DataFrame con precios históricos
    risk_free_rate : float
        Tasa libre de riesgo (anualizada)
    
    Returns:
    --------
    tuple
        (expected_returns, covariance_matrix)
    """
    print(f"{'='*70}")
    print("Calculando métricas del portafolio...")
    print(f"{'='*70}\n")
    
    # Calcular retornos diarios
    returns = calculate_returns(prices, method='simple')
    
    # Calcular retornos esperados anualizados (promedio * 252 días de trading)
    expected_returns = returns.mean() * 252
    
    # Calcular matriz de covarianza anualizada
    covariance_matrix = returns.cov() * 252
    
    # Mostrar estadísticas
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


def optimize_portfolio(expected_returns: pd.Series, 
                      covariance_matrix: pd.DataFrame,
                      risk_free_rate: float = 0.02,
                      min_weight: float = 0.0,
                      max_weight: float = 1.0) -> dict:
    """
    Optimiza el portafolio para maximizar el ratio de Sharpe.
    
    Parameters:
    -----------
    expected_returns : pd.Series
        Retornos esperados anualizados
    covariance_matrix : pd.DataFrame
        Matriz de covarianza anualizada
    risk_free_rate : float
        Tasa libre de riesgo
    min_weight : float
        Peso mínimo por activo
    max_weight : float
        Peso máximo por activo
    
    Returns:
    --------
    dict
        Resultados de la optimización
    """
    print(f"{'='*70}")
    print("Optimizando portafolio (Maximizar Ratio de Sharpe)...")
    print(f"{'='*70}\n")
    
    # Crear optimizador
    optimizer = PortfolioOptimizer(
        expected_returns=expected_returns,
        covariance_matrix=covariance_matrix,
        risk_free_rate=risk_free_rate
    )
    
    # Optimizar para máximo ratio de Sharpe
    constraints = {
        'min_weight': min_weight,
        'max_weight': max_weight,
        'long_only': True
    }
    
    result = optimizer.optimize_max_sharpe(constraints=constraints)
    
    return result


def print_optimization_results(result: dict):
    """
    Imprime los resultados de la optimización de forma legible.
    
    Parameters:
    -----------
    result : dict
        Diccionario con resultados de la optimización
    """
    print(f"{'='*70}")
    print("RESULTADOS DE LA OPTIMIZACIÓN")
    print(f"{'='*70}\n")
    
    if not result['optimization_success']:
        print("⚠️  ADVERTENCIA: La optimización no convergió completamente\n")
    
    print("Pesos Óptimos del Portafolio:")
    print("-" * 70)
    weights = result['weights']
    for ticker, weight in weights.items():
        bar = '█' * int(weight * 50)
        print(f"  {ticker:8s}: {weight*100:6.2f}% {bar}")
    
    print(f"\nMétricas del Portafolio Óptimo:")
    print("-" * 70)
    print(f"  Retorno Esperado:  {result['expected_return']*100:7.2f}% anual")
    print(f"  Volatilidad:       {result['volatility']*100:7.2f}% anual")
    print(f"  Ratio de Sharpe:   {result['sharpe_ratio']:7.2f}")
    
    print(f"\n{'='*70}\n")


def main():
    """
    Función principal para ejecutar la optimización de portafolio.
    """
    print("\n" + "="*70)
    print(" "*15 + "OPTIMIZACIÓN DE PORTAFOLIO - FINEAN")
    print("="*70 + "\n")
    
    # ========================================================================
    # CONFIGURACIÓN - ¡Modifica estos parámetros según tus necesidades!
    # ========================================================================
    
    # Lista de tickers de acciones (puedes agregar o quitar tickers)
    TICKERS = [
        'GLD',    # SPDR Gold Trust (Oro)
        'SPY',    # SPDR S&P 500 ETF (Acciones USA)
        'BIL',    # SPDR Bloomberg 1-3 Month T-Bill ETF (Bonos corto plazo)
    ]
    
    # Parámetros de descarga de datos
    PERIOD = '2y'        # Periodo: '1y', '2y', '5y', '10y', 'max'
    INTERVAL = '1d'      # Intervalo: '1d' (diario), '1wk' (semanal), '1mo' (mensual)
    
    # Parámetros de optimización
    RISK_FREE_RATE = 0.04  # Tasa libre de riesgo (4% anual)
    MIN_WEIGHT = 0.0       # Peso mínimo por activo (0 = permitir 0%)
    MAX_WEIGHT = 0.40      # Peso máximo por activo (0.4 = máximo 40%)
    
    # ========================================================================
    
    try:
        # Paso 1: Descargar datos históricos
        prices = download_stock_data(TICKERS, period=PERIOD, interval=INTERVAL)
        
        # Paso 2: Calcular métricas
        expected_returns, covariance_matrix = calculate_portfolio_metrics(
            prices, 
            risk_free_rate=RISK_FREE_RATE
        )
        
        # Paso 3: Optimizar portafolio
        result = optimize_portfolio(
            expected_returns,
            covariance_matrix,
            risk_free_rate=RISK_FREE_RATE,
            min_weight=MIN_WEIGHT,
            max_weight=MAX_WEIGHT
        )
        
        # Paso 4: Mostrar resultados
        print_optimization_results(result)
        
        # Información adicional
        print("INSTRUCCIONES:")
        print("-" * 70)
        print("Para cambiar los activos a optimizar, modifica la lista TICKERS")
        print("en la función main().")
        print("\nPuedes usar cualquier ticker válido de Yahoo Finance:")
        print("  - Acciones: AAPL, MSFT, GOOGL, etc.")
        print("  - ETFs: SPY, QQQ, VTI, etc.")
        print("  - Criptomonedas: BTC-USD, ETH-USD, etc.")
        print("  - Divisas: EURUSD=X, GBPUSD=X, etc.")
        print(f"{'='*70}\n")
        
    except Exception as e:
        print(f"\n✗ Error durante la ejecución: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
