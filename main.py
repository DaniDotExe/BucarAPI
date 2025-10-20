#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script integrado que ejecuta el proceso completo:
1. Extrae datos meteorológicos de Bucaramanga
2. Agrega unidades a las columnas
Fecha: 2025-10-20
"""

import sys
import os
import pandas as pd

# Importar funciones de los otros scripts
from API_meteostat import obtener_datos_meteorologicos, guardar_excel
from agregar_unidades import agregar_unidades_excel

def proceso_completo():
    """
    Ejecuta el proceso completo de extracción y formato de datos
    """
    print("\n" + "=" * 70)
    print("PROCESO COMPLETO DE EXTRACCIÓN DE DATOS METEOROLÓGICOS")
    print("=" * 70)
    print("\n📍 Paso 1/2: Extrayendo datos meteorológicos de Bucaramanga...")
    print("-" * 70)
    
    # Paso 1: Obtener datos meteorológicos
    df = obtener_datos_meteorologicos()
    
    if df is not None:
        # Guardar en Excel
        # Guardar archivo con formato ciudad_fechainicio_fechafin.xlsx
        ciudad = str(df['Ciudad'].iloc[0])
        # Convertir 'Fecha' (dd/mm/YYYY) a datetime y obtener fecha inicio/fin en YYYYMMDD
        fechas = pd.to_datetime(df['Fecha'], dayfirst=True, errors='coerce')
        if not fechas.isnull().all():
            fecha_inicio = fechas.min().strftime('%Y%m%d')
            fecha_fin = fechas.max().strftime('%Y%m%d')
        else:
            fecha_inicio = ''
            fecha_fin = ''
        # Sanitizar nombre de ciudad para evitar caracteres inválidos en el nombre de archivo
        ciudad_clean = ''.join(c if c.isalnum() or c in ('_', '-') else '_' for c in ciudad).replace(' ', '_')
        nombre_archivo = f'{ciudad_clean}_{fecha_inicio}_{fecha_fin}.xlsx'
        guardar_excel(df, nombre_archivo=nombre_archivo)
        
        # Mostrar primeras y últimas filas
        print("\nPrimeros 5 registros:")
        print(df.head().to_string(index=False))
        print("\nÚltimos 5 registros:")
        print(df.tail().to_string(index=False))
    else:
        print("No se pudieron obtener los datos.")
    
    # Guardar datos sin unidades
    archivo_sin_unidades = nombre_archivo
    guardar_excel(df, archivo_sin_unidades)
    
    print("\n" + "=" * 70)
    print("📍 Paso 2/2: Agregando unidades a las columnas...")
    print("-" * 70)
    
    # Paso 2: Agregar unidades
    base, ext = os.path.splitext(nombre_archivo)
    if not ext:
        ext = '.xlsx'
    archivo_con_unidades = f"{base}_u{ext}"

    exito = agregar_unidades_excel(archivo_sin_unidades, archivo_con_unidades)
    
    if not exito:
        print("\n❌ Error al agregar unidades.")
        return False
    
    print("\n" + "=" * 70)
    print("✅ PROCESO COMPLETADO EXITOSAMENTE")
    print("=" * 70)
    print("\nArchivos generados:")
    print(f"  1. {archivo_sin_unidades}")
    print(f"     └─ Datos sin unidades en los nombres de columnas")
    print(f"\n  2. {archivo_con_unidades}")
    print(f"     └─ Datos CON unidades en los nombres de columnas (RECOMENDADO)")
    print("\n" + "=" * 70)
    
    return True

def main():
    """
    Función principal
    """
    try:
        exito = proceso_completo()
        sys.exit(0 if exito else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Proceso interrumpido por el usuario.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
