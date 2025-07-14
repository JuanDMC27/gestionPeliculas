document.addEventListener("DOMContentLoaded", () => {
    const loader = document.getElementById("loader");

  // Carrusel de películas recientes
    fetch("/pelicula/recientes")
    .then(res => res.json())
    .then(data => {
        const contenedor = document.getElementById("carouselPeliculas");
        const duplicadas = [...data.peliculas, ...data.peliculas];

        duplicadas.forEach(p => {
            const card = document.createElement("div");
            card.classList.add("movie-card");
            card.innerHTML = `
            <div class="poster" style="background-image: url('${p.foto || "static/images/broken-image.png"}')"></div>
            `;
            contenedor.appendChild(card);
        });

        loader.style.display = "none";
    });

  // Cargar géneros
    fetch("/genero/")
    .then(res => res.json())
    .then(data => {
        const contenedorGen = document.getElementById("contenedorGeneros");
        contenedorGen.innerHTML = "";
        data.generos.forEach(g => {
            const chip = document.createElement("div");
            chip.classList.add("genre-chip");
            chip.textContent = g.nombre;
            contenedorGen.appendChild(chip);
        });
    });
});
