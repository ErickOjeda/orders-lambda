import json
import boto3
import uuid
import traceback
from datetime import datetime

# Conexão com o DynamoDB
dynamodb = boto3.resource("dynamodb")
tabela = dynamodb.Table("orders")

def lambda_handler(event, context):
    try:
        
        data = json.loads(event['body'])
        data["total"] = 0

        if not data["itens"] or not data["cliente"] or not data["email"] or not isinstance(data["itens"], list): 
            return {
                "statusCode": 400,
                "body": "Os campos 'cliente', 'email' e 'items' são obrigatórios e o campo 'items' deve conter pelo menos um item."
            }

        for item in data["itens"]:
            data["total"] += item["quantidade"] * item["preco"]

        pedido = {
            "id": str(uuid.uuid4()),
            "cliente": data["cliente"],
            "email": data["email"],
            "itens": data["itens"],
            "total": data["total"],
            "status": "PENDENTE",
            "data_criacao": datetime.utcnow().isoformat(),
            "data_atualizacao": datetime.utcnow().isoformat()
        }

        resposta = tabela.put_item(Item=pedido)

        return {
            "statusCode": 201,
            "body": json.dumps({
                "id" : pedido["id"],
                "status": pedido["status"],
                "total": pedido["total"],
                "data_criacao": pedido["data_criacao"]
            })
        }

    except Exception as e:
        erro = traceback.format_exc()
        print("Erro:", erro)

        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Erro interno no servidor.", "details": str(e)})
        }