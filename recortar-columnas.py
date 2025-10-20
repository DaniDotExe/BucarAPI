#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para exportar solo columnas específicas de un archivo Excel
Fecha: 2025-10-20
"""

import pandas as pd
import sys
import os

def exportar_columnas(archivo_entrada, columnas_deseadas, archivo_salida=None):
    """
    Exporta solo las columnas especificadas de un archivo Excel
    
    Args:
        archivo_entrada (str): Ruta del archivo Excel a procesar
        columnas_deseadas (list): Lista de nombres de columnas a exportar
        archivo_salida (str): Nombre del archivo de salida (opcional)
    """
    
    if not os.path.exists(archivo_entrada):
        print(f"❌ Error: El archivo '{archivo_entrada}' no existe.")
        return
    
    print(f"\n{'='*70}")
    print(f"EXPORTAR COLUMNAS ESPECÍFICAS")
    print(f"{'='*70}")
    print(f"📁 Archivo de entrada: {archivo_entrada}")
    
    try:
        # Leer el archivo Excel
        df = pd.read_excel(archivo_entrada)
        print(f"✓ Archivo cargado exitosamente")
        print(f"  Total de registros: {len(df):,}")
        print(f"  Total de columnas: {len(df.columns)}")
        
        # Mostrar columnas disponibles
        print(f"\n📊 Columnas disponibles en el archivo:")
        for i, col in enumerate(df.columns, 1):
            print(f"  {i}. {col}")
        
        # Buscar columnas (ignorando mayúsculas y caracteres especiales)
        columnas_encontradas = []
        columnas_no_encontradas = []
        
        print(f"\n{'='*70}")
        print(f"BUSCANDO COLUMNAS SOLICITADAS")
        print(f"{'='*70}")
        
        for col_deseada in columnas_deseadas:
            encontrada = False
            for col_real in df.columns:
                # Comparación flexible (ignorar mayúsculas, espacios, acentos)
                col_deseada_limpia = col_deseada.lower().strip()
                col_real_limpia = col_real.lower().strip()
                
                # Remover caracteres especiales
                col_deseada_limpia = col_deseada_limpia.replace('ó', 'o').replace('í', 'i').replace('á', 'a')
                col_real_limpia = col_real_limpia.replace('ó', 'o').replace('í', 'i').replace('á', 'a')
                
                if col_deseada_limpia in col_real_limpia or col_real_limpia in col_deseada_limpia:
                    columnas_encontradas.append(col_real)
                    print(f"✓ '{col_deseada}' → '{col_real}'")
                    encontrada = True
                    break
            
            if not encontrada:
                columnas_no_encontradas.append(col_deseada)
                print(f"❌ '{col_deseada}' → No encontrada")
        
        if columnas_no_encontradas:
            print(f"\n⚠️  Advertencia: Las siguientes columnas no fueron encontradas:")
            for col in columnas_no_encontradas:
                print(f"  • {col}")
        
        if not columnas_encontradas:
            print(f"\n❌ No se encontró ninguna de las columnas solicitadas.")
            return
        
        # Crear DataFrame solo con las columnas encontradas
        df_exportar = df[columnas_encontradas].copy()
        
        print(f"\n{'='*70}")
        print(f"RESULTADO")
        print(f"{'='*70}")
        print(f"✓ Columnas seleccionadas: {len(columnas_encontradas)}")
        print(f"✓ Total de registros: {len(df_exportar):,}")
        
        # Determinar nombre de archivo de salida
        if archivo_salida is None:
            base = os.path.splitext(os.path.basename(archivo_entrada))[0]
            archivo_salida = f"{base}_columnas_seleccionadas.xlsx"
        
        # Guardar archivo
        with pd.ExcelWriter(archivo_salida, engine='openpyxl') as writer:
            df_exportar.to_excel(writer, index=False, sheet_name='Datos')
            
            # Ajustar ancho de columnas
            worksheet = writer.sheets['Datos']
            for idx, col in enumerate(df_exportar.columns, 1):
                max_length = max(
                    df_exportar[col].astype(str).apply(len).max(),
                    len(col)
                ) + 2
                col_letter = chr(64 + idx) if idx <= 26 else chr(64 + idx // 26) + chr(64 + idx % 26)
                worksheet.column_dimensions[col_letter].width = min(max_length, 20)
        
        print(f"\n✓ Archivo exportado exitosamente: {archivo_salida}")
        
        # Mostrar vista previa
        print(f"\n{'='*70}")
        print(f"VISTA PREVIA (Primeras 5 filas)")
        print(f"{'='*70}")
        print(df_exportar.head().to_string(index=False))
        
        print(f"\n{'='*70}\n")
        
    except Exception as e:
        print(f"❌ Error al procesar el archivo: {e}")
        import traceback
        traceback.print_exc()

def main():
    """
    Función principal
    """
    # Columnas deseadas por defecto
    columnas_deseadas = ['Ciudad', 'Fecha', 'Hora', 'Temperatura', 'Presión']
    
    print("\n" + "="*70)
    print("EXPORTAR COLUMNAS ESPECÍFICAS DE EXCEL")
    print("="*70)
    
    if len(sys.argv) > 1:
        archivo_entrada = sys.argv[1]
        
        # Si se proporcionan columnas como argumentos
        if len(sys.argv) > 2:
            columnas_deseadas = sys.argv[2:]
    else:
        # Buscar archivos Excel en el directorio actual
        archivos_excel = [f for f in os.listdir('.') if f.endswith('.xlsx') and not f.startswith('~')]
        
        if not archivos_excel:
            print("❌ No se encontraron archivos Excel en el directorio actual.")
            print("\nUso:")
            print("  python exportar_columnas.py archivo.xlsx")
            print("  python exportar_columnas.py archivo.xlsx Ciudad Fecha Hora Temperatura")
            return
        
        print("\nArchivos Excel encontrados:")
        for i, archivo in enumerate(archivos_excel, 1):
            print(f"  {i}. {archivo}")
        
        try:
            seleccion = int(input("\nSeleccione el número de archivo a procesar: "))
            archivo_entrada = archivos_excel[seleccion - 1]
        except (ValueError, IndexError):
            print("❌ Selección inválida.")
            return
        
        # Preguntar si desea usar columnas por defecto
        print(f"\nColumnas por defecto: {', '.join(columnas_deseadas)}")
        usar_defecto = input("¿Usar estas columnas? (S/n): ").strip().lower()
        
        if usar_defecto == 'n':
            print("\nIngrese los nombres de las columnas separados por comas:")
            columnas_input = input("Columnas: ").strip()
            if columnas_input:
                columnas_deseadas = [col.strip() for col in columnas_input.split(',')]
    
    print(f"\n📋 Columnas a exportar: {', '.join(columnas_deseadas)}")
    
    # Exportar columnas
    exportar_columnas(archivo_entrada, columnas_deseadas)

if __name__ == "__main__":
    main()