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

### Ejecutar: Proceso completo 🚀

### Archivos generados

- **datos_meteorologicos_bucaramanga.xlsx**: Datos sin unidades en columnas
- **datos_meteorologicos_bucaramanga_con_unidades.xlsx**: Datos con unidades (RECOMENDADO)

Las unidades agregadas son:
- Temperatura → Temperatura (°C)
- Presión → Presión (hPa)
- Humedad → Humedad (%)
- Punto de Rocío → Punto de Rocío (°C)
- Precipitación → Precipitación (mm)
- Dirección Viento → Dirección Viento (°)
- Velocidad Viento → Velocidad Viento (km/h)
- Y todas las demás columnas con sus respectivas unidades


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

## Scripts disponibles

| Script | Descripción |
|--------|-------------|
| `Main.py` | Extrae datos meteorológicos de Meteostat y genera archivo Excel sin unidades |
| `agregar_unidades.py` | Toma el archivo Excel y agrega unidades a los nombres de columnas |
| `proceso_completo.py` | Ejecuta ambos procesos automáticamente (Main.py + agregar_unidades.py) |
