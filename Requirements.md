# Requirements.txt

# 📦 Requisitos del Laboratorio

Este proyecto requiere un entorno controlado de laboratorio para ejecutar correctamente la herramienta y reproducir la topología de red.

---

# 🖥 Requisitos de Software

## 🔹 Sistema Operativo (Atacante)

- Kali Linux / Ubuntu / Debian
- Python 3.8 o superior
- Permisos root

## 🔹 Dependencias Python

Instalar mediante pip:

```bash
pip install -r requirements.txt
```

Contenido del archivo `requirements.txt`:

```
scapy>=2.5.0
```

Instalar dependencias del sistema:

```bash
sudo apt update
sudo apt install python3-scapy python3-tk
```

---

# 🌐 Requisitos de Virtualización / Simulación

- PNETLab / EVE-NG / GNS3
- Imagen de Router (Cisco IOS recomendado)
- Switches Layer 2
- Máquinas VPC o Linux clientes
- Servidor DHCP activo (puede ser el Router)

---

# 📡 Requisitos de Red

## 🔹 Configuración LAN

- Red: 23.72.0.0/24
- Gateway: 23.72.0.1
- Broadcast: 23.72.0.255
- Servidor DHCP habilitado

## 🔹 Requisitos del Atacante

- Conectado al mismo dominio de broadcast
- Interfaz en modo normal (no requiere monitor mode)
- Acceso Layer 2 a la red

## 🔹 Clientes

- Configurados en modo DHCP
- Dependientes del servidor DHCP para asignación IP

---

# 🧪 Requisitos de la Topología

La topología debe incluir:

- 1 Router (Gateway 23.72.0.1)
- 1 Switch principal
- 1 Switch secundario
- 1 Máquina atacante (Linux)
- 1 Víctima
- 3 Clientes DHCP (VPCs)

Todos dentro del mismo dominio de broadcast.

---

# 🔐 Permisos

El script debe ejecutarse con privilegios elevados:

```bash
sudo python3 dhcp_starvation.py
```

---

# ⚠️ Advertencia

Este laboratorio debe ejecutarse únicamente en entornos controlados y autorizados.
No debe utilizarse en redes reales sin permiso explícito.