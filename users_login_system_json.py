import os
import hashlib
import json
from pathlib import Path

class User:
    def __init__(self, username, password):
        self.username = username  
        self.password = password

#hashlib.sha256() é uma função do módulo hashlib que cria um objeto de hash SHA-256. encode() é usado para codificar uma string em uma sequência de bytes
#hexdigest(): Este método retorna a representação hexadecimal do hash calculado.   
class UserRepository:
    def __init__(self):
        self.users = []

    def user_exists(self, username, password):
        for user in self.users:
            if user.username == username:
                return True
        return False

    # verifica se um usuário com um determinado nome de usuário (username) já existe na lista de usuários (self.users).
    def add_user(self, user):
        #A isinstance() função retorna True se o objeto especificado for do tipo especificado, caso contrário False. 
        if isinstance(user, User):
            if not self.user_exists(user.username,user.password):
                self.users.append(user)
                print("Usuário adicionado com sucesso!")  
            else:
                print("Usuário já existe!")       
        else:
            print("DEU MERDA!")
           
    def login(self, username, password):
        for user in self.users:
            if user.username == username:
                return user.password == hashlib.sha256(password.encode()).hexdigest()
        return False

    #Para cada objeto user na lista self.users (que contém todos os usuários), estamos acessando o atributo __dict__ de cada objeto user.
    #O atributo __dict__ contém um dicionário que mapeia os nomes dos atributos para seus valores. Portanto, estamos criando uma lista de dicionários, onde cada dicionário representa os dados de um usuário.
    def save_to_json(self, filename):
        data = [user.__dict__ for user in self.users]
        with open(filename, 'w') as file:
            json.dump(data, file)

    # Abre o arquivo JSON em modo de leitura ('r')
    def load_from_json(self, filename):
        with open(filename, 'r') as file:
            # Carrega os dados do arquivo JSON para a variável 'data'
            data = json.load(file)
            # Utilizando compreensão de lista para cada usuário nos dados carregados do arquivo JSON, cria um objeto User
            # e adiciona-o à lista de usuários da instância atual da classe
            self.users = [User(**user) for user in data]

def create_user_from_input(user_repository):
    username = input("Digite o nome de usuário: ")
    password = input("Digite a senha: ")
    user = User(username, hashlib.sha256(password.encode()).hexdigest())
    user_repository.add_user(user)
    

def login_user_from_input(user_repository):
    username = input("Digite o nome de usuário: ")
    password = input("Digite a senha: ")
    if user_repository.login(username, password):
        print("Login bem sucedido!")
    else:
        print("Nome de usuário ou senha incorretos!")

# Função para limpar o terminal
def clear_terminal():
    os.system('clear') 

def choice(): 
    # Criando um novo arquivo:
    user_repository = UserRepository()
    filename = "users.json"
    # Verificando a existência de um arquivo:
    if Path(filename).exists():
        user_repository.load_from_json(filename)

    while True:
        print("[1] Criar usuário")
        print("[2] Fazer login")
        print("[3] Sair")

        choice = input("Escolha uma opção: ")

        if choice == "1":
            clear_terminal()
            create_user_from_input(user_repository)
            user_repository.save_to_json(filename)
        elif choice == "2":
            clear_terminal()
            login_user_from_input(user_repository)
        elif choice == "3":
            clear_terminal()
            print("GoodBay")
            break
        else:
            clear_terminal()
            print("Opção inválida!")

choice()