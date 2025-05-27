import streamlit as st
import asyncio
from dotenv import load_dotenv
from agents import Agent, Runner
from agents.mcp import MCPServerStreamableHttp

load_dotenv()

# Criação do servidor MCP com URL
mcp_server = MCPServerStreamableHttp({"url": "http://localhost:8000/mcp"})

# Configura o agente com a LLM da OpenAI e o servidor MCP
agent = Agent(
    name="AgentePessoas",
    instructions=
    """
    Você é um assistente que responde perguntas sobre pessoas.
    Use a ferramenta mais adequada com base na intenção do usuário.

    - Use 'get_user_age' para saber a idade de alguém.
    - Use 'send_email_to_person' para enviar uma mensagem.
    - Use 'list_all_users' para listar todas as pessoas.
    - Use 'get_people_older_than' para filtrar por idade.

    Adicione na resposta uma linha mostrando o fluxo de ferramentas utilizadas e
    quais argumentos usados em cada uma.
    """,
    mcp_servers=[mcp_server]
)

# Função assíncrona usando Runner.run()
async def ask_agent(question):
    await mcp_server.connect()
    result = await Runner.run(agent, question)
    return result.final_output

# UI com Streamlit
st.title("Converse com a IA via MCP 🤖")
question_input = st.text_input("Digite sua pergunta ou solicitação:")

if st.button("Enviar"):
    if question_input.strip():
        with st.spinner("Consultando a IA..."):
            result = asyncio.run(ask_agent(question_input))
            st.success(result)
    else:
        st.warning("Por favor, digite uma pergunta.")
