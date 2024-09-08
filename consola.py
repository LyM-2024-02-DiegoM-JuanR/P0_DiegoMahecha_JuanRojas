from parser import initializeParser
archivo = ""

def menu():
    print("\n--- Menú ---")
    print("1. Ingresar nombre de archivo")
    print("2. Correr parser sobre archivo seleccionado")
    print("3. Salir")


def main():
    while True:
        menu()
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            archivo = input("Ingrese el nombre del archivo: ")
            
        elif opcion == '2':
            initializeParser(archivo)
            
        elif opcion == '3':
            break
            
        else:
            print("Opción no válida, por favor seleccione una opción válida.")

if __name__ == "__main__":
    
    main()
