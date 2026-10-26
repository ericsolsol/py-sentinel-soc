# 🛡️ py-sentinel-soc

**py-sentinel-soc** es un motor de detección y respuesta automatizada de incidentes (IPS / SOC Automation) escrito en Python para sistemas Linux.

## 🚀 Características
- **Módulo 1 (Parser Regex):** Extrae IPs de ataques SSH en `/var/log/auth.log` con expresiones regulares.
- **Módulo 2 (Ventana de Tiempo):** Correlaciona eventos en memoria reteniendo registros por 30 segundos para evitar falsos positivos.
- **Módulo 3 (Respuesta Automática):** Aplica aislamiento defensivo ejecutando reglas dinámicas en `iptables`.
- **Módulo 4 (SIEM & Telemetría):** Genera logs de auditoría estructurados en formato JSON (`logs/soc_alerts.json`).

## 🛠️ Requisitos e Instalación
- **SO:** Linux (Kali Linux, Ubuntu, Debian)
- **Lenguaje:** Python 3.x
- **Permisos:** Privilegios `sudo` para manipulación de reglas de red (`iptables`).

```bash
git clone [https://github.com/ericsolsol/py-sentinel-soc.git](https://github.com/ericsolsol/py-sentinel-soc.git)
cd py-sentinel-soc
sudo python3 main.py
