import logging
from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# Configurando o logging
logging.basicConfig(level=logging.DEBUG)

# Configurações das fontes de dados
#DATA_SOURCES = {
#    'inputId': {
#        'db': 'medicamentos.db',
#        'table': 'medicamentos2',
#        'column': 'PRODUTO'
#    }
#}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/autocomplete', methods=['GET'])
def autocomplete():
    query = request.args.get('q')
    db = request.args.get('db')
    table = request.args.get('table')
    column = request.args.get('column')
    
    # Implementação da lógica para buscar dados do banco de dados
    # Supondo que você esteja usando SQLite
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    offset = request.args.get('offset', default=0, type=int)
    sql_query = f"SELECT DISTINCT {column} FROM {table} WHERE {column} LIKE ? LIMIT 20 OFFSET {offset}"
    cursor.execute(sql_query, (f'%{query}%',))
    results = cursor.fetchall()
    cursor.close()
    connection.close()

    return jsonify([row[0] for row in results])


if __name__ == '__main__':
    app.run(debug=True)
