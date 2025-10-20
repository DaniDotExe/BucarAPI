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

### Opción 1: Proceso completo (Recomendado) 🚀

Ejecuta todo el proceso de una sola vez:

```bash
# Usando el script interactivo
./ejecutar.sh
# Selecciona la opción 1

# O directamente:
source venv/bin/activate
python proceso_completo.py
```

Este script ejecuta automáticamente:
1. Extracción de datos de Meteostat
2. Generación de archivo con unidades

### Opción 2: Ejecución paso a paso

#### 2.1. Extracción de datos meteorológicos

```bash
source venv/bin/activate
python Main.py
```

Genera: `datos_meteorologicos_bucaramanga.xlsx`

#### 2.2. Agregar unidades a las columnas

```bash
python agregar_unidades.py
```

Genera: `datos_meteorologicos_bucaramanga_con_unidades.xlsx`

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

## Scripts disponibles

| Script | Descripción |
|--------|-------------|
| `Main.py` | Extrae datos meteorológicos de Meteostat y genera archivo Excel sin unidades |
| `agregar_unidades.py` | Toma el archivo Excel y agrega unidades a los nombres de columnas |
| `proceso_completo.py` | Ejecuta ambos procesos automáticamente (Main.py + agregar_unidades.py) |
| `ejecutar.sh` | Script interactivo con menú para elegir qué ejecutar |
| `verificar_archivos.py` | Verifica y muestra información de los archivos Excel generados |

## Notas

- El archivo con unidades es **más legible** y **recomendado para uso final**
- Ambos archivos contienen los mismos datos, solo difieren en los nombres de columnas
- Los datos históricos están limitados a la disponibilidad de la API de Meteostat