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
    try:
        
        response = tabela.scan()
        
        items = response.get("Items", [])
        
        formatted_items = [
            {
                "id": item.get("id"),
                "cliente": item.get("cliente"),
                "total": float(item.get("total", 0)),  
                "status": item.get("status")
            }
            for item in items
        ]

        return {
            "statusCode": 200,
            "body": json.dumps(formatted_items, default=decimal_default)
        }
    
    except Exception as e:
        print("Erro:", e)
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Erro ao listar os pedidos.", "details": str(e)})
        }
