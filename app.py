import redis
import json
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import uuid

uri = "mongodb+srv://jonas:PCpyir20UvSL2v40@nosql.ocxhdgk.mongodb.net/?retryWrites=true&w=majority&appName=AtlasApp"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.biblioteca

conR = redis.Redis(
    host='redis-16217.c308.sa-east-1-1.ec2.cloud.redislabs.com',
    port=16217,
    password='Pi5K3Ge25WbYzAVgPmMeC0PDujv6dKSZ'
)

def geracao_token():
    token = str(uuid.uuid4())
    return token

def autenticacao_usuario(username):
    user = db.usuario.find_one({"nome": username})
    if user:
        token = geracao_token()
        conR.setex(token, 60, json.dumps({"username": username}))
        return token
    else:
        return None

def validacao_token(token):
    return conR.exists(token)

def acessar_mongodb(token):
    if validacao_token(token):
        username = json.loads(conR.get(token))["username"]
        print(f"Usuário {username} autenticado com sucesso!")

        user_id = json.loads(conR.get(token))["user_id"]

        while True:
            print("\nOpções:")
            print("1. Gerar relatório de favoritos")
            print("2. Gerar relatório de compras")
            print("3. Sair")

            choice = input("Escolha uma opção: ")

            if choice == "1":
                favoritos = db.favoritos.find({"user_id": user_id})
                print("\nRelatório de Favoritos:")
                for favorito in favoritos:
                    print(f"ID do Produto: {favorito['produto_id']}")

            elif choice == "2":
                compras = db.compras.find({"usuario_id": user_id})
                print("\nRelatório de Compras:")
                for compra in compras:
                    print(f"ID da Compra: {compra['_id']}")

            elif choice == "3":
                break

            else:
                print("Opção inválida. Tente novamente.")
    else:
        print("Token inválido. Faça login novamente.")

if __name__ == "__main__":
    while True:
        print("Opções:")
        print("1. Fazer login")
        print("2. Sair")

        choice = input("Escolha uma opção: ")

        if choice == "1":
            username = input("Digite o nome de usuário: ")
            token = autenticacao_usuario(username)
            if token:
                print(f"Login bem-sucedido! Seu token é: {token}")
                acessar_mongodb(token)
            else:
                print("Falha no login. Nome de usuário não encontrado.")
        elif choice == "2":
            break
        else:
            print("Opção inválida. Tente novamente.")
