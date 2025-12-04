import streamlit as st
from scripts.api import login, register, url_base


st.set_page_config(
    page_title='',
    layout='wide',
    initial_sidebar_state="collapsed"
)

if 'logado' not in st.session_state:
    st.session_state.logado = False
if 'token_acesso' not in st.session_state:
    st.session_state.token_acesso = None
if 'usuario' not in st.session_state:
    st.session_state.usuario = None


def show_login():
    '''Renderiza os formulários de login e registro.'''
    _, col2, _ = st.columns([.3, .4, .3])
    with col2:
        st.title('Books2Scrape')
        tab1, tab2 = st.tabs(['Login', 'Cadastro'])
        with tab1:
            st.subheader('Entrar')
            with st.form('form_login', clear_on_submit=False):
                usuario = st.text_input('Usuário', key='input_usuario')
                senha = st.text_input('Senha', type='password', key='input_senha')
                entrar = st.form_submit_button('Entrar')
                if entrar:
                    token, erro = login(usuario, senha)
                    if token:
                        st.session_state.token_acesso = token
                        st.session_state.usuario = usuario
                        st.session_state.logado = True
                        st.success(f'Login bem-sucedido. Bem-vindo(a), {usuario}!')
                        st.rerun()
                    else:
                        st.error(erro)
        with tab2:
            st.subheader('Criar Conta')
            with st.form('form_cadastro', clear_on_submit=True):
                usuario = st.text_input('Novo Usuário', key='input_novo_usuario')
                senha = st.text_input('Nova Senha', type='password', key='input_nova_senha')
                cadastrar = st.form_submit_button('Cadastrar')
                if cadastrar:
                    sucesso, msg = register(usuario, senha)
                    if sucesso:
                        st.success(msg)
                    else:
                        st.error(msg)
        st.markdown('---')
        st.info(f'URL base da API: {url_base}')


def show_logout_button():
    '''Botão de sair no sidebar.'''
    if st.button('Sair', key='logout_btn'):
        st.session_state.logado = False
        st.session_state.token_acesso = None
        st.session_state.usuario = None
        st.rerun()


if st.session_state.logado:
    st.markdown(f'Logado como: **{st.session_state.usuario}**')
    show_logout_button()
    st.title('Página inicial')
else:
    show_login()