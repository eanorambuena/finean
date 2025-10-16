# 📊 Finean - Financial Analysis and Portfolio Optimization

Una biblioteca Python profesional para optimización de portafolios de inversión usando datos reales del mercado.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## � Tabla de Contenidos

1. [🚀 Inicio Rápido (3 minutos)](#-inicio-rápido-3-minutos)
2. [📂 Scripts Disponibles](#-scripts-disponibles)
3. [🎯 Ejemplos Prácticos](#-ejemplos-prácticos)
4. [⚙️ Configuración y Personalización](#️-configuración-y-personalización)
5. [📊 Entendiendo los Resultados](#-entendiendo-los-resultados)
6. [🔧 API y Uso Avanzado](#-api-y-uso-avanzado)
7. [💡 Tips y Mejores Prácticas](#-tips-y-mejores-prácticas)
8. [❓ FAQ y Solución de Problemas](#-faq-y-solución-de-problemas)
9. [📚 Recursos Adicionales](#-recursos-adicionales)

---

## 🚀 Inicio Rápido (3 minutos)

### Paso 1: Instalar
```bash
pip install -r requirements.txt
```

### Paso 2: Ejecutar
```bash
python main.py
```

### Paso 3: Ver Resultados
```
RESULTADOS DE LA OPTIMIZACIÓN
======================================================================
Pesos Óptimos del Portafolio:
  WMT     :  39.28% ███████████████████
  JPM     :  31.90% ███████████████
  JNJ     :  14.66% ███████
  GOOGL   :  12.42% ██████

Métricas del Portafolio Óptimo:
  Retorno Esperado:    35.48% anual
  Volatilidad:         15.05% anual
  Ratio de Sharpe:      2.09  ⭐ Excelente
```

**¡Eso es todo!** Ya tienes un portafolio optimizado con datos reales.

---

## 📂 Scripts Disponibles

| Script | Descripción | Nivel | Cuándo Usar |
|--------|-------------|-------|-------------|
| **`main.py`** | Optimización básica (Máximo Sharpe) | ⭐ Principiante | Análisis rápido con tickers predefinidos |
| **`main_advanced.py`** | Comparación de estrategias | ⭐⭐ Intermedio | Comparar Máximo Sharpe vs Mínima Volatilidad |
| **`main_interactive.py`** | Modo interactivo | ⭐⭐⭐ Flexible | Experimentar sin editar código |
| **`demo.py`** | Demostración automatizada | 🎓 Aprendizaje | Ver múltiples ejemplos |

### Ejecutar Scripts

```bash
# Script básico (recomendado para empezar)
python main.py

# Comparar estrategias
python main_advanced.py

# Modo interactivo
python main_interactive.py

# Ver demostración
python demo.py
```

---

## 🎯 Ejemplos Prácticos

### Ejemplo 1: Portafolio de Tech Giants

Edita `main.py` y cambia los tickers:

```python
TICKERS = [
    'AAPL',   # Apple
    'MSFT',   # Microsoft
    'GOOGL',  # Alphabet
    'NVDA',   # NVIDIA
    'META',   # Meta
]
```

**Resultado esperado:**
```
Pesos Óptimos:
  NVDA    :  40.00% ████████████████████
  MSFT    :  35.50% █████████████████
  GOOGL   :  24.50% ████████████

Retorno Esperado:  42.15% anual
Volatilidad:       28.34% anual
Sharpe Ratio:      1.35 ✓✓ Bueno
```

### Ejemplo 2: Portafolio Diversificado (GLD, SPY, BIL)

```python
TICKERS = [
    'GLD',   # Oro (cobertura)
    'SPY',   # S&P 500 (acciones)
    'BIL',   # Bonos corto plazo (estabilidad)
]
```

**Resultado:**
```
Pesos Óptimos:
  SPY     :  71.80% ███████████████████████████████████
  GLD     :  28.20% ██████████████

Retorno Esperado:  13.33% anual
Volatilidad:       11.95% anual
Sharpe Ratio:      0.78 ⚠️ Aceptable (pero bajo riesgo)
```

### Ejemplo 3: Portafolio de ETFs Diversificado

```python
TICKERS = [
    'SPY',    # S&P 500
    'QQQ',    # NASDAQ 100
    'VTI',    # Total US Stock Market
    'AGG',    # Bonos agregados
    'GLD',    # Oro
]
```

### Ejemplo 4: Mix de Sectores

```python
TICKERS = [
    'AAPL',   # Tecnología
    'JPM',    # Financiero
    'JNJ',    # Salud
    'XOM',    # Energía
    'WMT',    # Consumo
    'CAT',    # Industrial
]
```

---

## ⚙️ Configuración y Personalización

### Cambiar Periodo de Datos

```python
PERIOD = '1y'   # 1 año
PERIOD = '2y'   # 2 años (recomendado)
PERIOD = '5y'   # 5 años (mejor para análisis)
PERIOD = '10y'  # 10 años
PERIOD = 'max'  # Máximo disponible
```

### Ajustar Tasa Libre de Riesgo

```python
RISK_FREE_RATE = 0.03  # 3% (bonos corto plazo)
RISK_FREE_RATE = 0.04  # 4% (bonos mediano plazo)
RISK_FREE_RATE = 0.05  # 5% (bonos largo plazo)
```

### Restricciones de Peso

```python
# Sin restricciones (un activo puede ser 100%)
MIN_WEIGHT = 0.0
MAX_WEIGHT = 1.0

# Forzar diversificación (máximo 40% por activo)
MIN_WEIGHT = 0.0
MAX_WEIGHT = 0.40

# Forzar participación mínima (cada activo al menos 5%)
MIN_WEIGHT = 0.05
MAX_WEIGHT = 0.30
```

### Tipos de Activos Soportados

✅ **Acciones individuales:** `AAPL`, `MSFT`, `GOOGL`, `TSLA`, etc.  
✅ **ETFs:** `SPY`, `QQQ`, `VTI`, `AGG`, `GLD`, etc.  
✅ **Criptomonedas:** `BTC-USD`, `ETH-USD`, `ADA-USD`, etc.  
✅ **Divisas:** `EURUSD=X`, `GBPUSD=X`, `USDJPY=X`, etc.  
✅ **Índices:** `^GSPC` (S&P 500), `^DJI` (Dow Jones), etc.

---

## 📊 Entendiendo los Resultados

### Ratio de Sharpe

Mide el **retorno ajustado por riesgo** (cuánto ganas por cada unidad de riesgo):

| Valor | Interpretación | Emoji |
|-------|----------------|-------|
| < 1.0 | Bajo retorno por riesgo | ❌ Evitar |
| 1.0 - 1.5 | Retorno aceptable | ⚠️ Considerar |
| 1.5 - 2.0 | Buen retorno ajustado | ✅ Bueno |
| > 2.0 | Excelente retorno ajustado | ⭐ Excelente |

**Fórmula:** `Sharpe = (Retorno - Tasa Libre de Riesgo) / Volatilidad`

### Volatilidad

Mide el **riesgo** (cuánto varía el precio):

| Rango | Tipo de Activo | Descripción |
|-------|----------------|-------------|
| < 10% | Muy bajo riesgo | Bonos, activos estables |
| 10-20% | Riesgo moderado | Portafolios diversificados |
| 20-30% | Riesgo alto | Acciones volátiles |
| > 30% | Riesgo muy alto | Crypto, acciones especulativas |

### Retorno Esperado

**Promedio anualizado** basado en datos históricos.

⚠️ **IMPORTANTE:** No garantiza resultados futuros. Úsalo como referencia, no como predicción.

### Matriz de Correlación

Muestra cómo se mueven los activos entre sí:

- **+1.0:** Se mueven juntos perfectamente (mala diversificación)
- **0.0:** No hay relación (buena diversificación)
- **-1.0:** Se mueven en direcciones opuestas (excelente diversificación)

**Ejemplo:**
```
         AAPL   JPM   GLD
AAPL     1.00  0.45  0.15  ← AAPL correlaciona poco con GLD (bueno)
JPM      0.45  1.00  0.20
GLD      0.15  0.20  1.00
```

---

## 🔧 API y Uso Avanzado

### Características de la Biblioteca

- ✅ **Optimización de Portafolio:** Máximo Sharpe, Mínima Volatilidad, Frontera Eficiente
- ✅ **Predicción de Series Temporales:** EWMA, SMA, EMA, Media Histórica
- ✅ **Utilidades Financieras:** Retornos, Volatilidad, Sharpe Ratio, Matrices de Covarianza

### Uso Programático (Python API)

#### 1. Optimización Básica

```python
import numpy as np
import pandas as pd
from finean import PortfolioOptimizer, TimeSeriesPredictor
from finean.utils import calculate_returns

# 1. Load or generate historical price data
prices = pd.read_csv('your_price_data.csv', index_col=0, parse_dates=True)

# 2. Calculate returns
returns = calculate_returns(prices, method='simple')

# 3. Use time series predictor to forecast returns
predictor = TimeSeriesPredictor(method='ewma')
predictor.fit(returns, span=60)
predictions = predictor.get_predictions(annualize=True, periods_per_year=252)

# 4. Optimize portfolio
optimizer = PortfolioOptimizer(
    expected_returns=predictions['returns'],
    covariance_matrix=predictions['covariance'],
    risk_free_rate=0.02
)

# Find maximum Sharpe ratio portfolio
result = optimizer.optimize_max_sharpe(
    constraints={'long_only': True, 'max_weight': 0.5}
)

print(f"Optimal Weights:\n{result['weights']}")
print(f"Expected Return: {result['expected_return']:.2%}")
print(f"Volatility: {result['volatility']:.2%}")
print(f"Sharpe Ratio: {result['sharpe_ratio']:.3f}")
```

## Usage Examples

### Portfolio Optimization

```python
from finean import PortfolioOptimizer

# Create optimizer with expected returns and covariance matrix
optimizer = PortfolioOptimizer(
    expected_returns=expected_returns,  # pd.Series
    covariance_matrix=cov_matrix,       # pd.DataFrame
    risk_free_rate=0.02
)

# 1. Maximum Sharpe Ratio Portfolio
max_sharpe = optimizer.optimize_max_sharpe(
    constraints={'long_only': True, 'max_weight': 0.4}
)

# 2. Minimum Volatility Portfolio
min_vol = optimizer.optimize_min_volatility()

# 3. Maximum Return for Target Risk
target_risk = optimizer.optimize_max_return_for_risk(target_volatility=0.15)

# 4. Calculate Efficient Frontier
frontier = optimizer.calculate_efficient_frontier(n_points=100)
```

### Time Series Prediction

```python
from finean import TimeSeriesPredictor

# Create predictor
predictor = TimeSeriesPredictor(method='ewma')

# Fit on historical returns
predictor.fit(returns, span=60)

# Get predictions
expected_returns = predictor.predict_returns()
cov_matrix = predictor.predict_covariance(method='shrinkage')

# Or get both at once
predictions = predictor.get_predictions(annualize=True)
```

### Financial Calculations

```python
from finean.utils import (
    calculate_returns,
    calculate_volatility,
    calculate_sharpe_ratio,
    calculate_covariance_matrix
)

# Calculate returns
returns = calculate_returns(prices, method='simple')

# Calculate volatility
vol = calculate_volatility(returns, annualize=True, periods_per_year=252)

# Calculate Sharpe ratio
sharpe = calculate_sharpe_ratio(returns, risk_free_rate=0.02, annualize=True)

# Calculate covariance matrix
cov = calculate_covariance_matrix(returns, annualize=True)
```

## Running the Example

A comprehensive example is provided in `examples/portfolio_optimization_example.py`:

```bash
python examples/portfolio_optimization_example.py
```

This will:
1. Generate sample historical price data
2. Calculate returns and use time series prediction
3. Optimize portfolios using different strategies
4. Calculate the efficient frontier
5. Create visualizations showing the results

## Testing

Run the test suite to verify the installation:

```bash
python -m unittest discover tests -v
```

All tests should pass, covering:
- Utility functions
- Time series prediction methods
- Portfolio optimization algorithms

## API Reference

### PortfolioOptimizer

Main class for portfolio optimization.

**Methods:**
- `optimize_max_sharpe(constraints=None)`: Find portfolio with maximum Sharpe ratio
- `optimize_min_volatility(constraints=None)`: Find minimum volatility portfolio
- `optimize_max_return_for_risk(target_volatility, constraints=None)`: Maximize return for given risk
- `calculate_efficient_frontier(n_points=100, constraints=None)`: Calculate efficient frontier
- `get_portfolio_statistics(weights)`: Calculate statistics for a given portfolio

**Constraints:**
- `max_weight`: Maximum weight per asset (default: 1.0)
- `min_weight`: Minimum weight per asset (default: 0.0)
- `long_only`: Boolean, whether to allow short selling (default: True)

### TimeSeriesPredictor

Class for time series prediction of asset returns.

**Methods:**
- `fit(returns, **kwargs)`: Fit predictor on historical returns
- `predict_returns(horizon=1)`: Predict expected returns
- `predict_covariance(method='sample')`: Predict covariance matrix
- `get_predictions(annualize=True, periods_per_year=252)`: Get both returns and covariance

**Prediction Methods:**
- `ewma`: Exponentially Weighted Moving Average
- `sma`: Simple Moving Average
- `ema`: Exponential Moving Average
- `historical_mean`: Historical mean returns

**Covariance Methods:**
- `sample`: Sample covariance
- `ewma`: Exponentially weighted covariance
- `shrinkage`: Ledoit-Wolf shrinkage estimator

## Mathematical Background

### Portfolio Optimization

The library implements Modern Portfolio Theory (MPT) optimization:

**Maximum Sharpe Ratio:**
Maximizes: (E[R] - Rf) / σ

Where:
- E[R] = Expected portfolio return
- Rf = Risk-free rate
- σ = Portfolio standard deviation (volatility)

**Subject to:**
- Sum of weights = 1
- Optional constraints on individual weights

**Minimum Volatility:**
Minimizes: σ = sqrt(w' Σ w)

Where:
- w = Portfolio weights
- Σ = Covariance matrix

**Efficient Frontier:**
The set of optimal portfolios offering the highest expected return for each level of risk.

### Time Series Prediction

The library uses various methods to predict future returns:

- **EWMA**: Gives more weight to recent observations
- **Moving Averages**: Simple or exponential averaging
- **Covariance Estimation**: Sample, EWMA, or shrinkage methods for better risk estimates

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Author

Fenian level finance
