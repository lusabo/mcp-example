import streamlit as st
import asyncio
from fastmcp import Client

async def call_hello(name):
    async with Client("http://localhost:8000/mcp") as client:
        response = await client.call_tool("hello", {"name": name})
        return response[0].text

st.title("Olá com MCP 👋")

name_input = st.text_input("Digite seu nome:")

if st.button("Enviar"):
    if name_input.strip():
        with st.spinner("Chamando o servidor..."):
            result = asyncio.run(call_hello(name_input))
            st.success(result)
    else:
        st.warning("Por favor, insira um nome.")