"""
Script de demostración automatizada.
Muestra diferentes ejemplos de optimización sin necesidad de interacción.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import numpy as np
import pandas as pd
import yfinance as yf
from finean import PortfolioOptimizer
from finean.utils import calculate_returns


def print_header(title):
    """Imprime un encabezado formateado."""
    print(f"\n{'='*70}")
    print(f"{title.center(70)}")
    print(f"{'='*70}\n")


def run_example(name, tickers, period='2y', risk_free_rate=0.04):
    """Ejecuta un ejemplo de optimización."""
    print_header(f"EJEMPLO: {name}")
    
    print(f"Tickers: {', '.join(tickers)}")
    print(f"Periodo: {period}")
    print(f"Tasa libre de riesgo: {risk_free_rate*100:.1f}%\n")
    
    try:
        # Descargar datos
        print("⏳ Descargando datos...")
        data = yf.download(tickers, period=period, interval='1d', progress=False, auto_adjust=True)
        
        if len(tickers) == 1:
            prices = data['Close'].to_frame()
            prices.columns = tickers
        else:
            prices = data['Close']
        
        prices = prices.dropna()
        
        if len(prices) < 50:
            print(f"⚠️  Datos insuficientes ({len(prices)} días). Saltando este ejemplo.\n")
            return
        
        print(f"✓ Descargados {len(prices)} días de datos\n")
        
        # Calcular métricas
        returns = calculate_returns(prices, method='simple')
        expected_returns = returns.mean() * 252
        covariance_matrix = returns.cov() * 252
        
        # Optimizar
        optimizer = PortfolioOptimizer(
            expected_returns=expected_returns,
            covariance_matrix=covariance_matrix,
            risk_free_rate=risk_free_rate
        )
        
        result = optimizer.optimize_max_sharpe(constraints={
            'min_weight': 0.0,
            'max_weight': 1.0,
            'long_only': True
        })
        
        # Mostrar resultados
        print("PORTAFOLIO ÓPTIMO:")
        print("-" * 70)
        
        weights = result['weights'].sort_values(ascending=False)
        for ticker, weight in weights.items():
            if weight > 0.01:
                bar = '█' * int(weight * 40)
                print(f"  {ticker:10s} {weight*100:6.2f}%  {bar}")
        
        print(f"\nMÉTRICAS:")
        print("-" * 70)
        print(f"  Retorno Esperado:  {result['expected_return']*100:7.2f}% anual")
        print(f"  Volatilidad:       {result['volatility']*100:7.2f}% anual")
        print(f"  Ratio de Sharpe:   {result['sharpe_ratio']:7.2f}")
        
        # Calificar el Sharpe
        sharpe = result['sharpe_ratio']
        if sharpe < 1.0:
            rating = "⚠️  Bajo"
        elif sharpe < 1.5:
            rating = "✓ Aceptable"
        elif sharpe < 2.0:
            rating = "✓✓ Bueno"
        else:
            rating = "⭐ Excelente"
        
        print(f"  Calificación:      {rating}")
        print()
        
        return result
        
    except Exception as e:
        print(f"✗ Error: {e}\n")
        return None


def main():
    """Ejecuta varios ejemplos de demostración."""
    print("\n" + "="*70)
    print("DEMOSTRACIÓN AUTOMATIZADA - OPTIMIZACIÓN DE PORTAFOLIOS".center(70))
    print("="*70)
    print("\nEste script ejecuta varios ejemplos automáticamente.\n")
    
    examples = [
        {
            'name': 'Portafolio Tech Giants',
            'tickers': ['AAPL', 'MSFT', 'GOOGL', 'META', 'NVDA'],
            'period': '2y'
        },
        {
            'name': 'Portafolio Diversificado por Sectores',
            'tickers': ['AAPL', 'JPM', 'JNJ', 'XOM', 'WMT'],
            'period': '2y'
        },
        {
            'name': 'Portafolio de ETFs',
            'tickers': ['SPY', 'QQQ', 'AGG', 'GLD', 'VTI'],
            'period': '2y'
        },
        {
            'name': 'Portafolio Defensivo',
            'tickers': ['JNJ', 'PG', 'KO', 'PEP', 'WMT', 'T'],
            'period': '2y'
        },
        {
            'name': 'Portafolio Financiero',
            'tickers': ['JPM', 'BAC', 'WFC', 'C', 'GS'],
            'period': '2y'
        },
    ]
    
    results = {}
    
    for example in examples:
        result = run_example(
            name=example['name'],
            tickers=example['tickers'],
            period=example['period']
        )
        
        if result:
            results[example['name']] = result
        
        print()
        input("Presiona Enter para continuar al siguiente ejemplo...")
    
    # Resumen final
    if results:
        print_header("RESUMEN DE TODOS LOS EJEMPLOS")
        
        print(f"{'Portafolio':<40} {'Retorno':>10} {'Vol':>10} {'Sharpe':>8}")
        print("-" * 70)
        
        for name, result in results.items():
            ret = result['expected_return'] * 100
            vol = result['volatility'] * 100
            sharpe = result['sharpe_ratio']
            print(f"{name:<40} {ret:>9.2f}% {vol:>9.2f}% {sharpe:>8.2f}")
        
        print("\n")
        
        # Mejor Sharpe
        best_sharpe_name = max(results.items(), key=lambda x: x[1]['sharpe_ratio'])[0]
        best_sharpe = results[best_sharpe_name]['sharpe_ratio']
        
        print(f"🏆 MEJOR RATIO DE SHARPE: {best_sharpe_name}")
        print(f"   Sharpe: {best_sharpe:.2f}")
        
        # Menor volatilidad
        min_vol_name = min(results.items(), key=lambda x: x[1]['volatility'])[0]
        min_vol = results[min_vol_name]['volatility'] * 100
        
        print(f"\n🛡️  MENOR VOLATILIDAD: {min_vol_name}")
        print(f"   Volatilidad: {min_vol:.2f}%")
        
        # Mayor retorno
        max_ret_name = max(results.items(), key=lambda x: x[1]['expected_return'])[0]
        max_ret = results[max_ret_name]['expected_return'] * 100
        
        print(f"\n📈 MAYOR RETORNO ESPERADO: {max_ret_name}")
        print(f"   Retorno: {max_ret:.2f}%")
        
        print(f"\n{'='*70}\n")
    
    print("CONCLUSIONES:")
    print("-" * 70)
    print("• Diferentes portafolios tienen diferentes perfiles de riesgo-retorno")
    print("• El Sharpe Ratio te ayuda a elegir el más eficiente")
    print("• La diversificación reduce el riesgo sin sacrificar mucho retorno")
    print("• Usa estos scripts para experimentar con tus propias ideas")
    print(f"\n{'='*70}\n")
    
    print("¡Demostración completada! 🎉")
    print("\nPara usar con tus propios tickers:")
    print("  1. Edita main.py y cambia la lista TICKERS")
    print("  2. O ejecuta main_interactive.py para modo interactivo")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✗ Demostración cancelada.\n")
    except Exception as e:
        print(f"\n✗ Error: {e}\n")
        import traceback
        traceback.print_exc()
