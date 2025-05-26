import streamlit as st
import asyncio
from fastmcp import Client

async def get_user_age(name):
    async with Client("http://localhost:8000/mcp") as client:
        response = await client.call_tool("get_user_age", {"name": name})
        return response[0].text

st.title("Consultar idade de uma pessoa 🧓")

name_input = st.text_input("Digite o nome da pessoa:")

if st.button("Consultar"):
    if name_input.strip():
        with st.spinner("Consultando no banco de dados..."):
            result = asyncio.run(get_user_age(name_input))
            st.success(result)
    else:
        st.warning("Por favor, insira um nome válido.")
