# 🚀 INICIO RÁPIDO - Optimización de Portafolio con Datos Reales

## ⚡ Ejecutar en 3 Pasos

### 1️⃣ Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2️⃣ Ejecutar el script
```bash
python main.py
```

### 3️⃣ Ver resultados
```
RESULTADOS DE LA OPTIMIZACIÓN
======================================================================

Pesos Óptimos del Portafolio:
----------------------------------------------------------------------
  WMT     :  39.28% ███████████████████
  JPM     :  31.90% ███████████████
  JNJ     :  14.66% ███████
  GOOGL   :  12.42% ██████

Métricas del Portafolio Óptimo:
----------------------------------------------------------------------
  Retorno Esperado:    35.48% anual
  Volatilidad:         15.05% anual
  Ratio de Sharpe:      2.09
```

---

## 📂 Scripts Disponibles

| Script | Descripción | Nivel |
|--------|-------------|-------|
| `main.py` | Optimización básica (Máximo Sharpe) | ⭐ Principiante |
| `main_advanced.py` | Comparación de estrategias | ⭐⭐ Intermedio |
| `main_interactive.py` | Modo interactivo | ⭐⭐⭐ Flexible |
| `demo.py` | Demostración automatizada | 🎓 Aprendizaje |

---

## 🎯 Personalizar Tickers

Edita cualquier script y cambia la lista:

```python
TICKERS = [
    'AAPL',   # Tu ticker 1
    'MSFT',   # Tu ticker 2
    'GOOGL',  # Tu ticker 3
    # ... agrega más
]
```

Funciona con:
- ✅ Acciones (AAPL, TSLA, NVDA...)
- ✅ ETFs (SPY, QQQ, VTI...)
- ✅ Criptos (BTC-USD, ETH-USD...)
- ✅ Divisas (EURUSD=X...)

---

## 📖 Documentación

- **[SCRIPTS_GUIDE.md](SCRIPTS_GUIDE.md)** - Guía completa de uso
- **[SUMMARY.md](SUMMARY.md)** - Resumen de características
- **[MAIN_README.md](MAIN_README.md)** - Docs del script básico

---

## 💡 Ejemplos Rápidos

### Portafolio Tech
```python
TICKERS = ['AAPL', 'MSFT', 'GOOGL', 'NVDA', 'META']
```

### Portafolio Diversificado
```python
TICKERS = ['AAPL', 'JPM', 'JNJ', 'XOM', 'WMT', 'GLD']
```

### Portafolio ETFs
```python
TICKERS = ['SPY', 'QQQ', 'AGG', 'GLD', 'VTI']
```

---

## ⚙️ Configuración Básica

```python
# Periodo de datos
PERIOD = '2y'  # Opciones: '1y', '2y', '5y', '10y'

# Tasa libre de riesgo (bonos del tesoro)
RISK_FREE_RATE = 0.04  # 4% anual

# Restricciones de peso
MAX_WEIGHT = 0.40  # Máximo 40% por activo
```

---

## 🎓 ¿Nuevo en Finanzas?

### ¿Qué hace este programa?
Encuentra la **mejor combinación** de acciones para tu portafolio, maximizando retornos mientras controla el riesgo.

### ¿Qué es el Ratio de Sharpe?
Mide **cuánto retorno obtienes por cada unidad de riesgo**. Más alto = mejor.

- < 1.0 = Malo ❌
- 1.0-2.0 = Bueno ✅
- \> 2.0 = Excelente ⭐

### ¿Qué es la Volatilidad?
Mide el **riesgo** (qué tanto varía el precio). Más bajo = más estable.

---

## ⚠️ Importante

- 📚 **Solo educativo** - No es asesoría financiera
- 📊 **Datos históricos** - No garantiza resultados futuros
- 💰 **Consulta a un profesional** antes de invertir dinero real

---

## 🆘 Ayuda

### Error: "No se pudo descargar datos"
👉 Verifica que el ticker sea válido en [Yahoo Finance](https://finance.yahoo.com/)

### Quiero cambiar los activos
👉 Edita la lista `TICKERS` en el script

### Quiero probar sin editar código
👉 Ejecuta `python main_interactive.py`

---

## 🎉 ¡Listo!

Ya puedes optimizar portafolios con datos reales del mercado.

**¿Siguiente paso?** Lee [SCRIPTS_GUIDE.md](SCRIPTS_GUIDE.md) para dominar todas las funciones.

---

**Creado con ❤️ usando finean + yfinance**
