import socket
import json

def enviar_pedido(pedido):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("localhost", 5000))
    s.send(json.dumps(pedido).encode())
    resposta = s.recv(4096).decode()
    s.close()
    return json.loads(resposta)

def solicitar_relatorio(tipo_relatorio):
    pedido = {
        "tipo_cliente": "gerente",
        "acao": "relatorio",
        "tipo_relatorio": tipo_relatorio
    }
    return enviar_pedido(pedido)

def main():
    while True:
        print("\n1 - Relatório: todas as tarefas cadastradas")
        print("2 - Relatório: tarefas pendentes")
        print("3 - Relatório: funcionários sem tarefas pendentes")
        print("0 - Sair")
        print("_____________________________________________________")
        escolha = input("Escolha: ")
        if escolha == "1":
            res = solicitar_relatorio("tarefas_cadastradas")
            if "erro" in res:
                print("Erro:", res["erro"])
            else:
                tarefas = res.get("relatorio", [])
                if tarefas:
                    for t in tarefas:
                        print(f"ID {t['id']} - {t['descricao']} - Funcionário: {t['funcionario']} - Status: {t['status']}")
                else:
                    print("Nenhuma tarefa cadastrada.")
        elif escolha == "2":
            res = solicitar_relatorio("tarefas_pendentes")
            if "erro" in res:
                print("Erro:", res["erro"])
            else:
                tarefas = res.get("relatorio", [])
                if tarefas:
                    for t in tarefas:
                        print(f"ID {t['id']} - {t['descricao']} - Funcionário: {t['funcionario']}")
                else:
                    print("Nenhuma tarefa pendente.")
        elif escolha == "3":
            res = solicitar_relatorio("funcionarios_sem_tarefas_pendentes")
            if "erro" in res:
                print("Erro:", res["erro"])
            else:
                funcs = res.get("relatorio", [])
                if funcs:
                    print("Funcionários sem tarefas pendentes:")
                    for f in funcs:
                        print(f"- {f}")
                else:
                    print("Nenhum funcionário sem tarefas pendentes.")
        elif escolha == "0":
            break
        else:
            print("Opção inválida")

if __name__ == "__main__":
    main()