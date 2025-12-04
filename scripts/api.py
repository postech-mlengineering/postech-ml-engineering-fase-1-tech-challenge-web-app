import requests
from requests.exceptions import RequestException
import streamlit as st
import pandas as pd


def encontrar_url_ativa():
    '''
    Testa sequencialmente as URLs de health check e retorna a URL base (sem o /health)
    da primeira API que responder com sucesso.
    '''
    for full_url in urls:
        try:
            response = requests.get(full_url, timeout=5) 
            if response.ok:
                url_base = full_url.rsplit('api/v1/health', 1)[0]
                return url_base
        except RequestException:
            continue  
    raise ConnectionError('Nenhuma API respondeu ao health check.')


def login(usuario, senha):
    '''Lida com o login do usuário e recupera o token JWT.'''
    try:
        response = requests.post(endpoint_login, json={'username': usuario, 'password': senha})
        if response.status_code == 200:
            return response.json().get('access_token'), None 
        else:
            try:
                erro_data = response.json()
                return None, erro_data.get('error', 'Credenciais inválidas.')
            except requests.exceptions.JSONDecodeError:
                return None, f'Erro de comunicação com a API (Status: {response.status_code}).'
    except requests.exceptions.ConnectionError:
        return None, f'Erro de conexão: não foi possível conectar à API em {url_base}.'
    except Exception as e:
        return None, f'Ocorreu um erro inesperado durante o login: {e}'


def register(usuario, senha):
    '''Lida com o registro do usuário.'''
    try:
        response = requests.post(endpoint_register, json={'username': usuario, 'password': senha})
        if response.status_code == 201:
            return True, response.json().get('msg') 
        else:
            try:
                erro_data = response.json()
                return False, erro_data.get('error', 'Falha no registro.')
            except requests.exceptions.JSONDecodeError:
                return False, f'Erro de comunicação com a API (Status: {response.status_code}).'
    except requests.exceptions.ConnectionError:
        return False, f'Erro de conexão: não foi possível conectar à API em {url_base}.'
    except Exception as e:
        return False, f'Ocorreu um erro inesperado durante o registro: {e}'


urls = [
    'https://postech-api-ml-fase-1.vercel.app/api/v1/health',
    'http://localhost:5000/api/v1/health'
]

try:
    url_base = encontrar_url_ativa()
    print(f'URL ativa definida: {url_base}')
except ConnectionError as e:
    print(f'Erro Crítico: {e}')
    url_base = None 

endpoint_login = f'{url_base}/api/v1/auth/login'
endpoint_register = f'{url_base}/api/v1/auth/register'