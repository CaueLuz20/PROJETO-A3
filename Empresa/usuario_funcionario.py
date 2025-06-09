import socket
import json

def enviar_pedido(pedido):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("localhost", 5000))
    s.send(json.dumps(pedido).encode())
    resposta = s.recv(4096).decode()
    s.close()
    return json.loads(resposta)

def listar_tarefas(funcionario):
    pedido = {"tipo_cliente":"funcionario", "acao":"listar_tarefas", "funcionario": funcionario}
    return enviar_pedido(pedido)

def concluir_tarefa(tarefa_id):
    pedido = {"tipo_cliente":"funcionario", "acao":"concluir_tarefa", "tarefa_id": tarefa_id}
    return enviar_pedido(pedido)

def main():
    nome = input("Digite seu nome: ")
    while True:
        print("\n1 - Listar tarefas pendentes")
        print("2 - Concluir tarefa")
        print("0 - Sair")
        print("_____________________________________________________")
        escolha = input("Escolha: ")
        if escolha == "1":
            res = listar_tarefas(nome)
            if "erro" in res:
                print("Erro:", res["erro"])
            else:
                tarefas = res.get("tarefas", [])
                if tarefas:
                    for t in tarefas:
                        print(f"ID {t['id']}: {t['descricao']} (Status: {t['status']})")
                else:
                    print("Nenhuma tarefa pendente.")
        elif escolha == "2":
            id_tarefa = int(input("Digite ID da tarefa para concluir: "))
            res = concluir_tarefa(id_tarefa)
            print(res.get("sucesso") or res.get("erro"))
        elif escolha == "0":
            break
        else:
            print("Opção inválida")

if __name__ == "__main__":
    main()