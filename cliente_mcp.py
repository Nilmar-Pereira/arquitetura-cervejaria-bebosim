from mcp.client.stdio import stdio_client
from mcp import ClientSession as session, StdioServerParameters as session_parameters
from ia import *

import asyncio
import json

SYSTEM_PROMPT = """
Você é o arquiteto de software do sistema Cervejaria BeboSim.

Você tem acesso às seguintes ferramentas:
- decisoes_arquiteturais: lista todas as ADRs disponíveis
- justificativa_arquitetural: gera uma justificativa formal para uma ADR usando IA
- validar_adrs: valida se todas as ADRs possuem os campos obrigatórios

Instruções:
- Sempre utilize as ferramentas para responder
- Pode chamar mais de uma ferramenta em sequência se necessário
- Para chamar uma ferramenta responda exatamente no formato:
  TOOL: nome_da_ferramenta ARGS: {"parametro": "valor"}
- Quando não precisar mais de ferramentas, forneça a resposta final ao usuário
"""

async def get_response(ai_connection, mensagem):
    params = session_parameters(command="python3", args=["adrs.py"])
    async with stdio_client(params) as (read, write):
        async with session(read, write) as s:
            await s.initialize()

            list = await s.list_tools()

            # monta descrição das tools para incluir no prompt
            tools_descricao = "\n".join([
                f"- {tool.name}: {tool.description}"
                for tool in list.tools
            ])

            # loop de interação com o Gemini
            historico = f"{SYSTEM_PROMPT}\n\nFerramentas disponíveis:\n{tools_descricao}\n\nUsuário: {mensagem}\n"

            while True:
                response = ai_connection.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=historico
                )

                resposta_texto = response.text.strip()

                # verifica se a IA quer chamar uma tool
                tool_call = re.search(r'TOOL:\s*(\w+)\s*ARGS:\s*(\{.*?\})', resposta_texto, re.DOTALL)

                if tool_call:
                    tool_name = tool_call.group(1).strip()
                    tool_args = json.loads(tool_call.group(2).strip())

                    print(f"tool '{tool_name}' executada")

                    tool_response = await s.call_tool(
                        name=tool_name,
                        arguments=tool_args
                    )

                    historico += f"\nAssistente chamou tool '{tool_name}' e recebeu: {str(tool_response.content)}\n"

                else:
                    print(f"resposta final: {resposta_texto}")
                    break

if __name__ == "__main__":
    load_dotenv()
    gemini_key = os.getenv("GEMINI_API_KEY")
    ai_connection = conectar_gemini(gemini_key)

    # PROMPT 1 — ferramenta base: listar ADRs
    print("\n" + "="*50)
    print("PROMPT 1: Listar ADRs")
    print("="*50)
    asyncio.run(get_response(ai_connection,
        "liste todas as decisões arquiteturais disponíveis"))

    # PROMPT 2 — ferramenta 2: validar formato
    print("\n" + "="*50)
    print("PROMPT 2: Validar ADRs")
    print("="*50)
    asyncio.run(get_response(ai_connection,
        "valide o formato de todas as ADRs e me diga quais estão completas"))
    

    # PROMPT 3 — ferramenta 1: justificativa com IA
    print("\n" + "="*50)
    print("PROMPT 3: Justificativa ADR-01")
    print("="*50)
    asyncio.run(get_response(ai_connection,
        "gere uma justificativa formal para a decisão arquitetural ADR-01")) 