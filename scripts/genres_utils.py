import logging
import requests
from scripts import URL_BASE
from typing import List, Dict


logger = logging.getLogger(__name__)


def get_all_genres(token: str) -> List[Dict[str, str]]:
    '''
    Recupera a lista de todas os gêneros de livros cadastradas.

    Args:
        token: Token JWT de autenticação.

    Returns:
        Uma lista de dicionários contendo os gêneros.
    '''
    headers = {'Authorization': f'Bearer {token}'}
    try:
        response = requests.get(f'{URL_BASE}/genres', headers=headers, timeout=5)
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f'Erro de requisição: {e}')
        return []
    except Exception as e:
        logger.error(f'error: {e}')
        return []