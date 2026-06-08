from mcp.server.fastmcp import FastMCP
from utilidades import *
from ia import *
import os

import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)

ARQUIVO_ADRs = "arquitetura/Arquitetura_Cervejaria_BeboSim.md"

NAME = "Arquitetura Cervejaria BeboSim"
mcp = FastMCP(NAME)
logger = logging.getLogger(NAME)

global adrs
adrs = None
global adrs_carregadas
adrs_carregadas = False

global ai_connection 
ai_connection = None

load_dotenv()

def conectar_ia():
    global ai_connection

    if ai_connection == None:
        gemini_key = os.getenv("GEMINI_API_KEY")
        ai_connection = conectar_gemini(gemini_key)

    return ai_connection

def iniciar_adrs():
    global adrs
    global adrs_carregadas

    if not adrs or len(adrs) == 0:
        adrs_carregadas, adrs = carregar_adrs(ARQUIVO_ADRs)
        if adrs_carregadas:
            logger.info("adrs carregadas com sucesso")
        else:
            logger.error("não foi possível carregar as adrs")

    return adrs_carregadas, adrs    

@mcp.tool(name="decisoes_arquiteturais", title="lista de decisoes arquiteturais", description="retorna a lista completa de decisoes arquiteturais")
def get_adrs():
    decisoes = []

    carregadas, adrs = iniciar_adrs()
    if carregadas and isinstance(adrs, dict):  # <- adicione o isinstance
        if carregadas:
            for adr in adrs.values():
                decisoes.append({
                    "id": adr["id"],
                    "titulo": adr["titulo"]
                })

    return decisoes

@mcp.tool(name="decisao_arquitetural", title="lista detalhes de uma decisao arquitetural", description="retorna a lista de detalhes sobre uma decisao arquitetural")
def get_detalhes_adr(id_adr):
    detalhes = {}    
    
    carregadas, adrs = iniciar_adrs()
    if carregadas:
        detalhes = adrs[id_adr]

    return detalhes

# Tool com IA
@mcp.tool(
    name="justificativa arquitetural",
    title="Gerador de Justificativa Arquitetural",
    description="Dado o ID de uma ADR, utiliza IA para gerar uma justificativa formal e detalhada explicando por que aquela decisão arquitetural foi tomada"
)
def get_justificativa(id_adr: str, usar_mock: bool = True):
    carregadas, adrs = iniciar_adrs()
    if not carregadas or not isinstance(adrs, dict):
        return {"erro": "ADRs não carregadas"}
    
    adr = adrs.get(id_adr)
    if not adr:
        return {"erro": f"ADR '{id_adr}' não encontrada"}
    
    return ia_justificativa_para_adr(conectar_ia(),adr)

# Tool sem IA
@mcp.tool(
    name="validar_adrs",
    title="Validador de Formato das ADRs",
    description="Verifica se todas as ADRs possuem os três campos obrigatórios: Contexto, Decisão e pelo menos uma Consequência. Retorna um relatório de validação."
)
def validar_formato_adrs():
    carregadas, adrs = iniciar_adrs()

    if not carregadas or not isinstance(adrs, dict):
        return {"erro": "ADRs não carregadas"}

    relatorio = []
    total = 0
    completas = 0

    for adr in adrs.values():
        total += 1
        campos_faltando = []

        if not adr.get("contexto"):
            campos_faltando.append("Contexto")
        if not adr.get("decisao"):
            campos_faltando.append("Decisão")
        if not adr.get("consequencias"):
            campos_faltando.append("Consequências")

        if campos_faltando:
            status = "INCOMPLETA"
        else:
            status = "COMPLETA"
            completas += 1

        relatorio.append({
            "id": adr.get("id"),
            "titulo": adr.get("titulo"),
            "status": status,
            "campos_faltando": campos_faltando
        })

    return {
        "total_adrs": total,
        "completas": completas,
        "incompletas": total - completas,
        "detalhes": relatorio
    }
   
"""    
if __name__ == "__main__":
    try:
        iniciar_adrs()

        print("=== LISTA DE ADRs ===")
        print(get_adrs())

        print("\n=== DETALHES ADR-01 ===")
        print(get_detalhes_adr("ADR-01"))

        print("\n=== VALIDAÇÃO ===")
        print(validar_formato_adrs())

    except Exception as e:
        raise
"""
"""
@mcp.tool(name="recomendacoes", title="recomendacoes para uma decisao arquitetural", description="dado o identificador de uma decisao arquitetural retorna dicas e recomendacoes de boas praticas sobre como implementar")
def get_recomendacoes(id_adr, linguagem_framework):
    recomendacoes = {}    
    
    carregadas, adrs = iniciar_adrs()
    if carregadas:
        recomendacoes = ia_recomendacoes_para_adr(conectar_ia(), adrs[id_adr], linguagem_framework)

    return recomendacoes   
    """ 

if __name__ == "__main__":
    try:
        iniciar_adrs()
        # print(get_adrs())
        mcp.run()
    except Exception as e:
        raise
    