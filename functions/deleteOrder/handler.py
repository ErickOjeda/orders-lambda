import json
import boto3

dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
tabela = dynamodb.Table("orders")

def lambda_handler(event, context):
    
    order_id = event.get("pathParameters", {}).get("id")

    if not order_id:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Parâmetro 'id' é obrigatório."})
        }

    try:
        
        response = tabela.get_item(Key={"id": order_id})

        if "Item" not in response:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "Pedido não encontrado."})
            }

        tabela.delete_item(Key={"id": order_id})

        return {
            "statusCode": 204,
            "body": ""
        }

    except Exception as e:
        print("Erro:", e)
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Erro ao deletar o pedido.", "details": str(e)})
        }
