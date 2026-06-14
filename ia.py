import json
from google import genai
from dotenv import load_dotenv
import os
import re

MODEL = "gemini-2.5-flash"

def conectar_gemini(key):
    client = genai.Client(api_key=key)

    return client

def ia_justificativa_para_adr(connection, adr):
    prompt = f"""
    Você é um arquiteto de software que deve ajudar desenvolvedores a concretizar decisões arquiteturais.

    Tarefa:
    Gere uma justificativa formal e detalhada explicando por que a seguinte decisão arquitetural foi tomada, com base no contexto descrito no ADR abaixo:

    ID: {adr.get('id')}
    Título: {adr.get('titulo')}
    Contexto: {adr.get('contexto')}
    Decisão: {adr.get('decisao')}

    Instruções:
    - A decisão foi escrita no formato de um Archteture Decision Record, então você deve considerar este formato.
    - Relacione a decisão ao contexto apresentado
    - Organize a resposta em JSON com os campos: 
      (i) "adr" contendo o id da ADR
      (ii) "justificativa" contendo o texto explicativo

    Restrições:
    - Retorne apenas as justificativas. Não inclua explicações sobre o seu processo de raciocínio, comentários ou texto adicional.
    - Cada recomendação deve ser concisa, com texto breve e claro 
    """

    response = connection.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    justificativas = response.text
    justificativas = re.search(r'{.*}', justificativas, re.DOTALL)
    if justificativas:
        justificativas = justificativas.group(0)

    return json.loads(justificativas)

