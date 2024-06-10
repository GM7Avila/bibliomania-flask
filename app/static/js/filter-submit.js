// submit automaticamente o formulário quando uma opção for selecionada atraves do listening filter-reservation-list-status
document.addEventListener("DOMContentLoaded", function() {
    const filterSelect = document.getElementById('filter-select');
    filterSelect.addEventListener('change', function() {
        document.getElementById('search-form').submit();
    });
});