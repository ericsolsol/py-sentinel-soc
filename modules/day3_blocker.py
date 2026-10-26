#!/usr/bin/env python3
"""
MÓDULO 3: Motor de Respuesta Automática y Bloqueo de Amenazas (py-sentinel-soc)
Objetivo: Interceptar alertas del Módulo 2 y aplicar reglas de bloqueo en el Firewall de Linux.
"""

import time
import re
import subprocess

MAX_ATTEMPTS = 3
TIME_WINDOW = 30

SSH_FAILED_PATTERN = re.compile(
    r"Failed password for (?:invalid user )?\w+ from (?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
)

failed_attempts = {}
blocked_ips = set()  # Control para no duplicar reglas de bloqueo

def apply_firewall_block(ip_address):
    """Ejecuta comando de firewall o simula el bloqueo si no se tienen permisos root."""
    if ip_address in blocked_ips:
        print(f"[{time.strftime('%H:%M:%S')}] ℹ️  La IP {ip_address} ya se encuentra bloqueada.")
        return

    blocked_ips.add(ip_address)
    print(f"[{time.strftime('%H:%M:%S')}] 🛡️  [ACCION DEFENSIVA] Aplicando regla de firewall para {ip_address}...")
    
    # Comando hipotético de iptables para bloqueo SSH
    cmd = f"sudo iptables -A INPUT -s {ip_address} -p tcp --dport 22 -j DROP"
    
    try:
        # Intentamos ejecutar la regla de firewall
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"[{time.strftime('%H:%M:%S')}] ✅ IP {ip_address} BLOQUEADA CON ÉXITO EN IPTABLES.")
        else:
            # Si se ejecuta sin privilegios root suficientes o en entorno simulado
            print(f"[{time.strftime('%H:%M:%S')}] ⚠️  [SIMULACIÓN REGLA] Comando generado: '{cmd}'")
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] ❌ Error al ejecutar bloqueo: {e}")

def process_failed_attempt(ip_address):
    """Procesa el intento, actualiza el contador y activa la respuesta automatica."""
    current_time = time.time()
    
    if ip_address not in failed_attempts:
        failed_attempts[ip_address] = []
        
    failed_attempts[ip_address].append(current_time)
    failed_attempts[ip_address] = [
        t for t in failed_attempts[ip_address] if current_time - t <= TIME_WINDOW
    ]
    
    attempts_count = len(failed_attempts[ip_address])
    print(f"[{time.strftime('%H:%M:%S')}] ⚠️  Intento fallido desde {ip_address} ({attempts_count}/{MAX_ATTEMPTS})")
    
    if attempts_count >= MAX_ATTEMPTS:
        print(f"[{time.strftime('%H:%M:%S')}] 🚨 UMBRAL SUPERADO por {ip_address}.")
        apply_firewall_block(ip_address)

def run_simulation():
    """Simula ataque de fuerza bruta coordinado."""
    print("=== PROBANDO MÓDULO 3 (RESPUESTA AUTOMÁTICA Y BLOQUEO) ===")
    
    simulated_events = [
        ("192.168.1.100", 0),
        ("192.168.1.100", 1),
        ("192.168.1.100", 1),  # Intento 3 -> ¡Bloqueo de 192.168.1.100!
        ("10.0.0.5", 1),
        ("192.168.1.100", 1),  # Intentos adicionales ignorados (ya está bloqueada)
    ]
    
    for ip, delay in simulated_events:
        time.sleep(delay)
        process_failed_attempt(ip)

if __name__ == "__main__":
    run_simulation()
