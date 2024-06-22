document.getElementById('addButton').addEventListener('click', function() {
    const input = document.getElementById('produto');
    const value = input.value;
    const list = document.getElementById('selectedItems');

    if (value) {
        const newItem = document.createElement('li');
        newItem.classList.add('list-group-item');
        newItem.textContent = value;
        list.appendChild(newItem);

        input.value = ''; // Limpa o campo após adicionar
    }
});
