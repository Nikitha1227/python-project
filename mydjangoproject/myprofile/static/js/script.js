
// MOBILE NAVIGATION

const menuBtn = document.getElementById("menuBtn");

const navbar = document.getElementById("navbar");

menuBtn.addEventListener("click", function () {

    navbar.classList.toggle("active");

    const isOpen = navbar.classList.contains("active");

    menuBtn.setAttribute("aria-expanded", isOpen);

    menuBtn.innerHTML = isOpen ? "✕" : "☰";

});


// CLOSE MENU AFTER CLICKING A LINK

const navLinks = document.querySelectorAll(".navbar a");

navLinks.forEach(function (link) {

    link.addEventListener("click", function () {

        navbar.classList.remove("active");

        menuBtn.setAttribute("aria-expanded", "false");

        menuBtn.innerHTML = "☰";

    });

});


// AUTOMATIC FOOTER YEAR

document.getElementById("year").textContent =
    new Date().getFullYear();


// CONSOLE MESSAGE

console.log("Welcome to Govind Raj's Portfolio!");
