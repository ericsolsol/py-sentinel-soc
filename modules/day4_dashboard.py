#!/usr/bin/env python3
"""
MÓDULO 4: SIEM Alerting & Reporting Engine (py-sentinel-soc)
Objetivo: Generar registros de auditoría JSON y métricas para el SOC.
"""

import time
import json
import os

ALERTS_LOG_FILE = "logs/soc_alerts.json"

def log_alert_to_siem(ip_address, total_attempts, action_taken="BLOCKED"):
    """Registra eventos de seguridad estructurados en formato JSON."""
    os.makedirs("logs", exist_ok=True)
    
    alert_event = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "event_type": "BRUTE_FORCE_DETECTED",
        "severity": "HIGH",
        "source_ip": ip_address,
        "attempts_count": total_attempts,
        "action_enforced": action_taken,
        "target_service": "SSH"
    }
    
    # Guardar en archivo JSON para auditoría SIEM
    with open(ALERTS_LOG_FILE, "a") as f:
        f.write(json.dumps(alert_event) + "\n")
        
    print(f"\n[📊 SIEM LOG GENERATED] Evento guardado en {ALERTS_LOG_FILE}:")
    print(json.dumps(alert_event, indent=2))

def display_soc_summary(blocked_ips):
    """Muestra un resumen ejecutivo de las amenazas mitigadas."""
    print("\n" + "="*50)
    print("      PY-SENTINEL-SOC | METRICAS DE SEGURIDAD")
    print("="*50)
    print(f" Total de IPs bloqueadas activas: {len(blocked_ips)}")
    print(f" Estado del Firewall: PROTEGIDO")
    print(f" Archivo de telemetría SIEM: {ALERTS_LOG_FILE}")
    print("="*50 + "\n")

def run_simulation():
    print("=== PROBANDO MÓDULO 4 (SIEM & REPORTING) ===")
    
    # Simulación de eventos
    test_ip = "192.168.1.100"
    log_alert_to_siem(test_ip, total_attempts=3, action_taken="IPTABLES_DROP")
    
    # Mostrar resumen en consola
    display_soc_summary([test_ip])

if __name__ == "__main__":
    run_simulation()
