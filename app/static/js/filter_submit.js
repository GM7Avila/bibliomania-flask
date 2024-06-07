document.addEventListener("DOMContentLoaded", function() {
    // Selecione o elemento select
    const filterSelect = document.getElementById('filter-select');

    // Adicione um ouvinte de eventos para detectar a mudança no valor do select
    filterSelect.addEventListener('change', function() {
        // Submeta automaticamente o formulário quando uma opção for selecionada
        document.getElementById('search-form').submit();
    });
});