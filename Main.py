#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para obtener datos meteorológicos de Bucaramanga usando Meteostat API
Fecha: 2025-10-20
"""

from datetime import datetime
from meteostat import Point, Hourly
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

def obtener_datos_meteorologicos():
    """
    Obtiene datos meteorológicos horarios de Bucaramanga usando Meteostat
    """
    
    # Coordenadas de Bucaramanga, Colombia
    # Latitud: 7.1193, Longitud: -73.1227, Altitud: 959 metros
    bucaramanga = Point(7.1193, -73.1227, 959)
    
    # Definir período de tiempo
    fecha_inicio = datetime(2024, 12, 1)
    fecha_fin = datetime(2025, 10, 19)
    
    print("Obteniendo datos meteorológicos de Bucaramanga...")
    print(f"Período: {fecha_inicio.strftime('%d/%m/%Y')} - {fecha_fin.strftime('%d/%m/%Y')}")
    print("Intervalo: Cada hora")
    print("-" * 60)
    
    # Obtener datos horarios
    data = Hourly(bucaramanga, fecha_inicio, fecha_fin)
    data = data.fetch()
    
    if data.empty:
        print("No se encontraron datos para el período especificado.")
        return None
    
    # Resetear el índice para tener la columna 'time' disponible
    data = data.reset_index()
    
    # Crear DataFrame con las columnas en el orden especificado
    df_final = pd.DataFrame()
    df_final['Ciudad'] = ['Bucaramanga'] * len(data)
    df_final['Fecha'] = data['time'].dt.strftime('%d/%m/%Y')
    df_final['Hora'] = data['time'].dt.strftime('%H:%M')
    
    # Agregar columnas meteorológicas en el orden especificado
    # Temperatura (temp) - en °C
    df_final['Temperatura'] = data['temp'].round(2) if 'temp' in data.columns else None
    
    # Presión (pres) - en hPa
    df_final['Presión'] = data['pres'].round(2) if 'pres' in data.columns else None
    
    # Humedad (rhum) - en %
    df_final['Humedad'] = data['rhum'].round(2) if 'rhum' in data.columns else None
    
    # Agregar datos adicionales si existen
    if 'dwpt' in data.columns:
        df_final['Punto de Rocío'] = data['dwpt'].round(2)
    
    if 'prcp' in data.columns:
        df_final['Precipitación'] = data['prcp'].round(2)
    
    if 'snow' in data.columns:
        df_final['Nieve'] = data['snow'].round(2)
    
    if 'wdir' in data.columns:
        df_final['Dirección Viento'] = data['wdir'].round(0)
    
    if 'wspd' in data.columns:
        df_final['Velocidad Viento'] = data['wspd'].round(2)
    
    if 'wpgt' in data.columns:
        df_final['Ráfaga Viento'] = data['wpgt'].round(2)
    
    if 'tsun' in data.columns:
        df_final['Horas Sol'] = data['tsun'].round(0)
    
    if 'coco' in data.columns:
        df_final['Condición'] = data['coco']
    
    print(f"\nTotal de registros obtenidos: {len(df_final)}")
    print(f"Columnas disponibles: {', '.join(df_final.columns)}")
    
    return df_final

def guardar_excel(df, nombre_archivo='datos_meteorologicos_bucaramanga.xlsx'):
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
                worksheet.column_dimensions[chr(64 + idx)].width = min(max_length, 20)
        
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
    print("=" * 60)
    print("EXTRACCIÓN DE DATOS METEOROLÓGICOS - BUCARAMANGA")
    print("=" * 60)
    print()
    
    # Obtener datos
    df = obtener_datos_meteorologicos()
    
    if df is not None:
        # Guardar en Excel
        guardar_excel(df)
        
        # Mostrar primeras y últimas filas
        print("\nPrimeros 5 registros:")
        print(df.head().to_string(index=False))
        print("\nÚltimos 5 registros:")
        print(df.tail().to_string(index=False))
    else:
        print("No se pudieron obtener los datos.")

if __name__ == "__main__":
    main()
