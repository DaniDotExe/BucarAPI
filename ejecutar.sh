#!/bin/bash
# Script para ejecutar el programa con el entorno virtual activado

echo "Activando entorno virtual..."
source venv/bin/activate

echo "Ejecutando extracción de datos..."
python Main.py

echo ""
echo "Proceso completado. Presiona Enter para salir..."
read
