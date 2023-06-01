const hamburguer = document.querySelector(".hamburguer");
const navbarNav = document.querySelector(".navbar-nav");

hamburguer.addEventListener("click", () => {
  hamburguer.classList.toggle("active");
  navbarNav.classList.toggle("active");
})

document.querySelectorAll(".nav-link").forEach(
  n => n.addEventListener("click", () => {
    hamburguer.classList.remove("active");
    navbarNav.classList.remove("active");
  }))
