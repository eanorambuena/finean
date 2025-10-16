# 📊 Finean - Optimización de Portafolios de Inversión

Biblioteca Python profesional para optimización de portafolios con **datos reales del mercado**.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📑 Índice

- [🚀 Inicio Rápido](#-inicio-rápido)
- [📂 Scripts Disponibles](#-scripts-disponibles)
- [🎯 Ejemplos Prácticos](#-ejemplos-prácticos)
- [⚙️ Configuración](#️-configuración)
- [📊 Interpretación de Resultados](#-interpretación-de-resultados)
- [🔧 API Python](#-api-python)
- [💡 Tips y Buenas Prácticas](#-tips-y-buenas-prácticas)
- [❓ FAQ](#-faq)
- [📚 Recursos](#-recursos)

---

## 🚀 Inicio Rápido

### 3 Pasos para Empezar

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Ejecutar optimización
python main.py

# 3. ¡Ver resultados!
```

### Resultado Esperado

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

---

## 📂 Scripts Disponibles

| Script | Nivel | Descripción | Uso |
|--------|-------|-------------|-----|
| `main.py` | ⭐ Básico | Optimización Máximo Sharpe | `python main.py` |
| `main_advanced.py` | ⭐⭐ Intermedio | Comparar estrategias | `python main_advanced.py` |
| `main_interactive.py` | ⭐⭐⭐ Flexible | Modo interactivo | `python main_interactive.py` |
| `demo.py` | 🎓 Demo | Múltiples ejemplos | `python demo.py` |

### ¿Cuál Script Usar?

- **Primera vez?** → `main.py`
- **Quieres comparar estrategias?** → `main_advanced.py`
- **Quieres cambiar parámetros sin editar código?** → `main_interactive.py`
- **Quieres ver varios ejemplos?** → `demo.py`

---

## 🎯 Ejemplos Prácticos

### Ejemplo 1: Tech Giants 🖥️

```python
# Edita main.py
TICKERS = ['AAPL', 'MSFT', 'GOOGL', 'NVDA', 'META']
```

**Resultado típico:**
- Retorno: ~40% anual
- Volatilidad: ~28% anual
- Sharpe: ~1.3 (Bueno)

### Ejemplo 2: Portafolio Clásico (Oro + Acciones + Bonos) 🏆

```python
TICKERS = [
    'GLD',   # Oro (cobertura)
    'SPY',   # S&P 500 (crecimiento)
    'BIL',   # Bonos (estabilidad)
]
```

**Resultado típico:**
- Retorno: ~13% anual
- Volatilidad: ~12% anual
- Sharpe: ~0.8 (Conservador pero estable)

### Ejemplo 3: ETFs Diversificados 📈

```python
TICKERS = ['SPY', 'QQQ', 'VTI', 'AGG', 'GLD']
```

### Ejemplo 4: Mix por Sectores 🏭

```python
TICKERS = [
    'AAPL',  # Tech
    'JPM',   # Finanzas
    'JNJ',   # Salud
    'XOM',   # Energía
    'WMT',   # Consumo
]
```

---

## ⚙️ Configuración

### Cambiar Activos

Edita la lista `TICKERS` en cualquier script:

```python
TICKERS = ['AAPL', 'MSFT', 'GOOGL']  # Tus tickers aquí
```

**Tipos soportados:**
- ✅ Acciones: `AAPL`, `MSFT`, `TSLA`
- ✅ ETFs: `SPY`, `QQQ`, `VTI`
- ✅ Criptos: `BTC-USD`, `ETH-USD`
- ✅ Divisas: `EURUSD=X`
- ✅ Índices: `^GSPC`, `^DJI`

### Periodo de Datos

```python
PERIOD = '2y'   # 2 años (recomendado)
PERIOD = '5y'   # 5 años (mejor)
PERIOD = 'max'  # Máximo disponible
```

### Tasa Libre de Riesgo

```python
RISK_FREE_RATE = 0.04  # 4% anual (bonos del tesoro USA)
```

### Restricciones de Peso

```python
MIN_WEIGHT = 0.0   # Mínimo por activo (0 = puede ser 0%)
MAX_WEIGHT = 0.40  # Máximo por activo (0.4 = máximo 40%)
```

---

## 📊 Interpretación de Resultados

### Ratio de Sharpe

**¿Qué mide?** Retorno ajustado por riesgo.

| Valor | Calificación | Significado |
|-------|--------------|-------------|
| < 1.0 | ❌ Malo | Bajo retorno por riesgo tomado |
| 1.0-1.5 | ⚠️ Aceptable | Retorno decente por el riesgo |
| 1.5-2.0 | ✅ Bueno | Buen balance riesgo-retorno |
| > 2.0 | ⭐ Excelente | Muy buen retorno ajustado |

**Fórmula:** `(Retorno - Tasa Libre de Riesgo) / Volatilidad`

### Volatilidad (Riesgo)

**¿Qué mide?** Cuánto varía el precio (a mayor volatilidad, mayor riesgo).

| Rango | Tipo | Ejemplos |
|-------|------|----------|
| < 10% | Muy bajo | Bonos, activos estables |
| 10-20% | Moderado | Portafolios diversificados |
| 20-30% | Alto | Acciones volátiles |
| > 30% | Muy alto | Crypto, especulativas |

### Retorno Esperado

Promedio anualizado de datos históricos.

⚠️ **Importante:** Datos pasados no garantizan resultados futuros.

### Matriz de Correlación

**¿Qué mide?** Cómo se mueven los activos entre sí.

- **+1.0:** Se mueven juntos (mala diversificación)
- **0.0:** Independientes (buena diversificación)
- **-1.0:** Opuestos (excelente diversificación)

---

## 🔧 API Python

### Instalación

```bash
pip install -r requirements.txt
```

**Dependencias:**
- numpy >= 1.21.0
- pandas >= 1.3.0
- scipy >= 1.7.0
- matplotlib >= 3.4.0
- yfinance >= 0.2.0

### Uso Básico

```python
from finean import PortfolioOptimizer
from finean.utils import calculate_returns
import yfinance as yf

# 1. Descargar datos
data = yf.download(['AAPL', 'MSFT', 'GOOGL'], period='2y')
prices = data['Close']

# 2. Calcular retornos y métricas
returns = calculate_returns(prices)
expected_returns = returns.mean() * 252
cov_matrix = returns.cov() * 252

# 3. Optimizar
optimizer = PortfolioOptimizer(
    expected_returns=expected_returns,
    covariance_matrix=cov_matrix,
    risk_free_rate=0.04
)

# 4. Obtener portafolio óptimo
result = optimizer.optimize_max_sharpe()

print(f"Pesos: {result['weights']}")
print(f"Sharpe: {result['sharpe_ratio']:.2f}")
```

### Estrategias de Optimización

```python
# 1. Máximo Sharpe Ratio (mejor retorno ajustado por riesgo)
max_sharpe = optimizer.optimize_max_sharpe()

# 2. Mínima Volatilidad (menor riesgo)
min_vol = optimizer.optimize_min_volatility()

# 3. Máximo Retorno (sin considerar riesgo - agresivo)
max_return = optimizer.optimize_max_return()

# 4. Máximo retorno para un riesgo objetivo
target = optimizer.optimize_max_return_for_risk(target_volatility=0.15)

# 5. Frontera eficiente
frontier = optimizer.calculate_efficient_frontier(n_points=100)
```

### Restricciones

```python
constraints = {
    'min_weight': 0.05,  # Mínimo 5% por activo
    'max_weight': 0.30,  # Máximo 30% por activo
    'long_only': True    # No short selling
}

result = optimizer.optimize_max_sharpe(constraints=constraints)
```

### Utilidades Financieras

```python
from finean.utils import (
    calculate_returns,
    calculate_volatility,
    calculate_sharpe_ratio,
    calculate_covariance_matrix
)

# Calcular retornos
returns = calculate_returns(prices, method='simple')

# Calcular volatilidad
vol = calculate_volatility(returns, annualize=True)

# Calcular Sharpe Ratio
sharpe = calculate_sharpe_ratio(returns, risk_free_rate=0.04)

# Matriz de covarianza
cov = calculate_covariance_matrix(returns, annualize=True)
```

### Predicción de Series Temporales

```python
from finean import TimeSeriesPredictor

# Crear predictor
predictor = TimeSeriesPredictor(method='ewma')

# Entrenar con datos históricos
predictor.fit(returns, span=60)

# Predecir retornos y covarianza
predictions = predictor.get_predictions(annualize=True)
expected_returns = predictions['returns']
cov_matrix = predictions['covariance']
```

---

## 💡 Tips y Buenas Prácticas

### ✅ Hacer

1. **Diversificar:** Usa activos de diferentes sectores
2. **Datos suficientes:** Mínimo 2 años de historia
3. **Revisar correlaciones:** Busca activos poco correlacionados
4. **Reoptimizar:** Cada 3-6 meses
5. **Considerar costos:** Comisiones, impuestos, etc.

### ❌ Evitar

1. **Solo un sector:** No pongas todo en tech/finanzas/etc.
2. **Datos insuficientes:** Menos de 1 año no es representativo
3. **Perseguir retornos:** Alto retorno pasado ≠ futuro garantizado
4. **Ignorar advertencias:** El optimizador te avisa de problemas
5. **Invertir sin asesoría:** Esto es educativo, no asesoría financiera

### 🎯 Portafolios Recomendados por Perfil

#### Conservador 🛡️
```python
TICKERS = ['BIL', 'AGG', 'GLD', 'SPY']
MAX_WEIGHT = 0.40
```
Objetivo: Preservar capital, bajo riesgo.

#### Moderado ⚖️
```python
TICKERS = ['SPY', 'QQQ', 'AGG', 'GLD', 'VTI']
MAX_WEIGHT = 0.35
```
Objetivo: Balance entre crecimiento y estabilidad.

#### Agresivo 🚀
```python
TICKERS = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'NVDA']
MAX_WEIGHT = 0.40
```
Objetivo: Máximo crecimiento, aceptando alta volatilidad.

---

## ❓ FAQ

### ¿Es esto asesoría financiera?

**No.** Este proyecto es **solo educativo**. No inviertas sin consultar a un profesional.

### ¿Los retornos son garantizados?

**No.** Los resultados se basan en datos históricos. El pasado no predice el futuro.

### ¿Qué significa "Optimización no convergió"?

El algoritmo tuvo problemas. Soluciones:
- Aumenta el periodo de datos (`PERIOD = '5y'`)
- Ajusta restricciones (aumenta `MAX_WEIGHT`)
- Reduce número de activos

### ¿Por qué un activo tiene peso 0%?

El optimizador decidió que no mejora el portafolio. Esto es normal y esperado.

### ¿Puedo usar con datos propios?

Sí. Usa la API Python con tus propios DataFrames de precios.

### ¿Funciona con criptomonedas?

Sí, usa tickers como `BTC-USD`, `ETH-USD`, etc.

### ¿Incluye costos de transacción?

No. Los cálculos son teóricos. En la práctica considera:
- Comisiones de compra/venta
- Impuestos sobre ganancias
- Spreads bid-ask
- Costos de rebalanceo

### ¿Cada cuánto debo reoptimizar?

Recomendado: cada 3-6 meses, o cuando cambien tus objetivos.

---

## 📚 Recursos

### Documentación

- **README.md** (este archivo) - Guía completa
- **examples/** - Ejemplos de uso de la biblioteca
- **tests/** - Suite de tests

### Teoría

- [Modern Portfolio Theory](https://en.wikipedia.org/wiki/Modern_portfolio_theory) - Teoría base
- [Sharpe Ratio](https://www.investopedia.com/terms/s/sharperatio.asp) - Explicación del ratio de Sharpe
- [Efficient Frontier](https://www.investopedia.com/terms/e/efficientfrontier.asp) - Frontera eficiente

### Herramientas

- [Yahoo Finance](https://finance.yahoo.com/) - Buscar tickers
- [ETF Database](https://etfdb.com/) - Información de ETFs
- [Portfolio Visualizer](https://www.portfoliovisualizer.com/) - Análisis complementario

### Libros Recomendados

- "A Random Walk Down Wall Street" - Burton Malkiel
- "The Intelligent Investor" - Benjamin Graham
- "Common Sense on Mutual Funds" - John Bogle

---

## 🔬 Tests

Ejecutar suite de tests:

```bash
python -m unittest discover tests -v
```

Los tests cubren:
- Utilidades financieras
- Optimización de portafolios
- Predicción de series temporales

---

## 📝 Licencia

MIT License - Ver [LICENSE](LICENSE)

---

## 🤝 Contribuir

¿Encontraste un bug o tienes una sugerencia?

1. Abre un **Issue** describiendo el problema
2. O haz un **Pull Request** con tu solución

---

## ⚠️ Disclaimers

### Riesgo de Inversión

Las inversiones en el mercado de valores conllevan riesgos. Puedes perder parte o todo tu capital. Esta herramienta:

- ❌ **NO** es asesoría financiera
- ❌ **NO** garantiza resultados
- ❌ **NO** reemplaza a un asesor profesional
- ✅ **ES** solo educativa
- ✅ **ES** para aprender sobre optimización
- ✅ **ES** un punto de partida para análisis

### Limitaciones del Modelo

- Asume distribución normal de retornos (no siempre cierto)
- No considera eventos extremos ("cisnes negros")
- Asume correlaciones constantes (cambian con el tiempo)
- No incluye costos de transacción
- Basado en datos históricos (pasado ≠ futuro)

### Uso Responsable

Antes de invertir:

1. ✅ Consulta con un asesor financiero certificado
2. ✅ Entiende tu tolerancia al riesgo
3. ✅ Considera tu horizonte temporal
4. ✅ Diversifica adecuadamente
5. ✅ Ten un plan de inversión claro

---

## 📧 Contacto

**Proyecto:** [github.com/eanorambuena/finean](https://github.com/eanorambuena/finean)

---

<div align="center">

**¡Gracias por usar Finean! 📈💰**

Si te resultó útil, considera darle una ⭐ en GitHub

</div>
