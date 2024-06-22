// Definição das fontes de dados para cada campo de autocompletar
const DATA_SOURCES = {
    'produto': {
        db: 'app.db',
        table: 'medicamentos2',
        column: 'PRODUTO'
    },
    'nome_do_campo2': {
        db: 'outro_banco.db',
        table: 'outra_tabela',
        column: 'outra_coluna'
    }
    // Adicione mais configurações conforme necessário
};

// Função para configurar o autocompletar nos campos especificados
document.addEventListener('DOMContentLoaded', function() {
    Object.keys(DATA_SOURCES).forEach(inputId => {
        const inputElement = document.getElementById(inputId);
        if (inputElement) {
            setupAutocomplete(inputElement, DATA_SOURCES[inputId]);
        } else {
            console.error(`Elemento não encontrado para o ID: ${inputId}`);
        }
    });
});

// Configura a funcionalidade de autocompletar para um campo de entrada específico
function setupAutocomplete(inputElement, dataSource) {
    inputElement.addEventListener('input', function() {
        const query = this.value;
        if (query.length > 1) { // Iniciar busca após dois caracteres
            fetchAutocompleteSuggestions(query, dataSource, inputElement);
        }
    });
}

// Busca sugestões de autocompletar do servidor
function fetchAutocompleteSuggestions(query, dataSource, inputElement) {
    const params = new URLSearchParams({
        q: query,
        db: dataSource.db,
        table: dataSource.table,
        column: dataSource.column
    }).toString();

    fetch(`/api/autocomplete?${params}`)
        .then(response => response.json())
        .then(data => {
            updateSuggestions(inputElement, data);
        })
        .catch(error => console.error('Erro ao buscar sugestões:', error));
}

// Atualiza o elemento <datalist> associado ao campo de entrada com novas sugestões
function updateSuggestions(inputElement, suggestions) {
    let dataListId = inputElement.getAttribute('list');
    if (!dataListId) {
        dataListId = `${inputElement.id}-datalist`;
        inputElement.setAttribute('list', dataListId);
        const dataList = document.createElement('datalist');
        dataList.id = dataListId;
        document.body.appendChild(dataList);
    }

    const dataList = document.getElementById(dataListId);
    dataList.innerHTML = ''; // Limpa sugestões anteriores

    suggestions.forEach(suggestion => {
        const option = document.createElement('option');
        option.value = suggestion;
        dataList.appendChild(option);
    });
}
