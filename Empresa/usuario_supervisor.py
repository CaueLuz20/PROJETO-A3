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

def listar_funcionarios():
    pedido = {
        "tipo_cliente": "supervisor",
        "acao": "listar_funcionarios"
    }
    return enviar_pedido(pedido)

def main():
    while True:
        print("____________________________________________________________")	
        print("\nSupervisor(a), Seja Bem-vindo(a) ao sistema de gerenciamento de tarefas")
        print("____________________________________________________________")	
        print("\n1 - Cadastrar tarefa")
        print("2 - Listar tarefas de funcionário")
        print("3 - Ver funcionários cadastrados")
        print("0 - Sair")
        print("_____________________________________________________")
        escolha = input("\nEscolha: ")
        
        if escolha == "1":
            func = input("Nome do funcionário: ").strip().capitalize()
            res = listar_funcionarios()
            if "funcionarios" in res and func not in res["funcionarios"]:
                print("Funcionário não cadastrado.")
                input("\nPressione Enter para voltar ao menu...")
                continue
            desc = input("Descrição da tarefa: ")
            res = cadastrar_tarefa(func, desc)
            print(res.get("sucesso") or res.get("erro"))
            input("\nPressione Enter para voltar ao menu...")
            
        elif escolha == "2":
            func = input("Nome do funcionário: ").strip().capitalize()
            res = listar_tarefas(func)
            if "funcionarios" in res and func not in res["funcionarios"]:
                print("Funcionário não cadastrado.")
                input("\nPressione Enter para voltar ao menu...")
                continue
            if "erro" in res:
                print("Erro:", res["erro"])
            else:
                tarefas = res.get("tarefas", [])
                if tarefas:
                    for t in tarefas:
                        print(f"ID {t['id']}: {t['descricao']} (Status: {t['status']})")
                else:
                    print("Nenhuma tarefa encontrada.")
            input("\nPressione Enter para voltar ao menu...")
                    
        elif escolha == "3":
            res = listar_funcionarios()
            if "funcionarios" in res:
                print("\nFuncionários cadastrados:")
                for nome in res["funcionarios"]:
                    print("-", nome)
                input("\nPressione Enter para voltar ao menu...")
            else:
                print("Não foi possível obter a lista de funcionários.")
                input("\nPressione Enter para voltar ao menu...")
                
        elif escolha == "0":
            break
        
        else:
            print("Opção inválida")

if __name__ == "__main__":
    main()
