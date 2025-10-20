# BucarAPI - Extracción de Datos Meteorológicos

Código para obtener datos meteorológicos de la ciudad de Bucaramanga mediante la API de WeatherAPI.

## Descripción

Este script extrae datos meteorológicos horarios de Bucaramanga, Colombia, usando la API de WeatherAPI.

### Parámetros de consulta:
- **Ciudad:** Bucaramanga (Lat: 7.1193, Lon: -73.1227)
- **Intervalo:** Cada hora
- **Fecha inicio:** 01 Diciembre 2024
- **Fecha fin:** 19 Octubre 2025

### Formato de salida:
Ciudad, Fecha, Hora, Temperatura, Presión, Humedad, [datos adicionales]

**Output:** Archivo .xlsx (Excel)

## Requisitos

### API Key de WeatherAPI (Gratis)

Obtén tu API key en: https://www.weatherapi.com/signup.aspx

**Plan Gratuito incluye:**
- 1,000,000 llamadas/mes
- Datos en tiempo real

## Instalación

1. Crear y activar el entorno virtual:
```bash
python3 -m venv venv
source venv/bin/activate  # En Linux/Mac
# venv\Scripts\activate   # En Windows
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Uso

### Ejecutar extracción de datos:

```bash
python API_WeatherAPI.py
```

El script solicitará tu API key de WeatherAPI.

### Archivos generados

- **WeatherAPI_[Ciudad]_[FechaInicio]_[FechaFin].xlsx**: Datos meteorológicos completos

Ejemplo: `WeatherAPI_Bucaramanga_20241201_20251019.xlsx`

## Estructura de datos

El archivo Excel generado contiene las siguientes columnas con sus unidades:

### Columnas principales:
- **Ciudad** - Nombre de la ciudad
- **Fecha** - Formato: dd/mm/YYYY
- **Hora** - Formato: HH:MM
- **Temperatura (°C)** - Temperatura en grados Celsius
- **Presión (hPa)** - Presión atmosférica en hectopascales
- **Humedad (%)** - Humedad relativa en porcentaje

### Columnas adicionales:
- **Punto de Rocío (°C)** - Temperatura del punto de rocío
- **Precipitación (mm)** - Precipitación acumulada en milímetros
- **Dirección Viento (°)** - Dirección del viento en grados (0-360)
- **Velocidad Viento (km/h)** - Velocidad del viento en kilómetros por hora
- **Ráfaga Viento (km/h)** - Velocidad de ráfagas de viento
- **Condición** - Descripción del clima (texto)
- **Nubosidad (%)** - Porcentaje de cobertura de nubes
- **Sensación Térmica (°C)** - Temperatura percibida
- **Visibilidad (km)** - Visibilidad en kilómetros
- **Índice UV** - Índice de radiación ultravioleta

## Scripts disponibles

| Script | Descripción |
|--------|-------------|
| `API_WeatherAPI.py` | Extrae datos meteorológicos de WeatherAPI y genera archivo .xlsx |
| `API_meteostat.py` | Extrae datos meteorológicos de Meteostat (alternativa sin API key) |
| `recortar-columnas.py` | Crea un nuevo .xlsx con solo las columnas seleccionadas desde uno o varios archivos de entrada |
| `validacion-empty-data.py` | Verifica valores vacíos/faltantes en archivos .xlsx y genera un informe resumen (opcional: archivo de salida con filas problemáticas o estadísticas) |

## Características de WeatherAPI

### Ventajas:
- ✅ Alta precisión en los datos
- ✅ Datos en tiempo real
- ✅ Más variables meteorológicas disponibles
- ✅ Condiciones del tiempo descriptivas
- ✅ API estable y confiable

### Limitaciones (Plan Gratuito):
- ⚠️ Requiere API key (gratis)
- ⚠️ Límite de 1,000,000 llamadas/mes

### Para datos históricos antiguos:
Si necesitas datos de meses/años anteriores, usa:
- **API_meteostat.py** - Sin límites, gratis, datos históricos completos

## Recursos

- **Documentación WeatherAPI:** https://www.weatherapi.com/docs/
- **Panel de control:** https://www.weatherapi.com/my/
- **Pricing:** https://www.weatherapi.com/pricing.aspx
- **README WeatherAPI:** [README_WeatherAPI.md](README_WeatherAPI.md)

## Soporte

Para más información sobre cada script, consulta los archivos README específicos:
- [README_WeatherAPI.md](README_WeatherAPI.md) - Detalles de WeatherAPI
- [README_Analizar_Fechas.md](README_Analizar_Fechas.md) - Análisis de fechas
- [README_Exportar_Columnas.md](README_Exportar_Columnas.md) - Exportación de columnas
- [README_Analisis_Datos_Faltantes.md](README_Analisis_Datos_Faltantes.md) - Análisis de datos faltantes
