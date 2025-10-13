import os
import json
import boto3
from smolagents import CodeAgent, WebSearchTool
from smolagents.models import Model, ChatMessage, MessageRole


class DeepSeekBedrockModel(Model):
    """专门适配 DeepSeek 模型的 Bedrock 模型类"""

    def __init__(self, model_id, region_name="us-east-2", **kwargs):
        self.model_id = model_id
        self.region_name = region_name
        self.client = boto3.client('bedrock-runtime', region_name=region_name)

    def generate(self, messages, stop_sequences=None, **kwargs):
        """生成响应"""
        request_body = self._prepare_request_body(messages, stop_sequences, **kwargs)

        try:
            response = self.client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(request_body),
                contentType="application/json",
            )
            response_body = json.loads(response["body"].read())

            # 解析 DeepSeek 响应
            if "outputs" in response_body and len(response_body["outputs"]) > 0:
                text = response_body["outputs"][0]["text"]
            else:
                text = response_body.get("generation", "")

            return ChatMessage(role=MessageRole.ASSISTANT, content=text)

        except Exception as e:
            raise Exception(f"Error calling DeepSeek model: {e}")

    def _prepare_request_body(self, messages, stop_sequences=None, **kwargs):
        """准备请求体"""
        # DeepSeek 使用 OpenAI 兼容的格式
        formatted_messages = []
        for msg in messages:
            formatted_messages.append({
                "role": msg.role.value,
                "content": msg.content
            })

        body = {
            "messages": formatted_messages,
            "max_tokens": 4096,
            "temperature": 0.1,
        }

        if stop_sequences:
            body["stop"] = stop_sequences

        return body


# 使用自定义模型
model = DeepSeekBedrockModel(
    model_id=os.environ.get("AMAZON_BEDROCK_MODEL_ID"),
    client_kwargs={"region_name": os.environ.get("AWS_REGION", "us-east-2")}
)

agent = CodeAgent(
    tools=[WebSearchTool()],
    model=model
)

# 测试运行
output = agent.run("How many seconds would it take for a leopard at full speed to run through Pont des Arts?",
                   stream=True)

for event in output:
    print(f"Event: {type(event).__name__}")
    if hasattr(event, 'output'):
        print(f"Output: {event.output}")