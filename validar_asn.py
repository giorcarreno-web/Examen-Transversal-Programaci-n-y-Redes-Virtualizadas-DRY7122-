# validar_asn.py
def validar_bgp_asn():
    print("=========================================")
    print("    Validador de ASN BGP - DRY7122       ")
    print("=========================================")
    
    while True:
        entrada = input("Ingrese el número de AS de BGP (o 's' para salir): ").strip()
        
        if entrada.lower() == 's':
            print("Saliendo del programa...")
            break
            
        if not entrada.isdigit():
            print("Por favor, ingrese un número entero válido.")
            print("-----------------------------------------")
            continue
            
        asn = int(entrada)
        
        # Validación de rangos de 16 bits y 32 bits según RFC 6996
        es_privado_16 = (64512 <= asn <= 65534)
        es_privado_32 = (4200000000 <= asn <= 4294967294)
        
        # Límites máximos permitidos para ASN
        if asn < 1 or asn > 4294967295 or asn == 65535:
            print(f"El ASN {asn} es reservado, inválido o está fuera de rango.")
        elif es_privado_16 or es_privado_32:
            print(f"Resultado: El ASN {asn} es PRIVADO.")
        else:
            print(f"Resultado: El ASN {asn} es PÚBLICO.")
        print("-----------------------------------------")

if __name__ == "__main__":
    validar_bgp_asn()