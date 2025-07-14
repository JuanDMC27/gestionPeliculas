document.addEventListener("DOMContentLoaded", () => {
  // Cargar películas
  fetch("/pelicula/")
    .then(res => res.json())
    .then(data => {
      const contenedor = document.getElementById("contenedorPeliculas");
      contenedor.innerHTML = "";

      data.peliculas.forEach(p => {
        const card = document.createElement("div");
        card.classList.add("movie-card");

        card.innerHTML = `
          <div class="poster" style="background-image: url('${p.foto || 'static/images/broken-image.png'}'); background-size: cover;"></div>
          <h3>${p.titulo}</h3>
          <span class="genre">${p.genero?.nombre || "Sin género"}</span>
          <p>${p.resumen.length > 120 ? p.resumen.slice(0, 120) + "..." : p.resumen}</p>
          <div class="actions">
              <button class="edit" onclick="editarPelicula('${p.id}')">Editar</button>
              <button class="delete" onclick="eliminarPelicula('${p.id}')">Eliminar</button>
              <button class="send" onclick="enviarCorreoPorId('${p.id}')">Enviar por correo</button>
          </div>
        `;
        contenedor.appendChild(card);
      });
    });

  // Abrir modal agregar
  document.querySelector(".add").addEventListener("click", () => {
    document.getElementById("modalAgregar").style.display = "block";
    cargarGeneros();
  });

  // Cerrar modal agregar
  document.getElementById("cerrarModal").addEventListener("click", () => {
    document.getElementById("modalAgregar").style.display = "none";
  });

  // Cargar géneros
  function cargarGeneros() {
    fetch("/genero/")
      .then(res => res.json())
      .then(data => {
        const select = document.getElementById("selectGenero");
        select.innerHTML = '<option value="">Selecciona un género</option>';
        data.generos.forEach(g => {
          const opt = document.createElement("option");
          opt.value = g.nombre;
          opt.textContent = g.nombre;
          select.appendChild(opt);
        });
      });
  }

  // Agregar película
  document.getElementById("formPelicula").addEventListener("submit", (e) => {
    e.preventDefault();
    const form = e.target;
    const formData = new FormData(form);
    const datos = Object.fromEntries(formData.entries());

    fetch("/pelicula/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(datos)
    })
      .then(res => res.json())
      .then(res => {
        alert(res.mensaje);
        if (res.estado) {
          form.reset();
          document.getElementById("modalAgregar").style.display = "none";
          location.reload();
        }
      });
  });

  // Editar película
  document.getElementById("formEditar").addEventListener("submit", (e) => {
    e.preventDefault();
    const datos = {
      id: document.getElementById("editId").value,
      codigo: document.getElementById("editCodigo").value,
      titulo: document.getElementById("editTitulo").value,
      protagonista: document.getElementById("editProtagonista").value,
      duracion: document.getElementById("editDuracion").value,
      resumen: document.getElementById("editResumen").value,
      foto: document.getElementById("editFoto").value,
      genero: document.getElementById("editGenero").value
    };

    fetch("/pelicula/", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(datos)
    })
      .then(res => res.json())
      .then(res => {
        alert(res.mensaje);
        if (res.estado) {
          cerrarModalEditar();
          location.reload();
        }
      });
  });

  // Confirmar eliminación
  document.getElementById("btnConfirmarEliminar").addEventListener("click", () => {
    if (!idParaEliminar) return;

    fetch("/pelicula/", {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id: idParaEliminar })
    })
      .then(res => res.json())
      .then(res => {
        alert(res.mensaje);
        if (res.estado) {
          cerrarModalEliminar();
          location.reload();
        }
      });
  });
});

// Enviar correo por ID
function enviarCorreoPorId(id) {
  const correo = prompt("Ingresa el correo del destinatario:");
  if (!correo) return;

  fetch("/pelicula/enviar-correo", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ correo, pelicula_id: id })
  })
    .then(res => res.json())
    .then(data => {
      alert(data.mensaje);
    });
}

// Variables globales
let idParaEliminar = null;

// Abrir modal editar
function editarPelicula(id) {
  fetch("/pelicula/")
    .then(res => res.json())
    .then(data => {
      const pelicula = data.peliculas.find(p => p.id === id);
      if (pelicula) {
        document.getElementById("editId").value = pelicula.id;
        document.getElementById("editCodigo").value = pelicula.codigo;
        document.getElementById("editTitulo").value = pelicula.titulo;
        document.getElementById("editProtagonista").value = pelicula.protagonista;
        document.getElementById("editDuracion").value = pelicula.duracion;
        document.getElementById("editResumen").value = pelicula.resumen;
        document.getElementById("editFoto").value = pelicula.foto || "";

        fetch("/genero/")
          .then(res => res.json())
          .then(g => {
            const select = document.getElementById("editGenero");
            select.innerHTML = "";
            g.generos.forEach(gen => {
              const opt = document.createElement("option");
              opt.value = gen.nombre;
              opt.textContent = gen.nombre;
              if (pelicula.genero?.nombre === gen.nombre) opt.selected = true;
              select.appendChild(opt);
            });
          });

        document.getElementById("modalEditar").style.display = "block";
      }
    });
}

// Cerrar modal editar
function cerrarModalEditar() {
  document.getElementById("modalEditar").style.display = "none";
}

// Abrir modal eliminar
function eliminarPelicula(id) {
  idParaEliminar = id;
  document.getElementById("modalEliminar").style.display = "block";
}

// Cerrar modal eliminar
function cerrarModalEliminar() {
  idParaEliminar = null;
  document.getElementById("modalEliminar").style.display = "none";
}
