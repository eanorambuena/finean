# 📊 Guía Completa: Scripts de Optimización de Portafolio

Este proyecto incluye **tres scripts** diferentes para optimizar portafolios con datos reales:

## 🎯 Los Tres Scripts

### 1. `main.py` - Script Básico ⭐ Recomendado para empezar

**Características:**
- ✅ Configuración simple mediante variables en el código
- ✅ Optimización para maximizar el Ratio de Sharpe
- ✅ Salida clara y visual con gráficos de barras
- ✅ Perfecto para análisis rápidos

**Cuándo usar:** Para análisis rápidos con tickers predefinidos.

**Ejemplo de uso:**
```bash
python main.py
```

---

### 2. `main_advanced.py` - Script Avanzado 🚀

**Características:**
- ✅ Dos estrategias de optimización:
  - Maximizar Ratio de Sharpe
  - Minimizar Volatilidad
- ✅ Comparación directa entre ambas estrategias
- ✅ Recomendaciones basadas en los resultados
- ✅ Análisis más profundo del portafolio

**Cuándo usar:** Para comparar diferentes estrategias y obtener recomendaciones.

**Ejemplo de uso:**
```bash
python main_advanced.py
```

---

### 3. `main_interactive.py` - Script Interactivo 💬

**Características:**
- ✅ Interfaz interactiva por consola
- ✅ El usuario elige los parámetros paso a paso
- ✅ Validación de datos en tiempo real
- ✅ Flexible para diferentes escenarios

**Cuándo usar:** Para experimentar con diferentes configuraciones sin modificar código.

**Ejemplo de uso:**
```bash
python main_interactive.py
```

El script te guiará paso a paso:
```
PASO 1: Selección de Activos
----------------------------------------------------------------------
Ingresa los símbolos de las acciones...
Tickers (separados por comas): AAPL, MSFT, GOOGL, TSLA

PASO 2: Periodo de Datos Históricos
----------------------------------------------------------------------
Opciones: 1y, 2y, 5y, 10y
Periodo [2y]: 5y

...etc
```

---

## 📋 Comparación Rápida

| Característica | main.py | main_advanced.py | main_interactive.py |
|----------------|---------|------------------|---------------------|
| Facilidad de uso | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| Flexibilidad | ⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| Análisis profundo | ⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| Comparación de estrategias | ❌ | ✅ | ✅ |
| Interactivo | ❌ | ❌ | ✅ |
| Mejor para | Análisis rápido | Análisis completo | Experimentación |

---

## 🚀 Instalación

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Instalar Dependencias

```bash
pip install -r requirements.txt
```

O manualmente:
```bash
pip install numpy pandas scipy matplotlib yfinance
```

---

## 📖 Ejemplos de Uso

### Ejemplo 1: Portafolio de Tecnología (main.py)

Edita `main.py` y modifica los tickers:

```python
TICKERS = [
    'AAPL',   # Apple
    'MSFT',   # Microsoft
    'GOOGL',  # Alphabet
    'NVDA',   # NVIDIA
    'META',   # Meta
]
```

Ejecuta:
```bash
python main.py
```

**Resultado esperado:**
```
RESULTADOS DE LA OPTIMIZACIÓN
======================================================================

Pesos Óptimos del Portafolio:
----------------------------------------------------------------------
  NVDA    :  40.00% ████████████████████
  MSFT    :  35.50% █████████████████
  GOOGL   :  24.50% ████████████

Métricas del Portafolio Óptimo:
----------------------------------------------------------------------
  Retorno Esperado:    42.15% anual
  Volatilidad:         28.34% anual
  Ratio de Sharpe:      1.35
```

---

### Ejemplo 2: Comparar Estrategias (main_advanced.py)

Edita `main_advanced.py` con tus tickers preferidos y ejecuta:

```bash
python main_advanced.py
```

