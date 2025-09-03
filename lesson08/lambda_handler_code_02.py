import json

def lambda_handler(event, context):
    body = json.loads(event.get("body") or "{}")
    name = body.get("name", "Guest")
    age = body.get("age", None)

    return {
        'statusCode': 200,
        'body': json.dumps({"message": f"Hello, {name}", "age": age})
    }