from fastmcp import FastMCP
import psycopg2

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