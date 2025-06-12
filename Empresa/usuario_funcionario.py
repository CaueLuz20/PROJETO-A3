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

def listar_funcionarios():
    pedido = {
        "tipo_cliente": "funcionario",
        "acao": "listar_funcionarios"
    }
    return enviar_pedido(pedido)

def main():
    while True:
        print("____________________________________________________________")
        nome = input("Digite seu nome, para entrar no sistema: ").strip().capitalize()
        print("____________________________________________________________")
        
        res = listar_funcionarios()

        if "funcionarios" in res and nome.lower() not in [f.lower() for f in res["funcionarios"]]:
            print("Esse usuário não existe! Por favor, verifique o nome digitado.")
            print("____________________________________________________________")
            input("Pressione Enter para tentar novamente...")
            continue  
        break  

    while True:
        print(nome, ", Seja Bem-Vindo(a) ao sistema de gerenciamento de tarefas")
        print("____________________________________________________________")
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
                        input("Pressione Enter para voltar ao menu...")
                else:
                    print("Nenhuma tarefa pendente.")
                    print("_____________________________________________________")
                    input("Pressione Enter para voltar ao menu...")
                    
        elif escolha == "2":
            id_tarefa = int(input("Digite ID da tarefa para concluir: "))
            res = concluir_tarefa(id_tarefa)
            print(res.get("sucesso") or res.get("erro"))
            print("\n_____________________________________________________")
            input("Pressione Enter para voltar ao menu...")
            
        elif escolha == "0":
            break
        else:
            print("Opção inválida")

if __name__ == "__main__":
    main()