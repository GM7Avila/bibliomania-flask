document.getElementById("button1").addEventListener("click", function() {
    // Chama a função do controlador para atualizar o conteúdo
    ContentController.updateContent("Conteúdo atualizado pelo Botão 1");
});

document.getElementById("button2").addEventListener("click", function() {
    // Chama a função do controlador para atualizar o conteúdo
    ContentController.updateContent("Conteúdo atualizado pelo Botão 2");
});