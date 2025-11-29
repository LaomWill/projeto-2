import sqlite3
import sys
from datetime import datetime

DATABASE_PATH = '/data/tasks.db'

def init_database():
    """Inicializa o banco de dados e cria a tabela se não existir"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'pendente',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✓ Banco de dados inicializado com sucesso!")

def add_task(title, description=""):
    """Adiciona uma nova tarefa"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO tasks (title, description) VALUES (?, ?)",
        (title, description)
    )
    
    task_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    print(f"✓ Tarefa #{task_id} adicionada: {title}")
    return task_id

def list_tasks():
    """Lista todas as tarefas"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, title, description, status, created_at FROM tasks ORDER BY id")
    tasks = cursor.fetchall()
    conn.close()
    
    if not tasks:
        print("Nenhuma tarefa encontrada.")
        return
    
    print("\n" + "="*80)
    print("LISTA DE TAREFAS")
    print("="*80)
    
    for task in tasks:
        task_id, title, description, status, created_at = task
        status_icon = "✓" if status == "concluída" else "○"
        
        print(f"\n[{status_icon}] Tarefa #{task_id} - {status.upper()}")
        print(f"    Título: {title}")
        if description:
            print(f"    Descrição: {description}")
        print(f"    Criada em: {created_at}")
    
    print("\n" + "="*80 + "\n")

def complete_task(task_id):
    """Marca uma tarefa como concluída"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute(
        "UPDATE tasks SET status = 'concluída', completed_at = ? WHERE id = ?",
        (datetime.now().isoformat(), task_id)
    )
    
    if cursor.rowcount > 0:
        conn.commit()
        print(f"✓ Tarefa #{task_id} marcada como concluída!")
    else:
        print(f"✗ Tarefa #{task_id} não encontrada.")
    
    conn.close()

def count_tasks():
    """Conta o total de tarefas"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*), SUM(CASE WHEN status = 'concluída' THEN 1 ELSE 0 END) FROM tasks")
    total, completed = cursor.fetchone()
    conn.close()
    
    pending = total - (completed or 0)
    
    print(f"\n📊 Estatísticas:")
    print(f"   Total de tarefas: {total}")
    print(f"   Concluídas: {completed or 0}")
    print(f"   Pendentes: {pending}\n")

def show_menu():
    """Exibe o menu interativo"""
    print("\n" + "="*60)
    print("GERENCIADOR DE TAREFAS - Sistema de Persistência")
    print("="*60)
    print("\n1. Adicionar tarefa")
    print("2. Listar tarefas")
    print("3. Concluir tarefa")
    print("4. Estatísticas")
    print("5. Sair")
    print()

def main():
    print("Inicializando sistema de gerenciamento de tarefas...")
    init_database()
    
    while True:
        show_menu()
        choice = input("Escolha uma opção: ").strip()
        
        if choice == '1':
            title = input("Título da tarefa: ").strip()
            if title:
                description = input("Descrição (opcional): ").strip()
                add_task(title, description)
            else:
                print("✗ Título não pode ser vazio!")
        
        elif choice == '2':
            list_tasks()
        
        elif choice == '3':
            try:
                task_id = int(input("ID da tarefa: ").strip())
                complete_task(task_id)
            except ValueError:
                print("✗ ID inválido!")
        
        elif choice == '4':
            count_tasks()
        
        elif choice == '5':
            print("\nEncerrando sistema. Dados persistidos em /data/tasks.db")
            break
        
        else:
            print("✗ Opção inválida!")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSistema encerrado pelo usuário.")
        sys.exit(0)
