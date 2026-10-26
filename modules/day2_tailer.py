#!/usr/bin/env python3
"""
MÓDULO 2: Monitoreo Continuo y Contador por Ventana de Tiempo (py-sentinel-soc)
Objetivo: Procesar eventos en tiempo real y contar intentos dentro de un límite de tiempo.
"""

import time
import re

# Configuración del motor de detección
MAX_ATTEMPTS = 3     # Umbral de intentos para activar la alerta
TIME_WINDOW = 30     # Ventana de tiempo en segundos

SSH_FAILED_PATTERN = re.compile(
    r"Failed password for (?:invalid user )?\w+ from (?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
)

# Estructura de datos en memoria: { "IP": [timestamp1, timestamp2, ...] }
failed_attempts = {}

def process_failed_attempt(ip_address):
    """Registra el intento y limpia los eventos fuera de la ventana de tiempo."""
    current_time = time.time()
    
    if ip_address not in failed_attempts:
        failed_attempts[ip_address] = []
        
    # Añadir timestamp actual
    failed_attempts[ip_address].append(current_time)
    
    # Filtrar eventos quitando los que tengan más de 30 segundos de antigüedad
    failed_attempts[ip_address] = [
        t for t in failed_attempts[ip_address] if current_time - t <= TIME_WINDOW
    ]
    
    attempts_count = len(failed_attempts[ip_address])
    print(f"[{time.strftime('%H:%M:%S')}] ⚠️  Intento fallido desde {ip_address} ({attempts_count}/{MAX_ATTEMPTS})")
    
    if attempts_count >= MAX_ATTEMPTS:
        print(f"[{time.strftime('%H:%M:%S')}] 🚨 UMBRAL SUPERADO: La IP {ip_address} debe ser bloqueada.")

def run_simulation():
    """Simula la llegada de logs con retrasos de tiempo para probar la ventana."""
    print("=== PROBANDO MÓDULO 2 (TAILER Y VENTANA DE TIEMPO) ===")
    
    # Eventos simulados con pausas
    simulated_events = [
        ("192.168.1.100", 0),   # Intento 1
        ("192.168.1.100", 1),   # Intento 2 (1 seg después)
        ("10.0.0.5", 0),       # Intento de otra IP
        ("192.168.1.100", 2),   # Intento 3 -> ¡Debe activar la alerta!
    ]
    
    for ip, delay in simulated_events:
        time.sleep(delay)
        process_failed_attempt(ip)

if __name__ == "__main__":
    run_simulation()
