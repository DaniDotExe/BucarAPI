"""
Script para analizar valores únicos de Fecha en archivos Excel (versión completa)
Fecha: 2025-10-20
"""

import pandas as pd
import sys
import os

def analizar_fechas_completo(archivo_entrada):
    """
    Analiza los valores únicos de la columna Fecha en un archivo Excel
    con análisis completo y visualización
    
    Args:
        archivo_entrada (str): Ruta del archivo Excel a analizar
    """
    
    if not os.path.exists(archivo_entrada):
        print(f"❌ Error: El archivo '{archivo_entrada}' no existe.")
        return
    
    print(f"\n{'='*80}")
    print(f"ANÁLISIS COMPLETO DE FECHAS")
    print(f"{'='*80}")
    print(f"📁 Archivo: {archivo_entrada}")
    
    try:
        # Leer el archivo Excel
        df = pd.read_excel(archivo_entrada)
        print(f"✓ Archivo cargado exitosamente")
        print(f"  Total de registros: {len(df):,}")
        
        # Buscar columna de Fecha
        columna_fecha = None
        for col in df.columns:
            if 'fecha' in col.lower():
                columna_fecha = col
                break
        
        if columna_fecha is None:
            print("❌ No se encontró una columna 'Fecha' en el archivo.")
            print(f"Columnas disponibles: {', '.join(df.columns)}")
            return
        
        print(f"✓ Columna encontrada: '{columna_fecha}'")
        
        # Obtener valores únicos de Fecha
        fechas_unicas = df[columna_fecha].dropna().unique()
        total_fechas_unicas = len(fechas_unicas)
        
        # Contar repeticiones de cada fecha
        contador_fechas = df[columna_fecha].value_counts().sort_index()
        
        # Convertir fechas a datetime para ordenar correctamente
        try:
            df_temp = pd.DataFrame({
                'Fecha': contador_fechas.index,
                'Repeticiones': contador_fechas.values
            })
            df_temp['Fecha_dt'] = pd.to_datetime(df_temp['Fecha'], dayfirst=True, errors='coerce')
            df_temp = df_temp.sort_values('Fecha_dt')
            contador_fechas = pd.Series(
                df_temp['Repeticiones'].values,
                index=df_temp['Fecha'].values
            )
        except:
            pass  # Si falla, mantener el orden original
        
        print(f"\n{'='*80}")
        print(f"RESUMEN GENERAL")
        print(f"{'='*80}")
        print(f"📊 Total de fechas únicas: {total_fechas_unicas:,}")
        print(f"📊 Total de registros con fecha: {df[columna_fecha].notna().sum():,}")
        print(f"📊 Registros sin fecha: {df[columna_fecha].isna().sum():,}")
        
        # Estadísticas
        print(f"\n{'='*80}")
        print(f"ESTADÍSTICAS DE REPETICIONES")
        print(f"{'='*80}")
        print(f"📈 Máximo de registros por fecha: {contador_fechas.max():,}")
        print(f"📈 Fecha con más registros: {contador_fechas.idxmax()} ({contador_fechas.max():,} registros)")
        print(f"📉 Mínimo de registros por fecha: {contador_fechas.min():,}")
        print(f"📉 Fecha con menos registros: {contador_fechas.idxmin()} ({contador_fechas.min():,} registros)")
        print(f"📊 Promedio de registros por fecha: {contador_fechas.mean():.2f}")
        print(f"📊 Mediana de registros por fecha: {contador_fechas.median():.0f}")
        print(f"📊 Desviación estándar: {contador_fechas.std():.2f}")
        
        # Mostrar primeras 10 y últimas 10 fechas
        print(f"\n{'='*80}")
        print(f"PRIMERAS 10 FECHAS")
        print(f"{'='*80}")
        print(f"{'#':<5} {'Fecha':<20} {'Repeticiones':<15} {'Porcentaje'}")
        print(f"{'-'*80}")
        
        total_con_fecha = df[columna_fecha].notna().sum()
        
        for i, (fecha, cantidad) in enumerate(list(contador_fechas.items())[:10], 1):
            porcentaje = (cantidad / total_con_fecha) * 100
            print(f"{i:<5} {str(fecha):<20} {cantidad:<15,} {porcentaje:.2f}%")
        
        if total_fechas_unicas > 20:
            print(f"\n... ({total_fechas_unicas - 20} fechas intermedias) ...")
        
        if total_fechas_unicas > 10:
            print(f"\n{'='*80}")
            print(f"ÚLTIMAS 10 FECHAS")
            print(f"{'='*80}")
            print(f"{'#':<5} {'Fecha':<20} {'Repeticiones':<15} {'Porcentaje'}")
            print(f"{'-'*80}")
            
            for i, (fecha, cantidad) in enumerate(list(contador_fechas.items())[-10:], total_fechas_unicas - 9):
                porcentaje = (cantidad / total_con_fecha) * 100
                print(f"{i:<5} {str(fecha):<20} {cantidad:<15,} {porcentaje:.2f}%")
        
        # Análisis de consistencia
        print(f"\n{'='*80}")
        print(f"ANÁLISIS DE CONSISTENCIA")
        print(f"{'='*80}")
        
        # Verificar si todas las fechas tienen la misma cantidad de registros
        if contador_fechas.nunique() == 1:
            print(f"✅ Todas las fechas tienen exactamente {contador_fechas.iloc[0]} registros (CONSISTENTE)")
        else:
            variacion = ((contador_fechas.max() - contador_fechas.min()) / contador_fechas.mean()) * 100
            print(f"⚠️  Las fechas tienen diferentes cantidades de registros")
            print(f"   Variación: {variacion:.2f}% respecto al promedio")
            
            # Buscar fechas con menos registros de lo esperado
            umbral = contador_fechas.median()
            fechas_bajas = contador_fechas[contador_fechas < umbral * 0.8]
            if len(fechas_bajas) > 0:
                print(f"\n⚠️  Fechas con registros por debajo del 80% de la mediana:")
                for fecha, cantidad in fechas_bajas.items():
                    print(f"   • {fecha}: {cantidad:,} registros ({(cantidad/umbral*100):.1f}% de la mediana)")
        
        # Guardar resultados en CSV
        nombre_salida = f"Analisis_Fechas_{os.path.splitext(os.path.basename(archivo_entrada))[0]}.csv"
        df_resultado = pd.DataFrame({
            'Fecha': contador_fechas.index,
            'Repeticiones': contador_fechas.values,
            'Porcentaje': (contador_fechas.values / total_con_fecha * 100).round(2)
        })
        df_resultado.to_csv(nombre_salida, index=False, encoding='utf-8')
        
        print(f"\n{'='*80}")
        print(f"✓ Resultados completos guardados en: {nombre_salida}")
        print(f"{'='*80}\n")
        
        return {
            'total_fechas_unicas': total_fechas_unicas,
            'total_registros': total_con_fecha,
            'contador': contador_fechas
        }
        
    except Exception as e:
        print(f"❌ Error al procesar el archivo: {e}")
        import traceback
        traceback.print_exc()
        return None

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
            print("  python analizar_fechas_completo.py archivo.xlsx")
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
    
    # Analizar fechas
    analizar_fechas_completo(archivo_entrada)

if __name__ == "__main__":
    main()