# netconf_csr.py
from ncclient import manager
import sys

# Parámetros de conectividad de la infraestructura
ROUTER_IP = "192.168.56.102"
ROUTER_PORT = 830
USERNAME = "developer"
PASSWORD = "cisco"

def configurar_infraestructura():
    print("==================================================")
    print(" INICIANDO PROCESO DE AUTOMATIZACIÓN NETCONF     ")
    print("==================================================")
    
    # Payload XML 1: Cambio de Hostname a los apellidos del grupo
    xml_hostname = """
    <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
            <hostname>Carreno-Petit</hostname>
        </native>
    </config>
    """
    
    # Payload XML 2: Creación de Loopback 111 (Corregido)
    xml_loopback = """
    <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
            <interface>
                <Loopback>
                    <name>111</name>
                    <ip>
                        <address>
                            <primary>
                                <address>111.111.111.111</address>
                                <mask>255.255.255.255</mask>
                            </primary>
                        </address>
                    </ip>
                </Loopback>
            </interface>
        </native>
    </config>
    """
    
    try:
        print(f"[*] Conectando vía SSH al subsistema NETCONF en {ROUTER_IP}:{ROUTER_PORT}...")
        
        with manager.connect(
            host=ROUTER_IP,
            port=ROUTER_PORT,
            username=USERNAME,
            password=PASSWORD,
            hostkey_verify=False,
            device_params={'name': 'iosxe'}
        ) as sesion:
            
            print("[+] Conexión establecida con éxito. Modificando parámetros...")
            print("--------------------------------------------------")
            
            print("[*] Enviando configuración: Modificar Hostname a 'Carreno-Petit'...")
            resp_host = sesion.edit_config(target='running', config=xml_hostname)
            if resp_host.ok:
                print("[+] Hostname actualizado correctamente en la infraestructura.")
            
            print("--------------------------------------------------")
            
            print("[*] Enviando configuración: Crear interfaz Loopback 111 (111.111.111.111/32)...")
            resp_loop = sesion.edit_config(target='running', config=xml_loopback)
            if resp_loop.ok:
                print("[+] Interfaz Loopback 111 inyectada y levantada con éxito.")
                
            print("--------------------------------------------------")
            print("[INFO] Automatización completada mediante transacciones atómicas XML.")
            
    except Exception as error:
        print(f"\n[X] Error crítico en la sesión de red: {error}")
        sys.exit(1)

if __name__ == "__main__":
    configurar_infraestructura()