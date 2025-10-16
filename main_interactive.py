"""
Script interactivo de optimización de portafolio.

Permite al usuario ingresar sus propios tickers de forma interactiva.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import numpy as np
import pandas as pd
import yfinance as yf
from finean import PortfolioOptimizer
from finean.utils import calculate_returns


def get_user_input():
    """Solicita al usuario los parámetros de optimización."""
    print("\n" + "="*70)
    print(" "*15 + "OPTIMIZACIÓN INTERACTIVA DE PORTAFOLIO")
    print("="*70 + "\n")
    
    # Obtener tickers
    print("PASO 1: Selección de Activos")
    print("-" * 70)
    print("Ingresa los símbolos de las acciones que deseas incluir en el portafolio.")
    print("Ejemplos: AAPL, MSFT, GOOGL, AMZN, TSLA, JPM, etc.")
    print("Puedes ingresar entre 2 y 20 activos.\n")
    
    while True:
        tickers_input = input("Tickers (separados por comas): ").strip()
        tickers = [t.strip().upper() for t in tickers_input.split(',') if t.strip()]
        
        if len(tickers) < 2:
            print("⚠️  Debes ingresar al menos 2 activos. Intenta de nuevo.\n")
        elif len(tickers) > 20:
            print("⚠️  Máximo 20 activos. Intenta de nuevo.\n")
        else:
            break
    
    print(f"\n✓ Seleccionados {len(tickers)} activos: {', '.join(tickers)}\n")
    
    # Obtener periodo
    print("PASO 2: Periodo de Datos Históricos")
    print("-" * 70)
    print("Opciones: 1y (1 año), 2y (2 años), 5y (5 años), 10y (10 años)")
    
    while True:
        period = input("Periodo [2y]: ").strip() or '2y'
        if period in ['1y', '2y', '3y', '5y', '10y', 'max']:
            break
        print("⚠️  Periodo inválido. Usa: 1y, 2y, 5y, 10y, o max\n")
    
    print(f"✓ Periodo seleccionado: {period}\n")
    
    # Obtener tasa libre de riesgo
    print("PASO 3: Tasa Libre de Riesgo")
    print("-" * 70)
    print("La tasa libre de riesgo se usa para calcular el Ratio de Sharpe.")
    print("Ejemplo: 0.04 para 4% anual (aproximado a bonos del tesoro USA)")
    
    while True:
        try:
            rfr_input = input("Tasa libre de riesgo [0.04]: ").strip() or '0.04'
            risk_free_rate = float(rfr_input)
            if 0 <= risk_free_rate <= 0.20:
                break
            print("⚠️  La tasa debe estar entre 0 y 0.20 (0% y 20%)\n")
        except ValueError:
            print("⚠️  Ingresa un número válido\n")
    
    print(f"✓ Tasa libre de riesgo: {risk_free_rate*100:.2f}%\n")
    
    # Restricciones de peso
    print("PASO 4: Restricciones de Peso por Activo")
    print("-" * 70)
    print("Define el peso mínimo y máximo que cada activo puede tener.")
    print("Ejemplo: máx 0.40 significa que ningún activo puede ser más del 40%")
    
    while True:
        try:
            max_weight_input = input("Peso máximo por activo [0.40]: ").strip() or '0.40'
            max_weight = float(max_weight_input)
            if 0.10 <= max_weight <= 1.0:
                break
            print("⚠️  El peso máximo debe estar entre 0.10 y 1.0\n")
        except ValueError:
            print("⚠️  Ingresa un número válido\n")
    
    min_weight = 0.0
    print(f"✓ Restricciones: 0% ≤ peso ≤ {max_weight*100:.0f}% por activo\n")
    
    # Estrategia
    print("PASO 5: Estrategia de Optimización")
    print("-" * 70)
    print("1. Maximizar Ratio de Sharpe (mejor retorno ajustado por riesgo)")
    print("2. Minimizar Volatilidad (menor riesgo)")
    print("3. Ambas (comparar estrategias)")
    
    while True:
        strategy = input("Selecciona estrategia [3]: ").strip() or '3'
        if strategy in ['1', '2', '3']:
            break
        print("⚠️  Selecciona 1, 2, o 3\n")
    
    strategy_names = {
        '1': 'Máximo Sharpe',
        '2': 'Mínima Volatilidad',
        '3': 'Ambas estrategias'
    }
    print(f"✓ Estrategia: {strategy_names[strategy]}\n")
    
    return {
        'tickers': tickers,
        'period': period,
        'risk_free_rate': risk_free_rate,
        'min_weight': min_weight,
        'max_weight': max_weight,
        'strategy': strategy
    }


def download_and_validate(tickers, period):
    """Descarga y valida los datos."""
    print(f"{'='*70}")
    print("Descargando datos del mercado...")
    print(f"{'='*70}\n")
    
    try:
        data = yf.download(tickers, period=period, interval='1d', progress=False, auto_adjust=True)
        
        if len(tickers) == 1:
            prices = data['Close'].to_frame()
            prices.columns = tickers
        else:
            prices = data['Close']
        
        prices = prices.dropna()
        
        # Validar que todos los tickers tengan datos
        valid_tickers = []
        invalid_tickers = []
        
        for ticker in tickers:
            if ticker in prices.columns and len(prices[ticker].dropna()) > 50:
                valid_tickers.append(ticker)
            else:
                invalid_tickers.append(ticker)
        
        if invalid_tickers:
            print(f"⚠️  Los siguientes tickers no tienen datos suficientes: {', '.join(invalid_tickers)}")
            print(f"    Continuando con: {', '.join(valid_tickers)}\n")
        
        if len(valid_tickers) < 2:
            raise ValueError("Se necesitan al menos 2 activos con datos válidos")
        
        prices = prices[valid_tickers]
        
        print(f"✓ Datos descargados exitosamente")
        print(f"  - Periodo: {prices.index[0].date()} a {prices.index[-1].date()}")
        print(f"  - Días de trading: {len(prices)}")
        print(f"  - Activos válidos: {len(valid_tickers)}\n")
        
        return prices
    
    except Exception as e:
        print(f"✗ Error al descargar datos: {e}")
        raise


def optimize_and_display(prices, risk_free_rate, min_weight, max_weight, strategy):
    """Realiza la optimización y muestra resultados."""
    # Calcular métricas
    returns = calculate_returns(prices, method='simple')
    expected_returns = returns.mean() * 252
    covariance_matrix = returns.cov() * 252
    
    print(f"{'='*70}")
    print("Métricas Individuales de los Activos")
    print(f"{'='*70}\n")
    
    print(f"{'Ticker':<10} {'Retorno Anual':>15} {'Volatilidad':>15} {'Sharpe':>10}")
    print("-" * 70)
    
    for ticker in expected_returns.index:
        ret = expected_returns[ticker] * 100
        vol = np.sqrt(covariance_matrix.loc[ticker, ticker]) * 100
        sharpe = (expected_returns[ticker] - risk_free_rate) / np.sqrt(covariance_matrix.loc[ticker, ticker])
        print(f"{ticker:<10} {ret:>14.2f}% {vol:>14.2f}% {sharpe:>10.2f}")
    
    print()
    
    # Crear optimizador
    optimizer = PortfolioOptimizer(
        expected_returns=expected_returns,
        covariance_matrix=covariance_matrix,
        risk_free_rate=risk_free_rate
    )
    
    constraints = {
        'min_weight': min_weight,
        'max_weight': max_weight,
        'long_only': True
    }
    
    results = {}
    
    # Máximo Sharpe
    if strategy in ['1', '3']:
        print(f"{'='*70}")
        print("OPTIMIZACIÓN: MAXIMIZAR RATIO DE SHARPE")
        print(f"{'='*70}\n")
        
        result = optimizer.optimize_max_sharpe(constraints=constraints)
        results['max_sharpe'] = result
        
        print_result(result, "Máximo Sharpe Ratio")
    
    # Mínima Volatilidad
    if strategy in ['2', '3']:
        print(f"{'='*70}")
        print("OPTIMIZACIÓN: MINIMIZAR VOLATILIDAD")
        print(f"{'='*70}\n")
        
        result = optimizer.optimize_min_volatility(constraints=constraints)
        results['min_vol'] = result
        
        print_result(result, "Mínima Volatilidad")
    
    # Comparación
    if strategy == '3':
        compare_results(results['max_sharpe'], results['min_vol'])
    
    return results


def print_result(result, title):
    """Imprime el resultado de una optimización."""
    print(f"Pesos del Portafolio ({title}):")
    print("-" * 70)
    
    weights = result['weights'].sort_values(ascending=False)
    for ticker, weight in weights.items():
        if weight > 0.001:
            bar = '█' * int(weight * 50)
            print(f"  {ticker:<10} {weight*100:>6.2f}% {bar}")
    
    print(f"\nMétricas del Portafolio:")
    print("-" * 70)
    print(f"  Retorno Esperado:  {result['expected_return']*100:7.2f}% anual")
    print(f"  Volatilidad:       {result['volatility']*100:7.2f}% anual")
    print(f"  Ratio de Sharpe:   {result['sharpe_ratio']:7.2f}")
    print()


def compare_results(result1, result2):
    """Compara dos resultados de optimización."""
    print(f"{'='*70}")
    print("COMPARACIÓN DE ESTRATEGIAS")
    print(f"{'='*70}\n")
    
    print(f"{'Métrica':<25} {'Max Sharpe':>15} {'Min Volatilidad':>15}")
    print("-" * 70)
    
    metrics = [
        ('Retorno Esperado (%)', 'expected_return', 100),
        ('Volatilidad (%)', 'volatility', 100),
        ('Ratio de Sharpe', 'sharpe_ratio', 1)
    ]
    
    for label, key, mult in metrics:
        val1 = result1[key] * mult
        val2 = result2[key] * mult
        print(f"{label:<25} {val1:>15.2f} {val2:>15.2f}")
    
    print()


def main():
    """Función principal interactiva."""
    try:
        # Obtener parámetros del usuario
        config = get_user_input()
        
        # Descargar datos
        prices = download_and_validate(config['tickers'], config['period'])
        
        # Optimizar
        results = optimize_and_display(
            prices,
            config['risk_free_rate'],
            config['min_weight'],
            config['max_weight'],
            config['strategy']
        )
        
        # Mensaje final
        print(f"{'='*70}")
        print("✓ OPTIMIZACIÓN COMPLETADA")
        print(f"{'='*70}\n")
        print("NOTA: Los resultados se basan en datos históricos y no garantizan")
        print("rendimientos futuros. Usa esta información como referencia y considera")
        print("consultar con un asesor financiero antes de tomar decisiones de inversión.")
        print(f"\n{'='*70}\n")
        
    except KeyboardInterrupt:
        print("\n\n✗ Operación cancelada por el usuario.\n")
        return 1
    except Exception as e:
        print(f"\n✗ Error: {e}\n")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
