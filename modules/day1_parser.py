
#!/usr/bin/env python3
"""
MÓDULO 1: Extractor de Telemetría SSH (py-sentinel-soc)
Objetivo: Identificar eventos de inicio de sesión fallidos y extraer la IP de origen.
"""

import re

# Expresión regular para capturar la IP en eventos de fallo SSH
SSH_FAILED_PATTERN = re.compile(
    r"Failed password for (?:invalid user )?\w+ from (?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
)

def extract_attacker_ip(log_line):
    """Analiza una línea de log y retorna la IP si es un intento fallido."""
    match = SSH_FAILED_PATTERN.search(log_line)
    if match:
        return match.group("ip")
    return None

def run_tests():
    """Prueba el parser con líneas de ejemplo de logs reales."""
    test_logs = [
        "Oct 24 10:15:30 srv-linux sshd[2041]: Failed password for root from 192.168.1.50 port 45222 ssh2",
        "Oct 24 10:15:32 srv-linux sshd[2042]: Failed password for invalid user admin from 10.0.0.15 port 33112 ssh2",
        "Oct 24 10:15:35 srv-linux sshd[2043]: Accepted password for eric from 192.168.1.10 port 50111 ssh2",
    ]

    print("=== PROBANDO MÓDULO 1 (PARSER REGEX) ===")
    for line in test_logs:
        ip = extract_attacker_ip(line)
        if ip:
            print(f"[🚨 AMENAZA DETECTADA] IP Atacante: {ip}")
        else:
            print("[🟢 EVENTO NORMAL] Acceso permitido u otro log.")

if __name__ == "__main__":
    run_tests()

