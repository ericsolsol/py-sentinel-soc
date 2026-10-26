#!/usr/bin/env python3
"""
PY-SENTINEL-SOC: Security Operations Center Automation Tool
Unifica Parseo Regex, Monitoreo por Ventana de Tiempo, IPS Firewall y SIEM Reporting.
"""

from modules.day1_parser import extract_attacker_ip
from modules.day2_tailer import process_failed_attempt
from modules.day3_blocker import apply_firewall_block
from modules.day4_dashboard import log_alert_to_siem, display_soc_summary

def run_full_pipeline():
    print("="*60)
    print(" 🚀 INICIANDO PY-SENTINEL-SOC (PIPELINE COMPLETO DE SEGURIDAD)")
    print("="*60)

    # Telemetría de prueba
    sample_logs = [
        "Oct 24 10:15:30 srv-linux sshd[2041]: Failed password for root from 192.168.1.100 port 45222 ssh2",
        "Oct 24 10:15:31 srv-linux sshd[2042]: Failed password for admin from 192.168.1.100 port 45223 ssh2",
        "Oct 24 10:15:32 srv-linux sshd[2043]: Failed password for user1 from 192.168.1.100 port 45224 ssh2",
    ]

    for log in sample_logs:
        ip = extract_attacker_ip(log)
        if ip:
            process_failed_attempt(ip)

    # Registro final en SIEM y resumen
    log_alert_to_siem("192.168.1.100", total_attempts=3, action_taken="IPTABLES_DROP")
    display_soc_summary(["192.168.1.100"])

if __name__ == "__main__":
    run_full_pipeline()
