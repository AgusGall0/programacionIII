// ===== Funciones de validación =====

// Muestra un mensaje de error en el span que está debajo del campo.
// Si el mensaje está vacío, borra el error.
function mostrarError(campo, mensaje) {
    const elementoError = document.getElementById("error_" + campo.id);
    elementoError.textContent = mensaje;
}

// Ejercicio 1: verifica que la fecha de nacimiento no sea posterior a hoy.
// Devuelve true si la fecha es válida y false si no lo es.
function validarFechaNacimiento(campoFecha) {
    // Si no se cargó ninguna fecha no hay nada que comparar
    if (campoFecha.value === "") {
        mostrarError(campoFecha, "");
        return true;
    }

    // Se agrega la hora para que la fecha se tome en hora local
    const fechaIngresada = new Date(campoFecha.value + "T00:00:00");
    const fechaActual = new Date();

    if (fechaIngresada > fechaActual) {
        mostrarError(campoFecha, "La fecha de nacimiento no puede ser posterior a la fecha actual");
        return false;
    } else {
        mostrarError(campoFecha, "");
        return true;
    }
}

// Ejercicio 2: verifica que el DNI tenga exactamente 8 dígitos.
// Devuelve true si el DNI es válido y false si no lo es.
function validarDni(campoDni) {
    const dni = campoDni.value;
    let esValido = true;

    // Tiene que tener exactamente 8 caracteres
    if (dni.length !== 8) {
        esValido = false;
    }

    // Cada caracter tiene que ser un número del 0 al 9
    for (let i = 0; i < dni.length; i++) {
        if (dni[i] < "0" || dni[i] > "9") {
            esValido = false;
        }
    }

    if (esValido) {
        mostrarError(campoDni, "");
    } else {
        mostrarError(campoDni, "El DNI debe contener 8 dígitos");
    }
    return esValido;
}

// ===== Validaciones del formulario de inscripción =====

const formulario = document.getElementById("formulario-inscripcion");
const campoFechaNacimiento = document.getElementById("fecha_nacimiento");
const campoDni = document.getElementById("dni");

// Valida la fecha cada vez que el usuario la cambia
campoFechaNacimiento.addEventListener("change", function () {
    validarFechaNacimiento(campoFechaNacimiento);
});

// Valida el DNI cada vez que el usuario lo cambia
campoDni.addEventListener("change", function () {
    validarDni(campoDni);
});

// Antes de enviar se vuelve a validar y, si hay errores, se cancela el envío
formulario.addEventListener("submit", function (evento) {
    let formularioValido = true;

    if (!validarFechaNacimiento(campoFechaNacimiento)) {
        formularioValido = false;
    }

    if (!validarDni(campoDni)) {
        formularioValido = false;
    }

    if (!formularioValido) {
        evento.preventDefault();
    }
});
