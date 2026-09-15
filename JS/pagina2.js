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

// ===== Validaciones del formulario de inscripción =====

const formulario = document.getElementById("formulario-inscripcion");
const campoFechaNacimiento = document.getElementById("fecha_nacimiento");

// Valida la fecha cada vez que el usuario la cambia
campoFechaNacimiento.addEventListener("change", function () {
    validarFechaNacimiento(campoFechaNacimiento);
});

// Antes de enviar se vuelve a validar y, si hay errores, se cancela el envío
formulario.addEventListener("submit", function (evento) {
    let formularioValido = true;

    if (!validarFechaNacimiento(campoFechaNacimiento)) {
        formularioValido = false;
    }

    if (!formularioValido) {
        evento.preventDefault();
    }
});
