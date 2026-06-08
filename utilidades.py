import re

def separar_adrs(conteudo):
    padrao = r"(## ADR-\d+.*?)(?=\n---|\Z)"

    blocos = re.findall(padrao, conteudo, re.DOTALL)

    adrs = {}
    for block in blocos:
        id_match = re.search(r"## (ADR-\d+)", block)
        titulo_match = re.search(r"## ADR-\d+: (.+)", block)

        contexto_match = re.search(
            r"\*\*Contexto:\*\*\s*(.*?)\s*\*\*Decisão:",
            block,
            re.DOTALL
        )

        decisao_match = re.search(
            r"\*\*Decisão:\*\*\s*(.*?)\s*\*\*Status:",
            block,
            re.DOTALL
        )

        status_match = re.search(
            r"\*\*Status:\*\*\s*(.*?)\s*\*\*Consequências:",
            block,
            re.DOTALL
        )
        
        consequencia_match = re.search(
            r"\*\*Consequências:\*\*\s*(.*)",
            block,
            re.DOTALL
        )

        id = id_match.group(1).strip() if id_match else None

        if id:
            adr = {
                "id": id,
                "titulo": titulo_match.group(1).strip() if titulo_match else None,
                "contexto": contexto_match.group(1).strip() if contexto_match else None,
                "decisao": decisao_match.group(1).strip() if decisao_match else None,
                "status": status_match.group(1).strip() if status_match else None,
                "consequencias": consequencia_match.group(1).strip() if consequencia_match else None,
            }
            adrs[id] = adr

    return adrs

def carregar_adrs(arquivo):
    carregadas, adrs = False, []

    try:
        with open(arquivo, "r") as a:
            adrs = separar_adrs(a.read())
            carregadas = True

            a.close()
    except Exception as e:
        print(f"erro carregando ADRs: {e}")

    return carregadas, adrs