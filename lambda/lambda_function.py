
import json
import os
import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(body)
    }


def lambda_handler(event, context):
    try:
        method = event.get("requestContext", {}).get("http", {}).get("method")
        path = event.get("rawPath", event.get("path", "/"))

        if method == "POST" and path == "/visit":
            result = table.update_item(
                Key={"counter_id": "portfolio"},
                UpdateExpression="ADD visit_count :inc",
                ExpressionAttributeValues={
                    ":inc": 1
                },
                ReturnValues="UPDATED_NEW"
            )

            count = int(result["Attributes"]["visit_count"])

            return response(200, {
                "message": "Visit recorded successfully",
                "visit_count": count
            })

        elif method == "GET" and path == "/visits":
            result = table.get_item(
                Key={"counter_id": "portfolio"}
            )

            count = int(
                result.get("Item", {}).get("visit_count", 0)
            )

            return response(200, {
                "visit_count": count
            })

        return response(404, {
            "error": "Route not found"
        })

    except Exception as error:
        print(f"Error processing request: {error}")

        return response(500, {
            "error": "Internal server error"
        })
