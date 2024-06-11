// Seletor de todos os links de navegação
var navLinks = document.querySelectorAll('.nav-link');

// Adiciona um ouvinte de evento de clique a cada link de navegação
navLinks.forEach(function(link) {
    link.addEventListener('click', function() {
        // Remove a classe .show de todas as páginas
        document.querySelectorAll('.page').forEach(function(page) {
            page.classList.remove('show');
        });

        // Adiciona a classe .show à página correspondente ao link clicado
        var targetPageId = this.getAttribute('data-target');
        document.getElementById(targetPageId).classList.add('show');
    });
});