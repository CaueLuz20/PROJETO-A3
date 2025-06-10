import socket
import json
import sqlite3
from datetime import datetime

conn = sqlite3.connect('tarefas.db', check_same_thread=False)
cursor = conn.cursor()

def criar_tabela():
    cursor.execute("CREATE TABLE IF NOT EXISTS tarefas (" \
    "id INTEGER PRIMARY KEY AUTOINCREMENT," \
    "descricao TEXT NOT NULL," \
    "funcionario TEXT NOT NULL," \
    "status TEXT CHECK(status IN ('pendente','concluida')) NOT NULL DEFAULT 'pendente'," \
    "data_criacao TEXT NOT NULL," \
    "data_conclusao TEXT)")
    conn.commit()

criar_tabela()

def criar_tabela_funcionarios():
    cursor.execute("CREATE TABLE IF NOT EXISTS funcionarios (nome TEXT PRIMARY KEY)")
    cursor.execute("SELECT COUNT(*) FROM funcionarios")
    if cursor.fetchone()[0] == 0:
        funcionarios_iniciais = [
            ("João",),
            ("Maria",),
            ("Carlos",),
            ("Rose",),
            ("Rita",),
            ("Alberto",),
            ('Ana',),
            ('Pedro',),
            ('Fernanda',),
            ('Lucas',),
            ('Julia',), 
            ('Roberto',),
            ('Patrícia',),
            ('Eduardo',),
            ('Camila',),
            ('Thiago',),
            ('Larissa',),
            ('Rafael',),
            ('Isabela',),
            ('Gustavo',)
            ]
        cursor.executemany("INSERT INTO funcionarios (nome) VALUES (?)", funcionarios_iniciais)
        conn.commit()

criar_tabela_funcionarios()

def processar_requisicao(dados):
    tipo = dados.get("tipo_cliente")
    acao = dados.get("acao")

    if tipo == "funcionario":
        if acao == "listar_tarefas":
            funcionario = dados.get("funcionario")
            if not funcionario:
                return {"erro": "Nome do funcionário não informado"}
            cursor.execute("SELECT id, descricao, status FROM tarefas WHERE funcionario=? AND status='pendente'", (funcionario,))
            tarefas = [{"id": t[0], "descricao": t[1], "status": t[2]} for t in cursor.fetchall()]
            return {"tarefas": tarefas}
        
        elif acao == "concluir_tarefa":
            tarefa_id = dados.get("tarefa_id")
            cursor.execute("SELECT status FROM tarefas WHERE id=?", (tarefa_id,))
            tarefa = cursor.fetchone()
            if not tarefa:
                return {"erro": "Tarefa não encontrada"}
            if tarefa[0] == "concluida":
                return {"erro": "Essa Tareja ja foi concluída anteriormente"}
            now = datetime.now().isoformat()
            cursor.execute("UPDATE tarefas SET status='concluida', data_conclusao=? WHERE id=?", (now, tarefa_id))
            conn.commit()
            return {"sucesso": "Tarefa concluída com sucesso"}
        
        elif acao == "listar_funcionarios":
            cursor.execute("SELECT nome FROM funcionarios")
            funcionarios = [f[0] for f in cursor.fetchall()]
            return {"funcionarios": funcionarios}

        else:
            return {"erro": "Ação inválida para funcionário"}

    elif tipo == "supervisor":
        if acao == "cadastrar_tarefa":
            funcionario = dados.get("funcionario")
            descricao = dados.get("descricao")
            if not funcionario or not descricao:
                return {"erro": "Dados insuficientes para cadastrar tarefa"}
            cursor.execute("SELECT 1 FROM funcionarios WHERE nome=?", (funcionario,))
            if cursor.fetchone() is None:
                return {"erro": "Funcionário não cadastrado"}
            now = datetime.now().isoformat()
            cursor.execute("INSERT INTO tarefas (descricao, funcionario, data_criacao) VALUES (?, ?, ?)", (descricao, funcionario, now))
            conn.commit()
            return {"sucesso": "Tarefa cadastrada"}

        elif acao == "listar_tarefas":
            funcionario = dados.get("funcionario")
            if not funcionario:
                return {"erro": "Nome do funcionário não informado"}
            cursor.execute("SELECT id, descricao, status FROM tarefas WHERE funcionario=?", (funcionario,))
            tarefas = [{"id": t[0], "descricao": t[1], "status": t[2]} for t in cursor.fetchall()]
            return {"tarefas": tarefas}
        
        elif acao == "listar_funcionarios":
            cursor.execute("SELECT nome FROM funcionarios")
            funcionarios = [f[0] for f in cursor.fetchall()]
            return {"funcionarios": funcionarios}
        
        else:
            return {"erro": "Ação inválida para supervisor"}

    elif tipo == "gerente":
        if acao == "relatorio":
            tipo_rel = dados.get("tipo_relatorio")
            if tipo_rel == "tarefas_cadastradas":
                cursor.execute("SELECT id, descricao, funcionario, status FROM tarefas")
                tarefas = [{"id": t[0], "descricao": t[1], "funcionario": t[2], "status": t[3]} for t in cursor.fetchall()]
                return {"relatorio": tarefas}
            elif tipo_rel == "tarefas_pendentes":
                cursor.execute("SELECT id, descricao, funcionario FROM tarefas WHERE status='pendente'")
                tarefas = [{"id": t[0], "descricao": t[1], "funcionario": t[2]} for t in cursor.fetchall()]
                return {"relatorio": tarefas}
            elif tipo_rel == "funcionarios_sem_tarefas_pendentes":
                cursor.execute("SELECT nome FROM funcionarios WHERE nome NOT IN (SELECT funcionario FROM tarefas WHERE status = 'pendente')")
                funcs = [f[0] for f in cursor.fetchall()]
                return {"relatorio": funcs}
            else:
                return {"erro": "Tipo de relatório inválido"}
        else:
            return {"erro": "Ação inválida para gerente"}

    else:
        return {"erro": "Tipo de cliente inválido"}

def iniciar_servidor():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("localhost", 5000))
    s.listen()
    print("Servidor iniciado. Aguardando conexões...\n")
    while True:
        cliente, addr = s.accept()
        print(f"> Conexão recebida de {addr}")
        try:
            dados_bytes = cliente.recv(4096)
            dados_str = dados_bytes.decode()
            dados_json = json.loads(dados_str)
            print(f"> Pedido recebido: {dados_json}")
            resposta = processar_requisicao(dados_json)
        except Exception as e:
            resposta = {"erro": "Erro ao processar requisição: " + str(e)}
        cliente.send(json.dumps(resposta).encode())
        cliente.close()
        print("> Resposta enviada. Aguardando próxima conexão...\n")

if __name__ == "__main__":
    iniciar_servidor()