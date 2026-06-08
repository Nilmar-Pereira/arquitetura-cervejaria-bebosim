import json
from google import genai
from dotenv import load_dotenv
import os
import re

MODEL = "gemini-2.5-flash-lite"

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

    #response = connection.chat.completions.create(
    response = connection.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt
        #messages=[
            #{"role": "user", "content": prompt}
       # ]
    )

    #if response and len(response.choices):
    justificativas = response.text
        #recomendacoes = response.choices[0].message.content
    justificativas = re.search(r'{.*}', justificativas, re.DOTALL)
    if justificativas:
        justificativas = justificativas.group(0)
    justificativas = json.loads(justificativas)

    return justificativas

if __name__ == "__main__":
    load_dotenv()
    gemini_key = os.getenv("GEMINI_API_KEY")
    connection = conectar_gemini(gemini_key)
    
    adr_teste = {
    "id": "ADR-01",
    "titulo": "Adoção do Estilo Arquitetural MVC",
    "contexto": "Necessidade de organizar um sistema web com múltiplos módulos CRUD e diferentes perfis de usuário, separando claramente as responsabilidades de interface, controle e dados.",
    "decisao": "Adotar o estilo arquitetural MVC (Model-View-Controller), separando a aplicação em camadas de apresentação (View), controle (Controller) e lógica de negócio e dados (Model)."
    }
    
    print("Testando com IA real")
    resultado = ia_justificativa_para_adr(connection, adr_teste)
    print(f"Justificativa: {resultado}")