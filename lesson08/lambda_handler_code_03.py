import json

def lambda_handler(event, context):
    # print("Received event:", json.dumps(event)) # To be added for debug
    method = event.get("httpMethod", "UNKNOWN")

    if method == "GET":
        params = event.get("queryStringParameters", {}) or {}
        name = params.get("name", "Guest")  
        return {
            'statusCode': 200,
            'body': json.dumps({"method": "GET", "message": f"Hello, {name}"})
        }
    elif method == "POST":
        body = json.loads(event.get("body") or "{}")
        name = body.get("name", "Guest")   
        return {
            'statusCode': 200,
            'body': json.dumps({"method": "POST", "message": f"Hello, {name}"})
        }
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({"error": "Unsupported HTTP method"})
        }