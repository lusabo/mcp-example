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
    instructions="Você é um assistente que responde perguntas sobre pessoas.",
    mcp_servers=[mcp_server]
)

# Função assíncrona usando Runner.run()
async def ask_agent(question):
    await mcp_server.connect()
    result = await Runner.run(agent, question)
    return result.final_output

# UI com Streamlit
st.title("Converse com a IA via MCP 🤖")
question_input = st.text_input("Faça uma pergunta (ex: Qual a idade da Carla?)")

if st.button("Enviar"):
    if question_input.strip():
        with st.spinner("Consultando a IA..."):
            result = asyncio.run(ask_agent(question_input))
            st.success(result)
    else:
        st.warning("Por favor, digite uma pergunta.")
