"""
Script avanzado de optimización de portafolio con múltiples estrategias.

Este script permite:
1. Descargar datos históricos de acciones reales
2. Optimizar para Máximo Sharpe Ratio
3. Optimizar para Mínima Volatilidad
4. Optimizar para Máximo Retorno
5. Comparar las tres estrategias
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
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





def compare_strategies(max_sharpe_result: dict, min_vol_result: dict, max_return_result: dict):
    """Compara las tres estrategias de optimización."""
    print(f"{'='*70}")
    print("COMPARACIÓN DE ESTRATEGIAS (ordenado por retorno)")
    print(f"{'='*70}\n")
    
    # Extraer métricas
    ret_sharpe = max_sharpe_result['expected_return'] * 100
    ret_minvol = min_vol_result['expected_return'] * 100
    ret_maxret = max_return_result['expected_return'] * 100
    
    vol_sharpe = max_sharpe_result['volatility'] * 100
    vol_minvol = min_vol_result['volatility'] * 100
    vol_maxret = max_return_result['volatility'] * 100
    
    sharpe_sharpe = max_sharpe_result['sharpe_ratio']
    sharpe_minvol = min_vol_result['sharpe_ratio']
    sharpe_maxret = max_return_result['sharpe_ratio']
    
    # Crear lista de estrategias con sus métricas
    strategies = [
        ('Min Vol', ret_minvol, vol_minvol, sharpe_minvol, '🛡️'),
        ('Max Sharpe', ret_sharpe, vol_sharpe, sharpe_sharpe, '⭐'),
        ('Max Return', ret_maxret, vol_maxret, sharpe_maxret, '🚀')
    ]
    
    # Ordenar por retorno (menor a mayor)
    strategies.sort(key=lambda x: x[1])
    
    # Imprimir encabezados
    print(f"{'Estrategia':<18} {'Retorno':>12} {'Volatilidad':>12} {'Sharpe':>10} {'Perfil':>12}")
    print("-" * 70)
    
    # Imprimir cada estrategia
    for name, ret, vol, sharpe, emoji in strategies:
        print(f"{name + ' ' + emoji:<18} {ret:>11.2f}% {vol:>11.2f}% {sharpe:>10.2f}   ", end='')
        
        # Indicador visual de riesgo
        if vol < 5:
            print("Muy Bajo")
        elif vol < 10:
            print("Bajo")
        elif vol < 20:
            print("Moderado")
        elif vol < 30:
            print("Alto")
        else:
            print("Muy Alto")
    
    print(f"\n{'='*70}\n")
    
    # Recomendación
    print("RECOMENDACIONES:")
    print("-" * 70)
    
    # Encontrar el mejor Sharpe
    best_sharpe = max(sharpe_sharpe, sharpe_minvol, sharpe_maxret)
    
    if sharpe_sharpe >= best_sharpe * 0.95:
        print("✓ MÁXIMO SHARPE: Mejor balance entre retorno y riesgo")
        print("  Recomendado para inversores que buscan eficiencia")
    
    if sharpe_minvol >= best_sharpe * 0.95 or vol_minvol < min(vol_sharpe, vol_maxret) * 0.85:
        print("✓ MÍNIMA VOLATILIDAD: Menor riesgo")
        print("  Recomendado para inversores conservadores")
    
    if ret_maxret > max(ret_sharpe, ret_minvol) * 1.1:
        print("⚠️  MÁXIMO RETORNO: Mayor retorno pero con MÁS RIESGO")
        print(f"  Volatilidad: {vol_maxret:.2f}% (vs {vol_sharpe:.2f}% Max Sharpe)")
        print("  Solo para inversores agresivos con alta tolerancia al riesgo")
    
    print(f"\n{'='*70}\n")


def plot_portfolio_scenarios(max_sharpe_result: dict, min_vol_result: dict, max_return_result: dict, 
                             investment_amount: float = 10000, time_horizon: int = 1):
    """
    Visualiza escenarios (pesimista, esperado, optimista) para cada portafolio.
    
    Parameters:
    -----------
    investment_amount : float
        Monto inicial de inversión
    time_horizon : int
        Horizonte temporal en años
    """
    print(f"{'='*70}")
    print("PROYECCIÓN DE ESCENARIOS")
    print(f"{'='*70}\n")
    print(f"Inversión inicial: ${investment_amount:,.0f}")
    print(f"Horizonte temporal: {time_horizon} año(s)\n")
    
    strategies = {
        'Min Vol 🛡️': min_vol_result,
        'Max Sharpe ⭐': max_sharpe_result,
        'Max Return 🚀': max_return_result
    }
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle('Proyección de Portafolios: Escenarios a 1 Año', fontsize=16, fontweight='bold')
    
    for idx, (name, result) in enumerate(strategies.items()):
        ax = axes[idx]
        
        # Extraer métricas
        expected_return = result['expected_return']
        volatility = result['volatility']
        
        # Calcular escenarios
        # Pesimista: retorno esperado - 2 desviaciones estándar
        # Esperado: retorno esperado
        # Optimista: retorno esperado + 2 desviaciones estándar
        pessimistic = investment_amount * (1 + (expected_return - 2 * volatility) * time_horizon)
        expected = investment_amount * (1 + expected_return * time_horizon)
        optimistic = investment_amount * (1 + (expected_return + 2 * volatility) * time_horizon)
        
        # Asegurar que el pesimista no sea negativo
        pessimistic = max(pessimistic, investment_amount * 0.1)
        
        # Datos para el gráfico
        scenarios = ['Pesimista\n(-2σ)', 'Esperado', 'Optimista\n(+2σ)']
        values = [pessimistic, expected, optimistic]
        colors = ['#d62728', '#2ca02c', '#1f77b4']
        
        # Crear barras
        bars = ax.bar(scenarios, values, color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)
        
        # Línea de referencia (inversión inicial)
        ax.axhline(y=investment_amount, color='gray', linestyle='--', linewidth=2, label='Inversión inicial')
        
        # Etiquetas en las barras
        for bar, value in zip(bars, values):
            height = bar.get_height()
            profit = value - investment_amount
            profit_pct = (profit / investment_amount) * 100
            
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'${value:,.0f}\n({profit_pct:+.1f}%)',
                   ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        # Configuración del gráfico
        ax.set_title(f'{name}\nRetorno: {expected_return*100:.1f}% | Vol: {volatility*100:.1f}%',
                    fontsize=11, fontweight='bold')
        ax.set_ylabel('Valor del Portafolio ($)', fontsize=10)
        ax.set_ylim(0, max(values) * 1.2)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        ax.legend(fontsize=8)
        
        # Formato de eje Y
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    
    plt.tight_layout()
    
    # Guardar y mostrar
    filename = 'portfolio_scenarios.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"✓ Gráfico guardado como: {filename}\n")
    
    # Mostrar el gráfico
    plt.show()
    
    # Tabla resumen de escenarios
    print("TABLA DE ESCENARIOS:")
    print("-" * 70)
    print(f"{'Portafolio':<20} {'Pesimista':>15} {'Esperado':>15} {'Optimista':>15}")
    print("-" * 70)
    
    for name, result in strategies.items():
        expected_return = result['expected_return']
        volatility = result['volatility']
        
        pessimistic = investment_amount * (1 + (expected_return - 2 * volatility) * time_horizon)
        expected = investment_amount * (1 + expected_return * time_horizon)
        optimistic = investment_amount * (1 + (expected_return + 2 * volatility) * time_horizon)
        
        pessimistic = max(pessimistic, investment_amount * 0.1)
        
        print(f"{name:<20} ${pessimistic:>14,.0f} ${expected:>14,.0f} ${optimistic:>14,.0f}")
    
    print()
    print("INTERPRETACIÓN:")
    print("-" * 70)
    print("• Pesimista: Escenario donde el retorno es 2 desviaciones estándar BAJO el esperado")
    print("             (probabilidad ~2.5% de ser peor que esto)")
    print("• Esperado: Retorno promedio esperado basado en datos históricos")
    print("• Optimista: Escenario donde el retorno es 2 desviaciones estándar SOBRE el esperado")
    print("             (probabilidad ~2.5% de ser mejor que esto)")
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
        'ITA',    # iShares U.S. Aerospace & Defense ETF
        'XLP',    # Consumer Staples Select Sector SPDR Fund
        'SPLB',   # SPDR Portfolio Long Term Treasury ETF
        'QQQ',    # Invesco QQQ Trust (Tecnología)
        'VTI',   # Total US Stock Market
        'AGG',   # Bonos agregados
        'JPM',       # Finanzas
        'JNJ',       # Salud
        'XOM',       # Energía
        'BTC-USD',   # Crypto
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
        
        # Paso 6: Optimización para Máximo Retorno
        print(f"{'='*70}")
        print("ESTRATEGIA 3: Maximizar Retorno (sin considerar riesgo)")
        print(f"{'='*70}\n")
        print("Optimizando para máximo retorno esperado...\n")
        
        max_return_result = optimizer.optimize_max_return(constraints=constraints)
        print_portfolio_results("PORTAFOLIO ÓPTIMO: MÁXIMO RETORNO", max_return_result)
        
        # Paso 7: Comparar estrategias
        compare_strategies(max_sharpe_result, min_vol_result, max_return_result)
        
        # Paso 8: Visualizar escenarios
        plot_portfolio_scenarios(max_sharpe_result, min_vol_result, max_return_result,
                                investment_amount=10000, time_horizon=1)
        
        # Información adicional
        print("NOTAS:")
        print("-" * 70)
        print("• Máximo Sharpe: Mejor eficiencia (retorno/riesgo)")
        print("• Mínima Volatilidad: Menor riesgo posible")
        print("• Máximo Retorno: Mayor retorno esperado (ignora el riesgo)")
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
