import requests
import json
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

MONDAY_API_URL = "https://api.monday.com/v2"
MONDAY_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjU1NTA4OTc0MCwiYWFpIjoxMSwidWlkIjo3NzEyODU2OSwiaWFkIjoiMjAyNS0wOC0yN1QxMzoxODozOS41NTdaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MTM1MzY5ODEsInJnbiI6InVzZTEifQ.8tcxfeufu9e2MwW41O8SgEPDdx4D-5boqPmTJwF4u0Q"
BOARD_ID = 9909832567

@tool(
    name="criar_lead_monday",
    description="Tool para criar um lead no Monday com as informações do comprador",
    permission=ToolPermission.ADMIN
)
def criar_lead_monday(
    nome: str,
    email: str,
    telefone: str,
    modelo: str,
    orcamento: float,
    contato_preferido: str,
    observacoes: str = ""
) -> dict:
    """
    Executar essa ferramenta quando o comprador quiser falar com um vendedor.

    Args:
        nome (str): Nome do cliente.
        email (str): Email do cliente.
        telefone (str): Telefone do cliente.
        modelo (str): Modelo de carro de interesse.
        orcamento (float): Orçamento do cliente.
        contato_preferido (str): Canal preferido de contato.
        observacoes (str, optional): Observações adicionais.

    Returns:
        dict: Resultado da operação com 'success' e 'lead_id' ou 'errors'.
    """

    # Monta os valores das colunas do Monday
    column_values = {
        "email_mkv723vd": {"email": email, "text": email},
        "phone_mkv752g6": {"phone": telefone, "text": telefone},
        "color_mkv7634a": {"label": "Chamado"},
        "dropdown_mkv74zs2": {"labels": [modelo]},
        "numeric_mkv776vz": str(orcamento),
        "dropdown_mkv7rpbf": {"labels": [contato_preferido]},
        "long_text_mkv713jb": observacoes
    }

    query = """
    mutation {
      create_item(
        board_id: %s,
        item_name: "%s",
        column_values: "%s"
      ) {
        id
      }
    }
    """ % (BOARD_ID, nome, json.dumps(column_values).replace('"', '\\"'))

    headers = {
        "Authorization": MONDAY_TOKEN,
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(MONDAY_API_URL, headers=headers, json={"query": query})
        result = response.json()

        if "errors" in result:
            return {"success": False, "errors": result["errors"]}
        
        lead_id = result["data"]["create_item"]["id"]
        return {"success": True, "lead_id": lead_id}

    except Exception as e:
        return {"success": False, "errors": str(e)}
