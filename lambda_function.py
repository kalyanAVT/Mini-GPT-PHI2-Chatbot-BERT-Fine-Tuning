# this lambda function is used to connect to endpoint

import json
import boto3

sagemaker_runtime = boto3.client("sagemaker-runtime")
ENDPOINT_NAME = "Enter_your_EndPoint_name"

def lambda_handler(event, context):
    try:
        # Handle test event (direct) or API Gateway event
        if "inputs" in event:  # Test event directly in Lambda
            inputs = event["inputs"]
        elif "body" in event:
            body = event["body"]
            # body might be a JSON string (from API Gateway)
            if isinstance(body, str):
                body = json.loads(body)
            inputs = body.get("inputs")
        else:
            raise ValueError("Missing 'inputs' field")

        if not inputs or "question:" not in inputs or "context:" not in inputs:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "error": "'inputs' must include both 'question:' and 'context:'"
                })
            }

        # Call SageMaker endpoint
        response = sagemaker_runtime.invoke_endpoint(
            EndpointName=ENDPOINT_NAME,
            ContentType="application/json",
            Body=json.dumps({"inputs": inputs})
        )

        result = json.loads(response["Body"].read().decode("utf-8"))

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"answer": result})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
# Note: This Lambda function is designed to be triggered by an API Gateway or directly for testing.