# app.py
import streamlit as st
import google.generativeai as genai
import os
import database as db
from dotenv import load_dotenv


# 1. Configuração da Página e Banco de Dados
st.set_page_config(page_title="Gemini ChatApp", layout="wide")
db.init_db()

# 2. Configuração da API do Gemini
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY") 
genai.configure(api_key=API_KEY)


SYSTEM_PROMPT = """
A partir de agora você é o Dr. Ernandez. Phd em psicologia, comportamento humano e linguagem corporal.
Você deve interagir com as informações providas nesse chat somente.
Responder de forma clara, educada e tom suave para seu paciente.
Levar em consideração o passado, e as informações que seu paciente fala.
E principalmente se atentar a estruturas em seus textos/fala ( verificar vicios de linguagem, tons de voz, pausas e etc).
Obtenha o máximo de informação que consegui durante as seções.

Seções:
Maximo de 1(uma) hora, se possível ajustar sua janela de contexto para esse intervalo.
Termine as seções somente em 1 dessas 3 situações:

1. paciente entendeu e solucionou o desabafo;


2. paciente satisfeito com a conversa;


3. paciente está comprometido em tentar os conselhos dado pelo Dr e voltará.

Seja cauteloso e atencioso com as respostas, sem ser muito direto, deixe fluir a conversa, perguntando encima da janela de contexto do paciente.

"""

# Inicializando o modelo com o Prompt Engineering embutido
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=SYSTEM_PROMPT
)

# 3. Gerenciamento de Estado da Sessão (Session State)
if "current_session_id" not in st.session_state:
    st.session_state.current_session_id = None

# 4. Interface: Sidebar para Histórico de Chats (Fase 2)
with st.sidebar:
    st.title("Histórico de Chats")
    if st.button("Novo Chat", use_container_width=True):
        st.session_state.current_session_id = db.create_session()
        st.rerun()

    st.divider()
    
    sessions = db.get_all_sessions()
    for session_id, title in sessions:
        if st.button(f"{title}", key=session_id, use_container_width=True):
            st.session_state.current_session_id = session_id
            st.rerun()

# 5. Interface: Área Principal do Chat (Fase 1)
if st.session_state.current_session_id is None:
    st.title("Bem-vindo ao WebApp do Gemini")
    st.write("Crie um **Novo Chat** na barra lateral para começar.")
else:
    current_session = st.session_state.current_session_id
    st.title("Conversa Atual")

    # Carregar mensagens do banco de dados (SQLite)
    chat_history = db.get_messages(current_session)
    
    # Reconstruir o histórico no objeto do Gemini para ele ter contexto da conversa
    gemini_history = []
    for role, content in chat_history:
        gemini_history.append({
            "role": "user" if role == "user" else "model",
            "parts": [content]
        })
    
    # Iniciar a sessão de chat do Gemini com o histórico recuperado
    chat = model.start_chat(history=gemini_history)

    # Exibir as mensagens na tela
    for role, content in chat_history:
        with st.chat_message("user" if role == "user" else "assistant"):
            st.markdown(content)

    # Input do usuário
    if prompt := st.chat_input("Digite sua mensagem para o Gemini..."):
        # Exibir a mensagem do usuário imediatamente
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Salvar a mensagem do usuário no DB
        db.save_message(current_session, "user", prompt)

        # Chamar a API do Gemini e obter a resposta
        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                response = chat.send_message(prompt)
                st.markdown(response.text)
        
        # Salvar a resposta no DB
        db.save_message(current_session, "model", response.text)