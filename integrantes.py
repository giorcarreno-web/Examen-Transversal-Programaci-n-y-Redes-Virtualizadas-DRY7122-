# integrantes.py
def mostrar_integrantes():
    integrantes = [
        "Giordano Carreño Barrera",
        "Benjamin Petit Barrera"
    ]
    
    print("=========================================")
    print("  Integrantes del Examen Transversal     ")
    print("=========================================")
    for alumno in integrantes:
        print(f"- {alumno}")
    print("=========================================")

if __name__ == "__main__":
    mostrar_integrantes()