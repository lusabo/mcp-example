from fastmcp import FastMCP
from email.mime.text import MIMEText
from dotenv import load_dotenv
import psycopg2
import smtplib
import os

load_dotenv()

# Configuração da conexão com o banco
conn = psycopg2.connect(
    dbname="mcpdb",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)

mcp = FastMCP(name="MyServer")

@mcp.tool()
def get_user_age(name: str) -> str:
    with conn.cursor() as cur:
        cur.execute("SELECT age FROM pessoas WHERE name = %s", (name,))
        result = cur.fetchone()
        if result:
            return f"{name} tem {result[0]} anos."
        return f"Usuário {name} não encontrado."
    
@mcp.tool()
def send_email_to_person(name: str, message: str) -> str:
    with conn.cursor() as cur:
        cur.execute("SELECT email FROM pessoas WHERE name = %s", (name,))
        result = cur.fetchone()
        if not result:
            return f"E-mail não encontrado para {name}."
        
        email_to = result[0]
        email_from = os.getenv("GMAIL_SENDER")
        email_pass = os.getenv("GMAIL_PASSWORD")

        if not email_from or not email_pass:
            return "Credenciais do Gmail não configuradas."

        try:
            msg = MIMEText(message)
            msg["Subject"] = f"Mensagem para {name}"
            msg["From"] = email_from
            msg["To"] = email_to

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(email_from, email_pass)
                server.send_message(msg)

            return f"E-mail enviado com sucesso para {name} ({email_to})."
        except Exception as e:
            return f"Erro ao enviar e-mail: {str(e)}"

@mcp.tool()
def list_all_users() -> str:
    with conn.cursor() as cur:
        cur.execute("SELECT name FROM pessoas")
        results = cur.fetchall()
        if results:
            nomes = [row[0] for row in results]
            return "Pessoas cadastradas: " + ", ".join(nomes)
        return "Nenhuma pessoa cadastrada no momento."

@mcp.tool()
def get_people_older_than(age: int) -> str:
    with conn.cursor() as cur:
        cur.execute("SELECT name, age FROM pessoas WHERE age > %s", (age,))
        results = cur.fetchall()
        if results:
            pessoas = [f"{row[0]} ({row[1]} anos)" for row in results]
            return f"Pessoas com mais de {age} anos: " + ", ".join(pessoas)
        return f"Não há pessoas com mais de {age} anos cadastradas."