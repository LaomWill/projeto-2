import sqlite3
import sys
import os

DATABASE_PATH = '/data/tasks.db'

def check_database_exists():
    """Verifica se o banco de dados existe"""
    if not os.path.exists(DATABASE_PATH):
        print(f"✗ Banco de dados não encontrado em {DATABASE_PATH}")
        print("Execute primeiro o container task-manager para criar dados.")
        return False
    return True

def read_all_tasks():
    """Lê todas as tarefas do banco persistido"""
    if not check_database_exists():
        return
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT id, title, description, status, created_at, completed_at 
            FROM tasks 
            ORDER BY id
        """)
        tasks = cursor.fetchall()
        
        print("\n" + "="*80)
        print("LEITOR DE DADOS PERSISTIDOS - Container Independente")
        print("="*80)
        print(f"Lendo dados de: {DATABASE_PATH}\n")
        
        if not tasks:
            print("⚠ Nenhuma tarefa encontrada no banco de dados.")
            print("Adicione tarefas usando o container task-manager primeiro.\n")
            return
        
        print(f"Total de tarefas encontradas: {len(tasks)}\n")
        
        for task in tasks:
            task_id, title, description, status, created_at, completed_at = task
            status_icon = "✓" if status == "concluída" else "○"
            
            print(f"[{status_icon}] Tarefa #{task_id}")
            print(f"    Título: {title}")
            if description:
                print(f"    Descrição: {description}")
            print(f"    Status: {status}")
            print(f"    Criada em: {created_at}")
            if completed_at:
                print(f"    Concluída em: {completed_at}")
            print()
        
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN status = 'concluída' THEN 1 ELSE 0 END) as completed,
                SUM(CASE WHEN status = 'pendente' THEN 1 ELSE 0 END) as pending
            FROM tasks
        """)
        total, completed, pending = cursor.fetchone()
        
        print("="*80)
        print("ESTATÍSTICAS")
        print("="*80)
        print(f"Total de tarefas: {total}")
        print(f"Concluídas: {completed or 0}")
        print(f"Pendentes: {pending or 0}")
        print(f"Taxa de conclusão: {(completed or 0) / total * 100:.1f}%")
        print("="*80 + "\n")
        
        print("✓ Dados lidos com sucesso do volume persistido!")
        print("Este container está lendo dados criados por outro container,")
        print("demonstrando a persistência através de volumes Docker.\n")
        
    except sqlite3.Error as e:
        print(f"✗ Erro ao ler banco de dados: {e}")
    finally:
        conn.close()

def main():
    print("\n🔍 Iniciando leitor de dados persistidos...\n")
    read_all_tasks()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nLeitor encerrado pelo usuário.")
        sys.exit(0)
