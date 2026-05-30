#!/bin/bash
# Script de inicio para Cloudera Applications con Gunicorn

cd /home/cdsw/HermesCalendar

# Obtener puerto de Cloudera
PORT=${CDSW_APP_PORT:-8080}

echo "🚀 Iniciando Gunicorn en puerto $PORT..."

# Ejecutar Gunicorn
exec gunicorn \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --threads 4 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    run:application
