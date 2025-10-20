#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para obtener datos meteorológicos de Bucaramanga usando WeatherAPI
Fecha: 2025-10-20
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
import time

def obtener_datos_meteorologicos(api_key, ciudad="Bucaramanga", lat=7.1193, lon=-73.1227, 
                                 fecha_inicio=None, fecha_fin=None):
    """
    Obtiene datos meteorológicos horarios usando WeatherAPI
    
    Args:
        api_key (str): API key de WeatherAPI
        ciudad (str): Nombre de la ciudad
        lat (float): Latitud
        lon (float): Longitud
        fecha_inicio (datetime): Fecha de inicio
        fecha_fin (datetime): Fecha de fin
    
    Returns:
        DataFrame: Datos meteorológicos en formato compatible con API_meteostat.py
    """
    
    # Definir período de tiempo por defecto
    if fecha_inicio is None:
        fecha_inicio = datetime(2024, 12, 1)
    if fecha_fin is None:
        fecha_fin = datetime(2024, 12, 2)
    
    print("=" * 60)
    print("EXTRACCIÓN DE DATOS METEOROLÓGICOS - WEATHERAPI")
    print("=" * 60)
    print(f"Ciudad: {ciudad}")
    print(f"Coordenadas: Lat {lat}, Lon {lon}")
    print(f"Período: {fecha_inicio.strftime('%d/%m/%Y')} - {fecha_fin.strftime('%d/%m/%Y')}")
    print("Intervalo: Cada hora")
    print("-" * 60)
    
    # URL base de WeatherAPI
    base_url = "http://api.weatherapi.com/v1/history.json"
    
    # Lista para almacenar todos los datos
    todos_los_datos = []
    
    # WeatherAPI limita a consultas de 1 día por request en la API gratuita
    fecha_actual = fecha_inicio
    total_dias = (fecha_fin - fecha_inicio).days + 1
    
    print(f"\nObteniendo datos de {total_dias} días...")
    print("Nota: WeatherAPI puede tener límites de rate. Espere entre solicitudes.\n")
    
    dias_procesados = 0
    
    while fecha_actual <= fecha_fin:
        try:
            # Parámetros de la consulta
            params = {
                'key': api_key,
                'q': f"{lat},{lon}",
                'dt': fecha_actual.strftime('%Y-%m-%d'),
                'hour': 'all'  # Obtener todas las horas del día
            }
            
            # Hacer la solicitud
            response = requests.get(base_url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                
                # Extraer datos horarios
                if 'forecast' in data and 'forecastday' in data['forecast']:
                    for day in data['forecast']['forecastday']:
                        for hour in day['hour']:
                            registro = {
                                'datetime': datetime.strptime(hour['time'], '%Y-%m-%d %H:%M'),
                                'temp': hour.get('temp_c'),  # Temperatura en °C
                                'pressure': hour.get('pressure_mb'),  # Presión en mb (equivalente a hPa)
                                'humidity': hour.get('humidity'),  # Humedad en %
                                'dewpoint': hour.get('dewpoint_c'),  # Punto de rocío en °C
                                'precip': hour.get('precip_mm'),  # Precipitación en mm
                                'wind_dir': hour.get('wind_degree'),  # Dirección del viento en grados
                                'wind_speed': hour.get('wind_kph'),  # Velocidad del viento en km/h
                                'wind_gust': hour.get('gust_kph'),  # Ráfaga de viento en km/h
                                'condition': hour.get('condition', {}).get('text'),  # Condición del tiempo
                                'cloud': hour.get('cloud'),  # Nubosidad en %
                                'feelslike': hour.get('feelslike_c'),  # Sensación térmica en °C
                                'visibility': hour.get('vis_km'),  # Visibilidad en km
                                'uv': hour.get('uv')  # Índice UV
                            }
                            todos_los_datos.append(registro)
                
                dias_procesados += 1
                if dias_procesados % 10 == 0:
                    print(f"Progreso: {dias_procesados}/{total_dias} días procesados...")
                
                # Pequeña pausa para evitar límites de rate
                time.sleep(0.5)
                
            elif response.status_code == 400:
                print(f"⚠️  Advertencia: No hay datos disponibles para {fecha_actual.strftime('%Y-%m-%d')}")
            elif response.status_code == 401:
                print("❌ Error: API key inválida o no autorizada")
                return None
            elif response.status_code == 429:
                print("⚠️  Límite de rate alcanzado. Esperando 60 segundos...")
                time.sleep(60)
                continue  # Reintentar la misma fecha
            else:
                print(f"❌ Error al obtener datos para {fecha_actual.strftime('%Y-%m-%d')}: {response.status_code}")
            
        except Exception as e:
            print(f"❌ Error al procesar {fecha_actual.strftime('%Y-%m-%d')}: {e}")
        
        # Avanzar al siguiente día
        fecha_actual += timedelta(days=1)
    
    if not todos_los_datos:
        print("\n❌ No se obtuvieron datos.")
        return None
    
    # Crear DataFrame con el formato de API_meteostat.py
    df_data = pd.DataFrame(todos_los_datos)
    
    # Crear DataFrame final con columnas en el orden especificado
    df_final = pd.DataFrame()
    df_final['Ciudad'] = [ciudad] * len(df_data)
    df_final['Fecha'] = df_data['datetime'].dt.strftime('%d/%m/%Y')
    df_final['Hora'] = df_data['datetime'].dt.strftime('%H:%M')
    
    # Columnas principales (mismo orden que API_meteostat.py)
    df_final['Temperatura'] = df_data['temp'].round(2) if 'temp' in df_data.columns else None
    df_final['Presión'] = df_data['pressure'].round(2) if 'pressure' in df_data.columns else None
    df_final['Humedad'] = df_data['humidity'].round(2) if 'humidity' in df_data.columns else None
    
    # Datos adicionales
    if 'dewpoint' in df_data.columns:
        df_final['Punto de Rocío'] = df_data['dewpoint'].round(2)
    
    if 'precip' in df_data.columns:
        df_final['Precipitación'] = df_data['precip'].round(2)
    
    if 'wind_dir' in df_data.columns:
        df_final['Dirección Viento'] = df_data['wind_dir'].round(0)
    
    if 'wind_speed' in df_data.columns:
        df_final['Velocidad Viento'] = df_data['wind_speed'].round(2)
    
    if 'wind_gust' in df_data.columns:
        df_final['Ráfaga Viento'] = df_data['wind_gust'].round(2)
    
    if 'condition' in df_data.columns:
        df_final['Condición'] = df_data['condition']
    
    if 'cloud' in df_data.columns:
        df_final['Nubosidad'] = df_data['cloud'].round(0)
    
    if 'feelslike' in df_data.columns:
        df_final['Sensación Térmica'] = df_data['feelslike'].round(2)
    
    if 'visibility' in df_data.columns:
        df_final['Visibilidad'] = df_data['visibility'].round(2)
    
    if 'uv' in df_data.columns:
        df_final['Índice UV'] = df_data['uv'].round(1)
    
    print(f"\n✓ Total de registros obtenidos: {len(df_final)}")
    print(f"✓ Columnas disponibles: {', '.join(df_final.columns)}")
    
    return df_final

def guardar_excel(df, nombre_archivo='WeatherAPI_Bucaramanga.xlsx'):
    """
    Guarda el DataFrame en formato Excel
    """
    if df is None or df.empty:
        print("No hay datos para guardar.")
        return
    
    try:
        # Guardar en Excel con formato
        with pd.ExcelWriter(nombre_archivo, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Datos Meteorológicos')
            
            # Obtener el worksheet para aplicar formato
            worksheet = writer.sheets['Datos Meteorológicos']
            
            # Ajustar ancho de columnas
            for idx, col in enumerate(df.columns, 1):
                max_length = max(
                    df[col].astype(str).apply(len).max(),
                    len(col)
                ) + 2
                col_letter = chr(64 + idx) if idx <= 26 else chr(64 + idx // 26) + chr(64 + idx % 26)
                worksheet.column_dimensions[col_letter].width = min(max_length, 20)
        
        print(f"\n✓ Datos guardados exitosamente en: {nombre_archivo}")
        
        # Mostrar estadísticas básicas
        print("\n" + "=" * 60)
        print("ESTADÍSTICAS BÁSICAS")
        print("=" * 60)
        
        if 'Temperatura' in df.columns and df['Temperatura'].notna().any():
            print(f"Temperatura promedio: {df['Temperatura'].mean():.2f} °C")
            print(f"Temperatura máxima: {df['Temperatura'].max():.2f} °C")
            print(f"Temperatura mínima: {df['Temperatura'].min():.2f} °C")
        
        if 'Humedad' in df.columns and df['Humedad'].notna().any():
            print(f"Humedad promedio: {df['Humedad'].mean():.2f} %")
        
        if 'Presión' in df.columns and df['Presión'].notna().any():
            print(f"Presión promedio: {df['Presión'].mean():.2f} hPa")
        
        print("=" * 60)
        
    except Exception as e:
        print(f"Error al guardar el archivo Excel: {e}")

def main():
    """
    Función principal
    """
    # Solicitar API key
    print("\n" + "=" * 60)
    print("CONFIGURACIÓN DE WEATHERAPI")
    print("=" * 60)
    print("\nPara usar este script necesitas una API key de WeatherAPI.")
    print("Obtén tu API key gratis en: https://www.weatherapi.com/signup.aspx")
    print("\nNota: La versión gratuita tiene límites:")
    print("  • 1,000,000 llamadas/mes")
    print("  • Datos históricos hasta 7 días atrás")
    print("-" * 60)
    
    api_key = input("\nIngresa tu API key de WeatherAPI: ").strip()
    
    if not api_key:
        print("❌ API key no proporcionada. Saliendo...")
        return
    
    # Parámetros de consulta
    ciudad = "Bucaramanga"
    lat = 7.1193
    lon = -73.1227
    fecha_inicio = datetime(2024, 12, 1)
    fecha_fin = datetime(2025, 10, 19)
    
    # Obtener datos
    df = obtener_datos_meteorologicos(api_key, ciudad, lat, lon, fecha_inicio, fecha_fin)
    
    if df is not None:
        # Guardar archivo con formato WeatherAPI_ciudad_fechainicio_fechafin.xlsx
        ciudad_clean = ''.join(c if c.isalnum() or c in ('_', '-') else '_' for c in ciudad).replace(' ', '_')
        fechas = pd.to_datetime(df['Fecha'], dayfirst=True, errors='coerce')
        if not fechas.isnull().all():
            fecha_inicio_str = fechas.min().strftime('%Y%m%d')
            fecha_fin_str = fechas.max().strftime('%Y%m%d')
        else:
            fecha_inicio_str = ''
            fecha_fin_str = ''
        
        nombre_archivo = f'WeatherAPI_{ciudad_clean}_{fecha_inicio_str}_{fecha_fin_str}.xlsx'
        guardar_excel(df, nombre_archivo=nombre_archivo)
        
        # Mostrar primeras y últimas filas
        print("\nPrimeros 5 registros:")
        print(df.head().to_string(index=False))
        print("\nÚltimos 5 registros:")
        print(df.tail().to_string(index=False))
    else:
        print("No se pudieron obtener los datos.")

if __name__ == "__main__":
    main()