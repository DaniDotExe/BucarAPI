#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para identificar y almacenar fechas/horas con datos faltantes
de Temperatura, Presión y Humedad en JSON
Fecha: 2025-10-20
"""

import pandas as pd
import sys
import os
from datetime import datetime
import json

def almacenar_datos_faltantes(archivo_entrada):
    """
    Identifica y almacena las fechas y horas donde faltan datos
    de temperatura, presión o humedad.
    
    Args:
        archivo_entrada (str): Ruta del archivo Excel a analizar
        
    Returns:
        dict: Diccionario con los datos faltantes organizados por tipo
    """
    
    if not os.path.exists(archivo_entrada):
        print(f"❌ Error: El archivo '{archivo_entrada}' no existe.")
        return None
    
    print(f"\n{'='*70}")
    print(f"ANÁLISIS DE DATOS FALTANTES")
    print(f"{'='*70}")
    print(f"📁 Archivo: {archivo_entrada}")
    
    try:
        # Leer el archivo Excel
        df = pd.read_excel(archivo_entrada)
        print(f"✓ Archivo cargado exitosamente")
        print(f"  Total de registros: {len(df)}")
        
        # Buscar columnas (ignorar mayúsculas y unidades)
        columnas_interes = {}
        for col in df.columns:
            col_lower = col.lower()
            if 'temperatura' in col_lower:
                columnas_interes['Temperatura'] = col
            elif 'presión' in col_lower or 'presion' in col_lower:
                columnas_interes['Presión'] = col
            elif 'humedad' in col_lower:
                columnas_interes['Humedad'] = col
        
        if not columnas_interes:
            print("❌ No se encontraron columnas de Temperatura, Presión o Humedad")
            return None
        
        print(f"\n📊 Columnas encontradas:")
        for tipo, col in columnas_interes.items():
            print(f"  • {tipo}: '{col}'")
        
        # Estructura para almacenar datos faltantes
        datos_faltantes = {
            'metadata': {
                'archivo': archivo_entrada,
                'fecha_analisis': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'total_registros': len(df)
            },
            'temperatura': {
                'registros_faltantes': [],
                'total_faltantes': 0,
                'porcentaje': 0.0
            },
            'presion': {
                'registros_faltantes': [],
                'total_faltantes': 0,
                'porcentaje': 0.0
            },
            'humedad': {
                'registros_faltantes': [],
                'total_faltantes': 0,
                'porcentaje': 0.0
            },
            'resumen': {
                'registros_con_datos_completos': 0,
                'registros_con_al_menos_un_faltante': 0
            }
        }
        
        print(f"\n{'='*70}")
        print("ANÁLISIS DETALLADO")
        print(f"{'='*70}")
        
        # Verificar cada tipo de dato
        for tipo, col in columnas_interes.items():
            tipo_key = tipo.lower().replace('ó', 'o').replace('í', 'i')
            
            # Identificar valores faltantes (NaN o None)
            mask_faltantes = df[col].isna()
            total_faltantes = mask_faltantes.sum()
            porcentaje = (total_faltantes / len(df)) * 100
            
            # Almacenar información
            datos_faltantes[tipo_key]['total_faltantes'] = int(total_faltantes)
            datos_faltantes[tipo_key]['porcentaje'] = round(porcentaje, 2)
            
            # Extraer fechas y horas de registros faltantes
            if total_faltantes > 0:
                # Intentar seleccionar columnas comunes; si no existen, usar índices
                cols_for_output = []
                for posible in ['Ciudad', 'Ciudad ' , 'fecha', 'Fecha']:
                    if posible in df.columns and 'Ciudad' not in cols_for_output:
                        cols_for_output.append('Ciudad' if posible.lower().startswith('ciudad') else posible)
                for posible in ['Fecha', 'fecha']:
                    if posible in df.columns:
                        cols_for_output.append(posible)
                        break
                for posible in ['Hora', 'hora', 'Time', 'time']:
                    if posible in df.columns:
                        cols_for_output.append(posible)
                        break

                # Si faltaron columnas, crear con valores vacíos para evitar errores
                for name in ['Ciudad', 'Fecha', 'Hora']:
                    if name not in df.columns:
                        df[name] = ''

                df_faltantes = df[mask_faltantes][['Ciudad', 'Fecha', 'Hora']].copy()
                
                # Convertir a lista de diccionarios
                registros = []
                for _, row in df_faltantes.iterrows():
                    registros.append({
                        'ciudad': '' if pd.isna(row['Ciudad']) else str(row['Ciudad']),
                        'fecha': '' if pd.isna(row['Fecha']) else str(row['Fecha']),
                        'hora': '' if pd.isna(row['Hora']) else str(row['Hora'])
                    })
                
                datos_faltantes[tipo_key]['registros_faltantes'] = registros
            
            # Mostrar estadísticas
            print(f"\n{tipo}:")
            print(f"  • Total faltantes: {total_faltantes} de {len(df)} ({porcentaje:.2f}%)")
            
            if total_faltantes > 0:
                print(f"  • Primeros 5 registros con datos faltantes:")
                for i, reg in enumerate(datos_faltantes[tipo_key]['registros_faltantes'][:5], 1):
                    print(f"    {i}. {reg['fecha']} {reg['hora']} - {reg['ciudad']}")
                
                if total_faltantes > 5:
                    print(f"    ... y {total_faltantes - 5} registros más")
        
        # Calcular resumen general
        mask_completo = True
        for col in columnas_interes.values():
            mask_completo &= ~df[col].isna()
        
        datos_faltantes['resumen']['registros_con_datos_completos'] = int(mask_completo.sum())
        datos_faltantes['resumen']['registros_con_al_menos_un_faltante'] = int((~mask_completo).sum())
        
        print(f"\n{'='*70}")
        print("RESUMEN GENERAL")
        print(f"{'='*70}")
        print(f"  ✓ Registros completos: {datos_faltantes['resumen']['registros_con_datos_completos']}")
        print(f"  ⚠ Registros con al menos un dato faltante: {datos_faltantes['resumen']['registros_con_al_menos_un_faltante']}")
        
        return datos_faltantes
        
    except Exception as e:
        print(f"❌ Error al procesar el archivo: {e}")
        import traceback
        traceback.print_exc()
        return None

def guardar_datos_faltantes(datos_faltantes, archivo_salida=None):
    """
    Guarda los datos faltantes únicamente en formato JSON.
    
    Args:
        datos_faltantes (dict): Diccionario con los datos faltantes
        archivo_salida (str): Nombre base para el archivo de salida (opcional)
    """
    
    if datos_faltantes is None:
        return
    
    # Determinar nombre de archivo de salida
    if archivo_salida is None:
        archivo_entrada = datos_faltantes['metadata']['archivo']
        base = os.path.splitext(os.path.basename(archivo_entrada))[0]
        archivo_salida = f"Datos_Faltantes_{base}.json"
    else:
        # Asegurar extensión .json
        if not archivo_salida.lower().endswith('.json'):
            archivo_salida = f"{archivo_salida}.json"
    
    print(f"\n{'='*70}")
    print("GUARDANDO RESULTADOS (JSON)")
    print(f"{'='*70}")
    
    try:
        with open(archivo_salida, 'w', encoding='utf-8') as f:
            json.dump(datos_faltantes, f, ensure_ascii=False, indent=2, default=str)
        print(f"✓ Resultados guardados en JSON: {archivo_salida}")
    except Exception as e:
        print(f"❌ Error al guardar JSON: {e}")
    
    print(f"\n{'='*70}")

def main():
    """
    Función principal
    """
    if len(sys.argv) > 1:
        archivo_entrada = sys.argv[1]
    else:
        # Buscar archivos Excel en el directorio actual
        archivos_excel = [f for f in os.listdir('.') if f.endswith('.xlsx') and not f.startswith('~')]
        
        if not archivos_excel:
            print("❌ No se encontraron archivos Excel en el directorio actual.")
            print("\nUso:")
            print("  python almacenar_datos_faltantes.py archivo.xlsx")
            return
        
        print("Archivos Excel encontrados:")
        for i, archivo in enumerate(archivos_excel, 1):
            print(f"  {i}. {archivo}")
        
        try:
            seleccion = int(input("\nSeleccione el número de archivo a analizar: "))
            archivo_entrada = archivos_excel[seleccion - 1]
        except (ValueError, IndexError):
            print("❌ Selección inválida.")
            return
    
    # Analizar y almacenar datos faltantes
    datos_faltantes = almacenar_datos_faltantes(archivo_entrada)
    
    if datos_faltantes:
        guardar_datos_faltantes(datos_faltantes)
        
        print(f"\n{'='*70}")
        print("✅ PROCESO COMPLETADO")
        print(f"{'='*70}\n")

if __name__ == "__main__":
    main()
