from dotenv import load_dotenv
import httpx
import os

load_dotenv()
VETSYS_API_URL = os.getenv("VETSYS_API_URL")
if not VETSYS_API_URL:
    raise RuntimeError('Sua VETSYS_API_URL não está no .env.')

cliente = httpx.Client(base_url="http://localhost:8000")

cabecalho = {}


def fazer_login(cliente, email, senha):
    """Faz login na VetSys API e devolve o cabeçalho Authorization com o token.
    Lança RuntimeError se o login falhar."""
    login = cliente.post("/auth/login", data={"username": email, "password": senha})
    if login.status_code != 200:
        raise RuntimeError("Login falhou: e-mail ou senha incorretos.")
    token = login.json()["access_token"]
    return {"Authorization": "Bearer {}".format(token)}

def ver_historico(id_animal: int):
    """Mostra o histórico de procedimentos de um animal (consultas, vacinas, exames,
    castrações e cirurgias), em ordem de data.
    Recebe o ID numérico do animal. Se só souber o nome, use buscar_animais antes."""
    requisicao = cliente.get("/animais/{}/procedimentos".format(id_animal), headers=cabecalho)
    if requisicao.status_code == 404:
        return "Animal não encontrado."
    if requisicao.status_code == 403:
        return "Você não está autorizado / Não tem permissão."
    return requisicao.json()

def buscar_animais(nome: str):
    """Busca animais da clínica pelo nome e devolve os dados de cada um, incluindo o ID.
    Use esta ferramenta para descobrir o ID de um animal quando o usuário citar só o nome,
    antes de consultar vacinas ou histórico.
    A busca ignora maiúsculas e minúsculas e aceita parte do nome.
    Pode devolver mais de um animal com o mesmo nome: nesse caso, não escolha sozinho,
    mostre as opções ao usuário (espécie, raça) e pergunte qual é."""
    animais = []
    requisicao = cliente.get("/animais", params={"limit": 100}, headers=cabecalho)
    if requisicao.status_code == 403:
        return "Você não está autorizado / Não tem permissão."
    for animal in requisicao.json():
        if nome.lower() in animal["nome"].lower():
            animais.append(animal)
    if len(animais) == 0:
        return "Nenhum animal encontrado com esse nome."
    return animais

def ver_vacinas(id_animal: int):
    """Mostra a carteira de vacinação de um animal: as vacinas aplicadas e as datas.
    Use quando o usuário perguntar sobre vacinas de um animal específico.
    Recebe o ID numérico do animal."""
    requisicao = cliente.get("/animais/{}/vacinas".format(id_animal), headers=cabecalho)
    if requisicao.status_code == 404:
        return "Animal não encontrado."
    if requisicao.status_code == 403:
        return "Você não está autorizado / Não tem permissão."
    return requisicao.json()

from getpass import getpass

while True:
    email = input("E-mail: ")
    senha = getpass("Senha: ")
    try:
        cabecalho.update(fazer_login(cliente, email, senha))
        break               
    except RuntimeError as erro:
        print(erro)