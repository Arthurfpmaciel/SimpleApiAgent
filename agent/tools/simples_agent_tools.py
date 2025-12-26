from langchain_core.tools import tool
import requests
from dotenv import load_dotenv
import os
load_dotenv(".env")

@tool
def dog_age(age: int) -> int:
    """
    Calcula a idade de um cachorro a partir da idade humana.
    """
    return age * 7

@tool
def search_web(query: str) -> str:
    """
    Pesquisa informações atualizadas na internet.
    Use somente quando o usuário pedir explicitamente para buscar na internet ou pesquisar aquela informação.
    """
    response = requests.get(
        "https://api.tavily.com/search",
        params={
            "query": query,
            "api_key": os.getenv("TAVILY_API_KEY"),
            "max_results": 5
        }
    )
    return response.text

@tool
def search_animal_wikipedia(animal_name: str) -> str:
    """
    Busca informações sobre um animal na Wikipedia.
    Use sempre que o usuário perguntar sobre um animal.
    """
    print("usou a api do wikipedia", flush=True)
    animal_name = animal_name.lower().strip().replace(" ", "_")
    url = f"https://pt.wikipedia.org/api/rest_v1/page/summary/{animal_name}"
    HEADERS = {
        "User-Agent": "AnimalAgent/1.0 (contato: seu_email@dominio.com)",
        "Accept": "application/json"
    }
    response = requests.get(url, headers=HEADERS, timeout=5)
    if response.status_code != 200:
        return f"Erro ao consultar a Wikipedia (status {response.status_code})."
    data = response.json()
    extract = data.get("extract")
    if not extract:
        return "Nenhuma informação relevante encontrada na Wikipedia."
    return extract

tools = [dog_age, search_animal_wikipedia]