import os
import json
import boto3


def test_deepseek_apis():
    """测试 DeepSeek 模型的实际 API 响应"""
    bedrock_runtime = boto3.client('bedrock-runtime',
                                   region_name=os.environ.get("AWS_REGION", "us-east-2"))

    model_id = os.environ.get("AMAZON_BEDROCK_MODEL_ID")

    # 测试消息
    test_messages = [
        {
            "role": "user",
            "content": "What is 2+2? Answer briefly."
        }
    ]

    print("Testing DeepSeek model APIs...")
    print(f"Model ID: {model_id}")

    # 测试 1: converse API
    try:
        print("\n1. Testing converse API:")
        response = bedrock_runtime.converse(
            modelId=model_id,
            messages=[{"role": "user", "content": [{"text": "What is 2+2?"}]}]
        )
        print("Converse API Response:")
        print(json.dumps(response, indent=2, default=str))
    except Exception as e:
        print(f"Converse API failed: {e}")

    # 测试 2: invoke_model API (传统方式)
    try:
        print("\n2. Testing invoke_model API:")
        request_body = {
            "messages": [{"role": "user", "content": "What is 2+2?"}],
            "max_tokens": 100
        }
        response = bedrock_runtime.invoke_model(
            modelId=model_id,
            body=json.dumps(request_body)
        )
        response_body = json.loads(response['body'].read())
        print("Invoke_model API Response:")
        print(json.dumps(response_body, indent=2))
    except Exception as e:
        print(f"Invoke_model API failed: {e}")


if __name__ == "__main__":
    test_deepseek_apis()