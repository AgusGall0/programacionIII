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

    // También se validan los campos de los participantes generados
    const dnisParticipantes = document.getElementsByClassName("dni-participante");
    for (let i = 0; i < dnisParticipantes.length; i++) {
        if (!validarDni(dnisParticipantes[i])) {
            formularioValido = false;
        }
    }

    const fechasParticipantes = document.getElementsByClassName("fecha-participante");
    for (let i = 0; i < fechasParticipantes.length; i++) {
        if (!validarFechaNacimiento(fechasParticipantes[i])) {
            formularioValido = false;
        }
    }

    if (!formularioValido) {
        evento.preventDefault();
    }
});

// ===== Ejercicio 5: generación dinámica de participantes =====

// Crea una columna con la etiqueta, el campo y el span para el mensaje de error
function crearCampo(textoEtiqueta, campo, claseColumna) {
    const columna = document.createElement("div");
    columna.className = claseColumna;

    const parrafo = document.createElement("p");
    parrafo.className = "campo";

    const etiqueta = document.createElement("label");
    etiqueta.htmlFor = campo.id;
    etiqueta.textContent = textoEtiqueta;

    const error = document.createElement("span");
    error.id = "error_" + campo.id;
    error.className = "mensaje-error";

    parrafo.appendChild(etiqueta);
    parrafo.appendChild(campo);
    parrafo.appendChild(error);
    columna.appendChild(parrafo);
    return columna;
}

// Agrega una opción (option) a una lista desplegable (select)
function agregarOpcion(lista, valor, texto) {
    const opcion = document.createElement("option");
    opcion.value = valor;
    opcion.textContent = texto;
    lista.appendChild(opcion);
}

// Crea el bloque completo de un participante con todos sus campos
function crearBloqueParticipante(numero) {
    const bloque = document.createElement("fieldset");

    const titulo = document.createElement("legend");
    titulo.textContent = "Participante " + numero;
    bloque.appendChild(titulo);

    const fila = document.createElement("div");
    fila.className = "row";

    // Apellido y nombre
    const campoNombre = document.createElement("input");
    campoNombre.type = "text";
    campoNombre.id = "apellido_nombre_participante_" + numero;
    campoNombre.name = "apellido_nombre_participante_" + numero;
    campoNombre.maxLength = 100;
    campoNombre.required = true;
    fila.appendChild(crearCampo("Apellido y nombre:", campoNombre, "col-md-8"));

    // DNI, con la validación del ejercicio 2
    const campoDniParticipante = document.createElement("input");
    campoDniParticipante.type = "number";
    campoDniParticipante.id = "dni_participante_" + numero;
    campoDniParticipante.name = "dni_participante_" + numero;
    campoDniParticipante.className = "dni-participante";
    campoDniParticipante.required = true;
    campoDniParticipante.addEventListener("change", function () {
        validarDni(campoDniParticipante);
    });
    fila.appendChild(crearCampo("DNI:", campoDniParticipante, "col-md-4"));

    // Fecha de nacimiento, con la validación del ejercicio 1
    const campoFecha = document.createElement("input");
    campoFecha.type = "date";
    campoFecha.id = "fecha_nacimiento_participante_" + numero;
    campoFecha.name = "fecha_nacimiento_participante_" + numero;
    campoFecha.className = "fecha-participante";
    campoFecha.addEventListener("change", function () {
        validarFechaNacimiento(campoFecha);
    });
    fila.appendChild(crearCampo("Fecha de nacimiento:", campoFecha, "col-md-4"));

    // Sexo
    const campoSexo = document.createElement("select");
    campoSexo.id = "sexo_participante_" + numero;
    campoSexo.name = "sexo_participante_" + numero;
    agregarOpcion(campoSexo, "femenino", "Femenino");
    agregarOpcion(campoSexo, "masculino", "Masculino");
    agregarOpcion(campoSexo, "no_binario", "No binario");
    fila.appendChild(crearCampo("Sexo:", campoSexo, "col-md-4"));

    // Nivel
    const campoNivel = document.createElement("select");
    campoNivel.id = "nivel_participante_" + numero;
    campoNivel.name = "nivel_participante_" + numero;
    agregarOpcion(campoNivel, "inicial", "Inicial");
    agregarOpcion(campoNivel, "intermedio", "Intermedio");
    agregarOpcion(campoNivel, "avanzado", "Avanzado");
    fila.appendChild(crearCampo("Nivel:", campoNivel, "col-md-4"));

    bloque.appendChild(fila);
    return bloque;
}

const campoCantidad = document.getElementById("cantidadParticipantes");
const botonGenerar = document.getElementById("botonGenerar");
const contenedorParticipantes = document.getElementById("contenedorParticipantes");

// Al presionar el botón se generan los bloques de participantes
botonGenerar.addEventListener("click", function () {
    const cantidad = Number(campoCantidad.value);

    if (cantidad < 1 || cantidad > 10) {
        alert("Ingrese una cantidad de participantes entre 1 y 10");
    } else {
        // Se borran los bloques que se hayan generado antes
        while (contenedorParticipantes.firstChild) {
            contenedorParticipantes.removeChild(contenedorParticipantes.firstChild);
        }

        // Se crea un bloque por cada participante
        for (let i = 1; i <= cantidad; i++) {
            contenedorParticipantes.appendChild(crearBloqueParticipante(i));
        }
    }
});
