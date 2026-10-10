"""
Ejercicio Nro 4: Gestión de Inventario de Instrumentos Musicales
Una fábrica de instrumentos musicales posee diferentes sucursales. Cada sucursal tiene un
nombre y una lista de instrumentos disponibles para la venta.
De cada instrumento se conoce:
 ID: identificador alfanumérico.
 Precio: precio del instrumento.
 Tipo: puede ser Percusión, Viento o Cuerda.
Implementar una solución que permita gestionar el inventario.

Requisitos
1. listarInstrumentos()
Mostrar en la consola todos los instrumentos disponibles, indicando sucursal, ID, precio y
tipo.
2. instrumentosPorTipo(tipo)
Recibir como parámetro un tipo de instrumento y devolver una lista con los instrumentos
que pertenecen a ese tipo.
3. borrarInstrumento(id)
Recibir un ID y eliminar el instrumento correspondiente de la sucursal en la que se
encuentre.
4. porcInstrumentosPorTipo(sucursal)
Recibir el nombre de una sucursal y mostrar o retornar el porcentaje de instrumentos
correspondientes a cada tipo:
o Percusión
o Viento
o Cuerda
"""

TIPOS = ["Percusión", "Viento", "Cuerda"]

sucursales = [
    {
        "nombre": "Centro",
        "instrumentos": [
            {"id": "P001", "precio": 85000, "tipo": "Percusión"},
            {"id": "V001", "precio": 42000, "tipo": "Viento"},
            {"id": "C001", "precio": 120000, "tipo": "Cuerda"},
            {"id": "C002", "precio": 95000, "tipo": "Cuerda"},
        ],
    },
    {
        "nombre": "Norte",
        "instrumentos": [
            {"id": "P002", "precio": 60000, "tipo": "Percusión"},
            {"id": "V002", "precio": 38000, "tipo": "Viento"},
            {"id": "V003", "precio": 51000, "tipo": "Viento"},
        ],
    },
]


def listarInstrumentos():
    for sucursal in sucursales:
        for instrumento in sucursal["instrumentos"]:
            print(f"Sucursal: {sucursal['nombre']} - ID: {instrumento['id']} - "
                  f"Precio: ${instrumento['precio']} - Tipo: {instrumento['tipo']}")


def instrumentosPorTipo(tipo):
    lista = []
    for sucursal in sucursales:
        for instrumento in sucursal["instrumentos"]:
            if instrumento["tipo"] == tipo:
                lista.append(instrumento)
    return lista


def borrarInstrumento(id):
    for sucursal in sucursales:
        for instrumento in sucursal["instrumentos"]:
            if instrumento["id"] == id:
                sucursal["instrumentos"].remove(instrumento)
                return True
    return False


def porcInstrumentosPorTipo(nombreSucursal):
    for sucursal in sucursales:
        if sucursal["nombre"] == nombreSucursal:
            instrumentos = sucursal["instrumentos"]
            porcentajes = {}
            for tipo in TIPOS:
                cantidad = 0
                for instrumento in instrumentos:
                    if instrumento["tipo"] == tipo:
                        cantidad += 1
                if len(instrumentos) > 0:
                    porcentajes[tipo] = cantidad * 100 / len(instrumentos)
                else:
                    porcentajes[tipo] = 0
            return porcentajes
    return None


def main():
    print("Listado de instrumentos:")
    listarInstrumentos()

    print("\nInstrumentos de Viento:")
    for instrumento in instrumentosPorTipo("Viento"):
        print(instrumento)

    print("\nBorrando el instrumento C002...")
    if borrarInstrumento("C002"):
        print("Instrumento borrado")
    else:
        print("No se encontró el instrumento")
    listarInstrumentos()

    print("\nPorcentaje de instrumentos por tipo en la sucursal Centro:")
    porcentajes = porcInstrumentosPorTipo("Centro")
    if porcentajes is None:
        print("La sucursal no existe")
    else:
        for tipo, porcentaje in porcentajes.items():
            print(f"{tipo}: {porcentaje:.2f}%")


main()
