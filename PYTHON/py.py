"""
Ejercicio Nro 1: Validación de entrada y búsqueda en una Lista.
Implementar un programa que valide la entrada de un número entero y verifique su presencia en
una lista.
Requisitos:
1. Solicitar al usuario que ingrese un número entero del 0 al 9.
2. Mientras el número ingresado no esté en el rango especificado, repetir la solicitud.
3. Verificar si el número se encuentra en una lista predefinida de números.
4. Notificar al usuario si el número está o no en la lista.
Concepto útil: Utilizar la sintaxis [valor] in [lista] para comprobar la presencia de un valor en una
lista
"""


def ingresoNum():
    while True:
        try:
            num = int (input ("Ingrese un numero entero entre el 0 y el 9:  "))
            if num >= 0 and num <= 9:
                print("numero en rango aceptado")
                return num
            else:
                print("numero fuera de rango aceptado")
        except ValueError:
                print("No ingresaste un numero")


def vali(num, lista):
    return num in lista



def main():
    lista= [1,5,7,4,9]
    numeros=ingresoNum()
    validados=vali(numeros, lista)
    if validados:
        print("El numero que ingreso esta en la lista")
    else:
        print("El numero que ingreso no esta en la lista")

    
main() 



