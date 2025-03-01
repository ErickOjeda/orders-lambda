import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
tabela = dynamodb.Table("orders")

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return str(obj) 
    raise TypeError("Tipo não serializável")

def lambda_handler(event, context):
  
        order_id = event.get("pathParameters", {}).get("id")

        if not order_id:
            return {
                "statusCode": 400,
                "body": "Parâmetro 'id' é obrigatório."
            }

        try:  
            response = tabela.get_item(Key={"id": order_id})
            
            if "Item" not in response:
                return {
                    "statusCode": 404,
                    "body": "Pedido não encontrado."
                }

            item = response["Item"]

            formatted_item = {
                "id": order_id, 
                "cliente": item.get("cliente"),
                "email" : item.get("email"),
                "itens": item.get("itens", []),
                "total": float(item.get("total", 0)), 
                "status": item.get("status"),
                "data_criacao": item.get("data_criacao"),
                "data_atualizacao" : item.get("data_atualizacao")
            }


            return {
                "statusCode": 200,
                "body": json.dumps(formatted_item, default=decimal_default)
            }
    
        except Exception as e:
            print("Erro:", e)
            return {
                "statusCode": 500,
                "body": json.dumps({"error": "Erro ao listar os pedidos.", "details": str(e)})
            }
