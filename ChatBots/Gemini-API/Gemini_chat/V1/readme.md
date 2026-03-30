
# Gemini_chat_V1

Um WebApp interativo de chat construído com Python e Streamlit, integrado à API do Google Gemini. Este projeto foi desenvolvido para explorar a criação de interfaces conversacionais com IA e a persistência de dados utilizando SQLite.

## Funcionalidades

* **Chat em Tempo Real:** Interface fluida e responsiva utilizando Streamlit.
* **Integração com LLM:** Respostas geradas pela API do Google Gemini.
* **Prompt Engineering Embutido:** Configuração de "System Instructions" para guiar o comportamento e o tom da IA.
* **Persistência de Histórico (SQLite):** * Criação de múltiplas sessões de chat.
    * Armazenamento de mensagens (usuário e assistente) em banco de dados relacional.
    * Recuperação de contexto: a IA lembra das mensagens anteriores da mesma sessão.

## Tecnologias Utilizadas

* **Linguagem:** Python 3
* **Gerenciador de Pacotes:** `uv`
* **Interface Web:** Streamlit
* **Inteligência Artificial:** [Google Generative AI](https://ai.google.dev/)
* **Banco de Dados:** SQLite (nativo do Python)