**Resultado esperado:**
```
COMPARACIÓN DE ESTRATEGIAS
======================================================================

Métrica                        Max Sharpe Min Volatilidad   Diferencia
----------------------------------------------------------------------
Retorno Esperado (%)                35.48           24.36        11.12
Volatilidad (%)                     15.05           12.04         3.01
Ratio de Sharpe                      2.09            1.69         0.40

RECOMENDACIÓN:
----------------------------------------------------------------------
✓ El portafolio de MÁXIMO SHARPE ofrece mejor retorno ajustado por riesgo.
```

---

### Ejemplo 3: Modo Interactivo (main_interactive.py)

```bash
python main_interactive.py
```

Sigue las instrucciones en pantalla:

```
Tickers (separados por comas): AAPL, MSFT, JPM, JNJ, WMT
Periodo [2y]: 5y
Tasa libre de riesgo [0.04]: 0.03
Peso máximo por activo [0.40]: 0.30
Selecciona estrategia [3]: 3
```

---

## 🎨 Personalización

### Cambiar Periodo de Datos

```python
PERIOD = '5y'  # Opciones: '1y', '2y', '5y', '10y', 'max'
```

### Cambiar Tasa Libre de Riesgo

```python
RISK_FREE_RATE = 0.03  # 3% anual (bonos corto plazo)
RISK_FREE_RATE = 0.04  # 4% anual (bonos mediano plazo)
RISK_FREE_RATE = 0.05  # 5% anual (bonos largo plazo)
```

### Cambiar Restricciones de Peso

```python
MIN_WEIGHT = 0.05  # Mínimo 5% por activo
MAX_WEIGHT = 0.25  # Máximo 25% por activo
```

Esto fuerza diversificación (ningún activo puede ser 0% ni más del 25%).

---

## 📊 Tipos de Activos Soportados

### Acciones Individuales
```python
TICKERS = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
```

### ETFs (Fondos Cotizados)
```python
TICKERS = [
    'SPY',   # S&P 500
    'QQQ',   # NASDAQ 100
    'VTI',   # Total US Stock Market
    'AGG',   # Bonos agregados
    'GLD',   # Oro
]
```

### Criptomonedas
```python
TICKERS = ['BTC-USD', 'ETH-USD', 'BNB-USD']
```

### Mix Diversificado
```python
TICKERS = [
    'AAPL',      # Tech
    'JPM',       # Finanzas
    'JNJ',       # Salud
    'XOM',       # Energía
    'SPY',       # ETF S&P
    'GLD',       # Oro
    'BTC-USD',   # Crypto
]
```

---

## 🔍 Interpretación de Resultados

### Ratio de Sharpe

El Ratio de Sharpe mide el retorno ajustado por riesgo:

- **< 1.0**: Retorno bajo por unidad de riesgo (❌ Evitar)
- **1.0 - 1.5**: Retorno aceptable (⚠️ Considerar)
- **1.5 - 2.0**: Buen retorno ajustado (✅ Bueno)
- **> 2.0**: Excelente retorno ajustado (⭐ Excelente)

### Volatilidad

Representa el riesgo (desviación estándar anualizada):

- **< 10%**: Muy bajo riesgo (bonos, activos estables)
- **10-20%**: Riesgo moderado (mix diversificado)
- **20-30%**: Riesgo alto (acciones volátiles)
- **> 30%**: Riesgo muy alto (crypto, acciones especulativas)

### Retorno Esperado

Basado en datos históricos. **NO garantiza resultados futuros**.

- Es un promedio anualizado del periodo histórico
- Considera volatilidad y costos de transacción reales
- Úsalo como referencia, no como predicción

---

## ⚠️ Advertencias Importantes

### 1. No es Asesoría Financiera
Este proyecto es **solo educativo**. No constituye asesoría financiera. Consulta con un profesional antes de invertir.

### 2. Datos Históricos
Los resultados se basan en datos pasados. El rendimiento pasado **no garantiza** resultados futuros.

### 3. Costos No Incluidos
Los cálculos no incluyen:
- Comisiones de compra/venta
- Impuestos sobre ganancias
- Spreads bid-ask
- Costos de rebalanceo

