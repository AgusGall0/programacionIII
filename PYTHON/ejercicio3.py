"""
Ejercicio Nro 3: Registro de Información en un Diccionario.
Requisitos:
1. Solicitar al usuario que ingrese los siguientes datos: nombre, edad, dirección y teléfono.
2. Almacenar los datos en un diccionario llamado usuario_info.
3. Permitir el ingreso de información para varios usuarios.
4. Mostrar la información ingresada para cada usuario en formato clave-valor.

"""


def ingreso():
    usuario_info = {}
    usuario_info["nombre"] = input("Ingrese el nombre: ")
    usuario_info["edad"] = int(input("Ingrese la edad: "))
    usuario_info["dirección"] = input("Ingrese la dirección: ")
    usuario_info["teléfono"] = input("Ingrese el teléfono: ")
    return usuario_info

def main():

    usuarios=[]
    while True:
        continuar = input("¿Desea ingresar información de un usuario? (s/n): ")
        if continuar.lower() == 'n':
            break

        else:
            usuario_info = ingreso()
            usuarios.append(usuario_info)

    print("\nInformación de los usuarios ingresados:")
    for i, usuario in enumerate(usuarios, start=1):
        print(f"\nUsuario {i}:")
        for clave, valor in usuario.items():
            print(f"{clave}: {valor}")
            
main()


