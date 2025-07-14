document.addEventListener("DOMContentLoaded", () => {
    const modalAgregar = document.getElementById("modalGenero");
    const modalEliminar = document.getElementById("modalEliminarGenero");
    const modalEditar = document.getElementById("modalEditarGenero");

    const formAgregar = document.getElementById("formGenero");
    const formEditar = document.getElementById("formEditarGenero");

    const nombreInput = document.getElementById("nombreGenero");
    const contenedor = document.getElementById("contenedorGeneros");

    const editNombreInput = document.getElementById("editNombreGenero");
    const editIdInput = document.getElementById("editGeneroId");

    let idGeneroAEliminar = null;
    

  // Abrir modal de agregar
    document.getElementById("btnAgregarGenero").addEventListener("click", () => {
        modalAgregar.style.display = "block";
        nombreInput.value = "";
    });

  // Cerrar modal de agregar
    window.cerrarModalGenero = () => {
        modalAgregar.style.display = "none";
    };

  // Cargar géneros desde el servidor
    function cargarGeneros() {
        fetch("/genero/")
        .then(res => res.json())
        .then(data => {
            contenedor.innerHTML = "";
            data.generos.forEach(g => {
            const div = document.createElement("div");
            div.classList.add("genero-item");
            div.innerHTML = `
                <span>${g.nombre}</span>
                <div style="display: flex; gap: 5px;">
                <button class="editar" onclick="editarGenero('${g._id}', '${g.nombre}')">Editar</button>
                <button class="eliminar" onclick="eliminarGenero('${g._id}')">Eliminar</button>
                </div>
            `;
            contenedor.appendChild(div);
            });
        });
    }

  // Enviar nuevo género
    formAgregar.addEventListener("submit", e => {
        e.preventDefault();
        const nombre = nombreInput.value.trim();
        if (!nombre) return;

    fetch("/genero/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nombre })
    })
        .then(res => res.json())
        .then(res => {
            alert(res.mensaje);
            if (res.estado) {
            cerrarModalGenero();
            cargarGeneros();
            }
        });
    });

  // 🔹 Eliminar género
    window.eliminarGenero = (id) => {
        idGeneroAEliminar = id;
        modalEliminar.style.display = "block";
    };

    window.cerrarModalEliminarGenero = () => {
        modalEliminar.style.display = "none";
        idGeneroAEliminar = null;
    };

    document.getElementById("btnConfirmarEliminarGenero").addEventListener("click", () => {
        if (!idGeneroAEliminar) return;

    fetch("/genero/", {
        method: "DELETE",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id: idGeneroAEliminar })
    })
        .then(res => res.json())
        .then(res => {
            alert(res.mensaje);
            if (res.estado) {
            cerrarModalEliminarGenero();
            cargarGeneros();
            }
        });
    });

  // 🔹 Abrir modal de edición
    window.editarGenero = (id, nombre) => {
        editIdInput.value = id;
        editNombreInput.value = nombre;
        modalEditar.style.display = "block";
    };

  // 🔹 Cerrar modal de edición
    window.cerrarModalEditarGenero = () => {
        modalEditar.style.display = "none";
    };

  // 🔹 Enviar edición
    formEditar.addEventListener("submit", (e) => {
        e.preventDefault();

    const id = editIdInput.value;
    const nombre = editNombreInput.value.trim();

    if (!id || !nombre) return;

    fetch("/genero/", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id, nombre })
    })
        .then(res => res.json())
        .then(res => {
            alert(res.mensaje);
            if (res.estado) {
            cerrarModalEditarGenero();
            cargarGeneros();
            }
        });
    });

  //Inicializar
    cargarGeneros();
});
