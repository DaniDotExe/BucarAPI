# BucarAPI - Extracción de Datos Meteorológicos

Código para obtener datos meteorológicos de la ciudad de Bucaramanga mediante la API de Meteostat.

## Descripción

Este script extrae datos meteorológicos horarios de Bucaramanga, Colombia, usando la librería Meteostat.

### Parámetros de consulta:
- **Ciudad:** Bucaramanga (Lat: 7.1193, Lon: -73.1227, Alt: 959m)
- **Intervalo:** Cada hora
- **Fecha inicio:** 01 Diciembre 2024
- **Fecha fin:** 19 Octubre 2025

### Formato de salida:
Ciudad, Fecha, Hora, Temperatura, Presión, Humedad, [datos adicionales]

**Output:** Archivo .xlsx (Excel)

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

```bash
# Asegúrate de tener el entorno virtual activado
source venv/bin/activate

# Ejecutar el script
python Main.py
```

El script generará un archivo `datos_meteorologicos_bucaramanga.xlsx` con todos los datos.

## Dependencias

- meteostat==1.6.7
- pandas==2.2.3
- openpyxl==3.1.5
- numpy==1.26.4

## Estructura de datos

El archivo Excel generado contiene las siguientes columnas:
- Ciudad
- Fecha
- Hora
- Temperatura (°C)
- Presión (hPa)
- Humedad (%)
- Punto de Rocío (°C) *
- Precipitación (mm) *
- Dirección del Viento (°) *
- Velocidad del Viento (km/h) *
- Ráfaga de Viento (km/h) *
- Horas de Sol (min) *
- Condición del Tiempo *

*Campos adicionales disponibles según la estación meteorológica