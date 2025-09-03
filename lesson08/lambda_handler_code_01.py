def lambda_handler(event, context):
    name = event.get("queryStringParameters", {}).get("name", "Guest")

    return {
        'statusCode': 200,
        'body': f"Hello, {name}"
    }