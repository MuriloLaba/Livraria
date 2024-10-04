import sqlite3
import os
import csv
from pathlib import Path
from datetime import datetime

BASE_DIR = Path("Sistema De Livraria")
BACKUP_DIR = BASE_DIR / "backups"
DATA_DIR = BASE_DIR / "data"
EXPORT_DIR = BASE_DIR / "exports"
DB_FILE = DATA_DIR / "livraria.db"

def inicializar_diretorios():
    for dir_path in [BASE_DIR, BACKUP_DIR, DATA_DIR, EXPORT_DIR]:
        dir_path.mkdir(parents=True, exist_ok=True)

def conectar_banco():
    return sqlite3.connect(DB_FILE)

def inicializar_banco():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT,
            autor TEXT,
            ano_publicacao INTEGER,
            preco REAL
        )
    ''')
    conn.commit()
    conn.close()

def adicionar_livro(titulo, autor, ano_publicacao, preco):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO livros (titulo, autor, ano_publicacao, preco) VALUES (?, ?, ?, ?)', 
                   (titulo, autor, ano_publicacao, preco))
    conn.commit()
    conn.close()
    fazer_backup()

def exibir_livros():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM livros')
    livros = cursor.fetchall()
    conn.close()
    return livros

def atualizar_preco_livro(livro_id, novo_preco):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('UPDATE livros SET preco = ? WHERE id = ?', (novo_preco, livro_id))
    conn.commit()
    conn.close()
    fazer_backup()

def remover_livro(livro_id):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM livros WHERE id = ?', (livro_id,))
    conn.commit()
    conn.close()
    fazer_backup()

def buscar_livros_por_autor(autor):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM livros WHERE autor LIKE ?', ('%' + autor + '%',))
    livros = cursor.fetchall()
    conn.close()
    return livros

def exportar_para_csv():
    livros = exibir_livros()
    with open(EXPORT_DIR / "livros_exportados.csv", mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Título', 'Autor', 'Ano de Publicação', 'Preço'])
        writer.writerows(livros)

def importar_de_csv(caminho_csv):
    with open(caminho_csv, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader) 
        conn = conectar_banco()
        cursor = conn.cursor()
        for row in reader:
            cursor.execute('INSERT INTO livros (titulo, autor, ano_publicacao, preco) VALUES (?, ?, ?, ?)', 
                           (row[1], row[2], int(row[3]), float(row[4])))
        conn.commit()
        conn.close()
    fazer_backup()

def fazer_backup():
    data_atual = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    backup_file = BACKUP_DIR / f"backup_livraria_{data_atual}.db"
    if DB_FILE.exists():
        with open(DB_FILE, 'rb') as db_original:
            with open(backup_file, 'wb') as db_backup:
                db_backup.write(db_original.read())
    limpar_backups_antigos()

def limpar_backups_antigos():
    backups = sorted(BACKUP_DIR.glob("backup_livraria_*.db"), key=os.path.getmtime, reverse=True)
    for backup in backups[5:]:  
        backup.unlink()

def limpar_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def listar_arquivos_csv():
    arquivos_csv = [f for f in EXPORT_DIR.glob("*.csv")]
    return arquivos_csv

def menu():
    while True:
        limpar_console() 
        
        print("\nSistema de Gerenciamento de Livraria\n")
        print("1. Adicionar novo livro")
        print("2. Exibir todos os livros")
        print("3. Atualizar preço de um livro")
        print("4. Remover um livro")
        print("5. Buscar livros por autor")
        print("6. Exportar dados para CSV")
        print("7. Importar dados de CSV")
        print("8. Fazer backup do banco de dados")
        print("9. Sair")

        opcao = input("\nEscolha uma opção: ")

        limpar_console()  

        if opcao == "1":
            print("Adicionar novo livro\n")
            titulo = input("Título do livro: ")
            autor = input("Autor do livro: ")
            ano_publicacao = int(input("Ano de publicação: "))
            preco = float(input("Preço: "))
            adicionar_livro(titulo, autor, ano_publicacao, preco)
            print("\nLivro adicionado com sucesso.")
        
        elif opcao == "2":
            print("Exibir todos os livros\n")
            livros = exibir_livros()
            if livros:
                for livro in livros:
                    print(livro)
            else:
                print("Nenhum livro encontrado.")
        
        elif opcao == "3":
            print("Atualizar preço de um livro\n")
            livros = exibir_livros()
            if livros:
                for livro in livros:
                    print(livro)
            else:
                print("Nenhum livro encontrado.")
                input("\nPressione Enter para voltar ao menu...")
                continue  

            livro_id = int(input("\nDigite o ID do livro que deseja atualizar: "))
            novo_preco = float(input("Novo preço: "))
            atualizar_preco_livro(livro_id, novo_preco)
            print("\nPreço atualizado com sucesso.")
        
        elif opcao == "4":
            print("Remover um livro\n")
            livros = exibir_livros()
            if livros:
                for livro in livros:
                    print(livro)
            else:
                print("Nenhum livro encontrado.")
                input("\nPressione Enter para voltar ao menu...")
                continue  

            livro_id = int(input("\nDigite o ID do livro que deseja remover: "))
            remover_livro(livro_id)
            print("\nLivro removido com sucesso.")
        
        elif opcao == "5":
            print("Buscar livros por autor\n")
            livros = exibir_livros()
            if livros:
                for livro in livros:
                    print(livro)
            else:
                print("Nenhum livro encontrado.")
                input("\nPressione Enter para voltar ao menu...")
                continue

            autor = input("\nDigite o nome do autor: ")
            livros_autor = buscar_livros_por_autor(autor)
            if livros_autor:
                for livro in livros_autor:
                    print(livro)
            else:
                print(f"Nenhum livro encontrado para o autor {autor}.")
        
        elif opcao == "6":
            print("Exportar dados para CSV\n")
            exportar_para_csv()
            print("Dados exportados com sucesso para CSV.")
        
        elif opcao == "7":
            print("Importar dados de CSV\n")
            arquivos_csv = listar_arquivos_csv()
            
            if arquivos_csv:
                print("Arquivos disponíveis para importação:")
                for idx, arquivo in enumerate(arquivos_csv, start=1):
                    print(f"{idx}. {arquivo.name}")
                
                escolha = int(input("\nEscolha o número do arquivo que deseja importar: ")) - 1
                if 0 <= escolha < len(arquivos_csv):
                    importar_de_csv(arquivos_csv[escolha])
                    print(f"Dados importados com sucesso do arquivo {arquivos_csv[escolha].name}.")
                else:
                    print("Escolha inválida.")
            else:
                print("Não há arquivos CSV disponíveis para importação.")
        
        elif opcao == "8":
            print("Fazer backup do banco de dados\n")
            fazer_backup()
            print("Backup realizado com sucesso.")
        
        elif opcao == "9":
            print("Saindo...")
            break
        
        else:
            print("Opção inválida. Tente novamente.")

        input("\nPressione Enter para voltar ao menu...")


if __name__ == "__main__":
    inicializar_diretorios()
    inicializar_banco()
    menu()
