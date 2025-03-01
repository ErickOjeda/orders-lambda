import json
import boto3
import datetime
from decimal import Decimal

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
        
        body = json.loads(event['body'])
        novo_status = body.get("status")

        if not novo_status:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "O campo 'status' é obrigatório no body."})
            }

        agora = datetime.datetime.utcnow().isoformat()

        response = tabela.update_item(
            Key={"id": order_id},
            UpdateExpression="SET #s = :s, #d = :d",
            ExpressionAttributeNames={
                "#s": "status",
                "#d": "data_atualizacao"
            },
            ExpressionAttributeValues={
                ":s": novo_status,
                ":d": agora
            },
            ReturnValues="ALL_NEW"
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Pedido atualizado com sucesso",
                "status": "ENVIADO"
            })
        }

    except Exception as e:
        print("Erro:", e)
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Erro ao atualizar o status.", "details": str(e)})
        }
