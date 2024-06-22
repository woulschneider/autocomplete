import os
import sqlite3

def list_sqlite_databases(directory):
    """ Lista todos os arquivos de banco de dados SQLite no diretório especificado. """
    return [file for file in os.listdir(directory) if file.endswith('.db')]

def select_table(database_path):
    """ Lista todas as tabelas em um banco de dados SQLite e permite ao usuário selecionar uma. """
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    conn.close()
    print("Tabelas disponíveis:")
    for i, table in enumerate(tables):
        print(f"{i + 1}. {table[0]}")
    index = int(input("Selecione o número da tabela: ")) - 1
    return tables[index][0]

def copy_table_to_new_db(source_db, table_name, new_db):
    """ Copia uma tabela de um banco de dados SQLite para um novo banco de dados. """
    source_conn = sqlite3.connect(source_db)
    new_conn = sqlite3.connect(new_db)
    query = f"CREATE TABLE {table_name} AS SELECT * FROM {table_name};"
    source_conn.backup(new_conn, pages=1, progress=None, name=table_name, schema=table_name)
    source_conn.close()
    new_conn.close()
    print(f"Tabela '{table_name}' copiada para '{new_db}' com sucesso!")

def main():
    directory = input("Digite o caminho do diretório onde estão os bancos de dados: ")
    db_files = list_sqlite_databases(directory)
    if not db_files:
        print("Nenhum arquivo de banco de dados encontrado.")
        return
    print("Arquivos de banco de dados encontrados:")
    for i, db_file in enumerate(db_files):
        print(f"{i + 1}. {db_file}")
    db_index = int(input("Selecione o número do banco de dados: ")) - 1
    selected_db = os.path.join(directory, db_files[db_index])
    selected_table = select_table(selected_db)
    new_db_path = input("Digite o nome para o novo banco de dados (ex: novo_banco.db): ")
    copy_table_to_new_db(selected_db, selected_table, new_db_path)

if __name__ == "__main__":
    main()
