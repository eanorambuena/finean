# Guía de Uso: main.py - Optimización de Portafolio con Datos Reales

## 📊 Descripción

El script `main.py` utiliza la biblioteca **finean** para optimizar portafolios de inversión con datos reales del mercado. Descarga automáticamente datos históricos de acciones usando Yahoo Finance y calcula el portafolio óptimo que maximiza el ratio de Sharpe (retorno ajustado por riesgo).

## 🚀 Inicio Rápido

### 1. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 2. Ejecutar el Script

```bash
python main.py
```

## ⚙️ Configuración

Puedes personalizar la optimización modificando los parámetros en la función `main()` del archivo `main.py`:

### Seleccionar Activos

Modifica la lista `TICKERS` con los símbolos de las acciones que deseas incluir:

```python
TICKERS = [
    'AAPL',   # Apple
    'MSFT',   # Microsoft
    'GOOGL',  # Alphabet (Google)
    'AMZN',   # Amazon
    'TSLA',   # Tesla
]
```

### Parámetros de Datos Históricos

```python
PERIOD = '2y'        # Periodo de datos: '1y', '2y', '5y', '10y', 'max'
INTERVAL = '1d'      # Intervalo: '1d' (diario), '1wk' (semanal), '1mo' (mensual)
```

### Parámetros de Optimización

```python
RISK_FREE_RATE = 0.04  # Tasa libre de riesgo (4% anual)
MIN_WEIGHT = 0.0       # Peso mínimo por activo (0 = permitir 0%)
MAX_WEIGHT = 0.40      # Peso máximo por activo (0.4 = máximo 40%)
```

## 📈 Tipos de Activos Soportados

Puedes usar cualquier símbolo válido de Yahoo Finance:

- **Acciones**: `AAPL`, `MSFT`, `GOOGL`, `TSLA`, `JPM`, etc.
- **ETFs**: `SPY`, `QQQ`, `VTI`, `VEA`, `AGG`, etc.
- **Criptomonedas**: `BTC-USD`, `ETH-USD`, `ADA-USD`, etc.
- **Divisas**: `EURUSD=X`, `GBPUSD=X`, `USDJPY=X`, etc.
- **Índices**: `^GSPC` (S&P 500), `^DJI` (Dow Jones), `^IXIC` (NASDAQ), etc.

## 📊 Ejemplo de Salida

```
======================================================================
RESULTADOS DE LA OPTIMIZACIÓN
======================================================================

Pesos Óptimos del Portafolio:
----------------------------------------------------------------------
  AAPL    :   0.00% 
  GOOGL   :  12.42% ██████
  JNJ     :  14.66% ███████
  JPM     :  31.90% ███████████████
  WMT     :  39.29% ███████████████████

Métricas del Portafolio Óptimo:
----------------------------------------------------------------------
  Retorno Esperado:    35.48% anual
  Volatilidad:         15.05% anual
  Ratio de Sharpe:      2.09
```

## 🔍 ¿Qué Hace el Script?

1. **Descarga Datos**: Obtiene precios históricos de Yahoo Finance
2. **Calcula Métricas**: Computa retornos esperados, volatilidades y correlaciones
3. **Optimiza**: Encuentra la asignación óptima de pesos que maximiza el ratio de Sharpe
4. **Muestra Resultados**: Presenta los pesos óptimos y métricas del portafolio

## 📝 Interpretación de Resultados

### Ratio de Sharpe
- **< 1.0**: Retorno bajo ajustado por riesgo
- **1.0 - 2.0**: Buen retorno ajustado por riesgo
- **> 2.0**: Excelente retorno ajustado por riesgo

### Volatilidad
Representa el riesgo anual del portafolio. Menor volatilidad = menor riesgo.

### Retorno Esperado
Retorno anual esperado basado en datos históricos (no garantiza resultados futuros).

## 🛠️ Ejemplos de Uso

### Portafolio de Tech Stocks

```python
TICKERS = ['AAPL', 'MSFT', 'GOOGL', 'NVDA', 'META']
```

### Portafolio Diversificado por Sectores

```python
TICKERS = [
    'AAPL',   # Tecnología
    'JPM',    # Financiero
    'JNJ',    # Salud
    'XOM',    # Energía
    'PG',     # Consumo
    'CAT',    # Industrial
]
```

### Portafolio de ETFs

```python
TICKERS = [
    'SPY',    # S&P 500
    'QQQ',    # NASDAQ
    'VTI',    # Total Stock Market
    'AGG',    # Bonos
    'GLD',    # Oro
]
```

### Portafolio con Criptomonedas

```python
TICKERS = [
    'BTC-USD',  # Bitcoin
    'ETH-USD',  # Ethereum
    'AAPL',     # Apple
    'MSFT',     # Microsoft
    'GLD',      # Oro
]
```

## ⚠️ Advertencias

1. **No es Asesoría Financiera**: Este script es solo para fines educativos
2. **Datos Históricos**: Los resultados se basan en datos pasados, que no garantizan rendimientos futuros
3. **Validación**: Siempre valida los resultados y considera otros factores (costos, impuestos, liquidez, etc.)
4. **Conexión a Internet**: Requiere conexión para descargar datos de Yahoo Finance

## 🔧 Solución de Problemas

### Error al descargar datos

Si un ticker no se puede descargar:
- Verifica que el símbolo sea correcto en Yahoo Finance
- Algunos mercados pueden tener retrasos en los datos
- Algunos activos pueden no tener suficiente historial

### Optimización no converge

Si ves una advertencia de convergencia:
- Aumenta el periodo de datos históricos
- Reduce el número de activos
- Ajusta los límites `MIN_WEIGHT` y `MAX_WEIGHT`

## 📚 Recursos Adicionales

- [Documentación de yfinance](https://pypi.org/project/yfinance/)
- [Yahoo Finance](https://finance.yahoo.com/)
- [Teoría Moderna del Portafolio](https://en.wikipedia.org/wiki/Modern_portfolio_theory)
- [Ratio de Sharpe](https://en.wikipedia.org/wiki/Sharpe_ratio)

## 📄 Licencia

Ver archivo `LICENSE` en el repositorio.
