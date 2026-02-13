##  DHCP Starvation 
- Este Proyecto esta basado en una practica realizada con fines educativos, en el cual realizamos un ataque DHCP Starvation utilizando Script basados en Scapy en el Lenguaje Python.

Este script es una herramienta gráfica desarrollada en Python con Scapy y Tkinter que ejecuta un ataque de DHCP Starvation.

## Función del Script
Su función principal es:
Generar múltiples solicitudes DHCP Discover con direcciones MAC aleatorias para agotar el pool de direcciones IP disponibles en un servidor DHCP, impidiendo que nuevos clientes legítimos obtengan una dirección IP.

**Características clave:**

- Generación masiva de MACs aleatorias.

- Envío concurrente mediante múltiples hilos.

- Interfaz gráfica para monitoreo en tiempo real.

- Contador de paquetes enviados y MACs generadas.

- Control manual de inicio y detención del ataque.
<img width="350" height="370" alt="image" src="https://github.com/user-attachments/assets/ccde0d34-8e36-4909-b50b-3408ab850af8" />

## Video de Demostracion
**https://youtu.be/xuY-mT1N42w**

## Topologia Representada en PnetLAB
<img width="1209" height="830" alt="image" src="https://github.com/user-attachments/assets/89850eeb-ba17-48d7-82e5-cc3e3786cdce" />

##  Router

| Conexión | Interfaz Router | Dispositivo Destino | Interfaz Destino |
|----------|-----------------|---------------------|-------------------|
| LAN      | e0/0            | Switch Principal    | e0/0              |
| WAN      | e0/1            | Net                 | -                 |

**IP LAN:** 23.72.0.1  
**Gateway de la red:** 23.72.0.1  

---

## 🖧 Switch Principal

| Interfaz | Dispositivo Conectado | Interfaz Destino |
|----------|----------------------|------------------|
| e0/0     | Router               | e0/0             |
| e0/1     | Atacante             | eth0             |
| e0/2     | VPC 1                | eth0             |
| e1/0     | VPC 2                | eth0             |
| e1/1     | Víctima              | eth0             |
| e0/3     | Switch 2             | e0/0             |

---

## 🖧 Switch 2

| Interfaz | Dispositivo Conectado | Interfaz Destino |
|----------|----------------------|------------------|
| e0/0     | Switch Principal     | e0/3             |
| e0/2     | VPC 3                | eth0             |

---

## 🧨 Atacante (Linux)

| Interfaz | Conectado a         | Interfaz Destino |
|----------|---------------------|------------------|
| eth0     | Switch Principal    | e0/1             |
| eth1     | Net                 | -                |

**Configuración IP:** DHCP o estática dentro del rango 23.72.0.0/24  
**Gateway:** 23.72.0.1  

---

## 💻 Víctima

| Interfaz | Conectado a        | Interfaz Destino |
|----------|--------------------|------------------|
| eth0     | Switch Principal   | e1/1             |

**Configuración IP:** DHCP  
**Gateway:** 23.72.0.1  

---

## 🖥 Clientes DHCP (VPCs)

### VPC 1

| Interfaz | Conectado a        | Interfaz Destino |
|----------|--------------------|------------------|
| eth0     | Switch Principal   | e0/2             |

Gateway: 23.72.0.1  

---

### VPC 2

| Interfaz | Conectado a        | Interfaz Destino |
|----------|--------------------|------------------|
| eth0     | Switch Principal   | e1/0             |

Gateway: 23.72.0.1  

---

### VPC 3

| Interfaz | Conectado a  | Interfaz Destino |
|----------|--------------|------------------|
| eth0     | Switch 2     | e0/2             |

Gateway: 23.72.0.1  

## 📋 Requisitos para Utilizar la Herramienta

### 🔹 Requisitos Técnicos

- Sistema operativo Linux (Kali, Ubuntu, Debian, etc.)
- Python 3.8 o superior
- Permisos de superusuario (root)
- Acceso a una red de laboratorio controlada
- Estar dentro del mismo dominio de broadcast que el servidor DHCP objetivo

---

### 🔹 Dependencias

```bash
sudo apt update
sudo apt install python3-scapy python3-tk
```

---

### 🔹 Permisos

El script debe ejecutarse con privilegios elevados debido al envío de paquetes a nivel 2 (Layer 2):

```bash
sudo python3 dhcp_starvation.py
```

---

### 🔹 Requisitos de Red

- Servidor DHCP activo en la red
- Clientes configurados para obtener IP por DHCP
- Router configurado como gateway
- Red LAN configurada correctamente (ejemplo: 23.72.0.0/24)

---

### ⚠️ Advertencia

Esta herramienta debe utilizarse únicamente en entornos de laboratorio autorizados.  
El uso en redes reales sin autorización puede constituir delito.

---

# 🛡 Medidas de Mitigación contra DHCP Starvation

El ataque DHCP Starvation puede prevenirse mediante configuraciones adecuadas en la infraestructura de red.

---

##  1. DHCP Snooping (Recomendado)

Habilitar DHCP Snooping en switches gestionables:

- Permite marcar puertos confiables (trusted)
- Bloquea respuestas DHCP no autorizadas
- Limita solicitudes DHCP por puerto

Ejemplo en Cisco:

```
ip dhcp snooping
ip dhcp snooping vlan 1
interface e0/0
 ip dhcp snooping trust
interface range e0/1 - e0/24
 ip dhcp snooping limit rate 10
```

---

##  2. Port Security

Restringir el número de direcciones MAC permitidas por puerto:

```
interface e0/1
 switchport mode access
 switchport port-security
 switchport port-security maximum 2
 switchport port-security violation shutdown
```

Evita que un atacante genere múltiples MAC falsas desde un mismo puerto.

---

##  3. Limitar el Pool DHCP

- Configurar tiempos de lease más cortos
- Reservar direcciones IP para dispositivos críticos
- Reducir rango disponible para pruebas controladas

---

##  4. Segmentación de Red (VLANs)

Separar usuarios, servidores y dispositivos críticos en VLANs distintas para reducir el dominio de broadcast.

---

##  5. Monitoreo y Alertas

- Supervisar logs del servidor DHCP
- Detectar picos anormales de solicitudes DHCP Discover
- Implementar sistemas IDS/IPS

---

##  6. Autenticación de Red (802.1X)

Implementar autenticación basada en puerto para evitar que dispositivos no autorizados accedan a la red.

---

#  Enfoque Defensivo

El objetivo del laboratorio no es solo ejecutar el ataque, sino:

- Comprender cómo funciona
- Identificar señales de detección
- Implementar controles preventivos
- Validar configuraciones defensivas