### 4. Supuestos del Modelo
- Asume distribución normal de retornos (no siempre cierto)
- No considera eventos extremos (cisnes negros)
- Asume que las correlaciones se mantienen constantes

---

## 🛠️ Solución de Problemas

### Error: "No se pudo descargar datos"

**Causa:** Ticker inválido o sin datos en Yahoo Finance.

**Solución:** Verifica el ticker en [Yahoo Finance](https://finance.yahoo.com/).

```bash
# Ejemplo: Buscar Apple
# Correcto: AAPL
# Incorrecto: APPLE, APL
```

### Error: "La optimización no convergió"

**Causa:** Restricciones muy estrictas o datos insuficientes.

**Soluciones:**
1. Aumenta el periodo de datos (usa '5y' en vez de '1y')
2. Reduce restricciones de peso (aumenta MAX_WEIGHT)
3. Reduce el número de activos

### Advertencia: "Covariance matrix is not symmetric"

**Causa:** Problema numérico menor (el script lo corrige automáticamente).

**Acción:** Generalmente puedes ignorar esta advertencia.

---

## 📚 Recursos Adicionales

### Teoría
- [Modern Portfolio Theory - Investopedia](https://www.investopedia.com/terms/m/modernportfoliotheory.asp)
- [Sharpe Ratio - Wikipedia](https://en.wikipedia.org/wiki/Sharpe_ratio)
- [Efficient Frontier - Wikipedia](https://en.wikipedia.org/wiki/Efficient_frontier)

### Herramientas
- [Yahoo Finance](https://finance.yahoo.com/) - Buscar tickers
- [Portfolio Visualizer](https://www.portfoliovisualizer.com/) - Análisis complementario
- [ETF Database](https://etfdb.com/) - Información sobre ETFs

### Libros Recomendados
- "A Random Walk Down Wall Street" - Burton Malkiel
- "The Intelligent Investor" - Benjamin Graham
- "Common Sense on Mutual Funds" - John Bogle

---

## 🤝 Contribuciones

¿Encontraste un bug o tienes una sugerencia? ¡Abre un issue o pull request!

---

## 📄 Licencia

Ver archivo `LICENSE` en el repositorio.

---

## 💡 Tips y Mejores Prácticas

### 1. Diversifica

No pongas todos los huevos en la misma canasta:
```python
# ❌ Malo: Solo tech
TICKERS = ['AAPL', 'MSFT', 'GOOGL', 'META']

# ✅ Bueno: Diversificado
TICKERS = ['AAPL', 'JPM', 'JNJ', 'XOM', 'WMT', 'GLD']
```

### 2. Usa Datos Suficientes

Mínimo 2 años de datos históricos:
```python
PERIOD = '2y'  # Mínimo recomendado
PERIOD = '5y'  # Mejor
```

### 3. Considera ETFs

Para inversores principiantes, usa ETFs en lugar de acciones individuales:
```python
TICKERS = ['SPY', 'AGG', 'VEA', 'VWO', 'GLD']  # Portfolio simple y diversificado
```

### 4. Rebalancea Regularmente

Los pesos óptimos cambian con el tiempo. Reoptimiza cada 3-6 meses.

### 5. No Persigas el Rendimiento

Si un activo tuvo altos retornos históricos, no significa que continuará así.

---

## 🎓 Glosario

- **Sharpe Ratio**: Medida de retorno ajustado por riesgo
- **Volatilidad**: Medida de riesgo (desviación estándar)
- **Covarianza**: Medida de cómo se mueven juntos dos activos
- **Correlación**: Covarianza normalizada (-1 a 1)
- **Portafolio Óptimo**: Mejor combinación de activos según criterio elegido
- **Frontera Eficiente**: Conjunto de portafolios óptimos
- **Tasa Libre de Riesgo**: Retorno de una inversión sin riesgo (ej: bonos del tesoro)

---

**¡Feliz optimización! 📈💰**
