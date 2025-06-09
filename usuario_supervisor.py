import socket
import json

def enviar_pedido(pedido):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("localhost", 5000))
    s.send(json.dumps(pedido).encode())
    resposta = s.recv(4096).decode()
    s.close()
    return json.loads(resposta)

def cadastrar_tarefa(funcionario, descricao):
    pedido = {
        "tipo_cliente": "supervisor",
        "acao": "cadastrar_tarefa",
        "funcionario": funcionario,
        "descricao": descricao
    }
    return enviar_pedido(pedido)

def listar_tarefas(funcionario):
    pedido = {
        "tipo_cliente": "supervisor",
        "acao": "listar_tarefas",
        "funcionario": funcionario
    }
    return enviar_pedido(pedido)

def main():
    while True:
        print("\n1 - Cadastrar tarefa")
        print("2 - Listar tarefas de funcionário")
        print("0 - Sair")
        print("_____________________________________________________")
        escolha = input("Escolha: ")
        if escolha == "1":
            func = input("Nome do funcionário: ")
            desc = input("Descrição da tarefa: ")
            res = cadastrar_tarefa(func, desc)
            print(res.get("sucesso") or res.get("erro"))
        elif escolha == "2":
            func = input("Nome do funcionário: ")
            res = listar_tarefas(func)
            if "erro" in res:
                print("Erro:", res["erro"])
            else:
                tarefas = res.get("tarefas", [])
                if tarefas:
                    for t in tarefas:
                        print(f"ID {t['id']}: {t['descricao']} (Status: {t['status']})")
                else:
                    print("Nenhuma tarefa encontrada.")
        elif escolha == "0":
            break
        else:
            print("Opção inválida")

if __name__ == "__main__":
    main()
