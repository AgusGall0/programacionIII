// ===== Ejercicio 3: gestión de actividades =====

// 3.1 Función constructora: crea un objeto con los datos de una actividad
function Actividad(nombre, lugar, dia, horario, cupo, estado) {
    this.nombre = nombre;
    this.lugar = lugar;
    this.dia = dia;
    this.horario = horario;
    this.cupo = cupo;
    this.estado = estado;
}

// 3.2 Clase que guarda y administra la lista de actividades
class SistemaDeportes {
    constructor() {
        // Array interno donde se guardan las actividades
        this.actividades = [];
    }

    // Agrega una actividad al final del array
    agregarActividad(actividad) {
        this.actividades.push(actividad);
    }

    // Devuelve el array con todas las actividades
    listarActividades() {
        return this.actividades;
    }
}

// 3.3 Se crea el sistema y se cargan las cuatro actividades
const sistema = new SistemaDeportes();

sistema.agregarActividad(new Actividad("Fútbol", "Cancha Universitaria", "Lunes", "18:00 - 20:00", 20, "Disponible"));
sistema.agregarActividad(new Actividad("Básquet", "Cancha Techada", "Martes", "17:00 - 19:00", 15, "Disponible"));
sistema.agregarActividad(new Actividad("Vóley", "Cancha Techada", "Miércoles", "18:00 - 20:00", 12, "Completo"));
sistema.agregarActividad(new Actividad("Atletismo", "Pista de Atletismo", "Jueves", "16:00 - 18:00", 25, "Disponible"));
