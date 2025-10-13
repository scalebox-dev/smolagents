import json, os
from smolagents import (
    AmazonBedrockServerModel,
    ChatMessage,
    MessageRole,
    CodeAgent,
    WebSearchTool,
)

class CompatibleBedrockModel(AmazonBedrockServerModel):
    def generate(self, prompt, max_tokens=1024, temperature=0.7, **kwargs):
        # 1. 统一转成消息列表
        if isinstance(prompt, list):
            messages = [
                {"role": msg.role.value, "content": item["text"]}
                for msg in prompt
                for item in msg.content
                if item["type"] == "text"
            ]
        else:
            messages = [{"role": "user", "content": prompt}]

        # 2. 请求体（AWS 官方格式）
        body = {"messages": messages, "max_tokens": max_tokens, "temperature": temperature}

        # 3. 调用 Bedrock
        resp = self.client.invoke_model(
            modelId=self.model_id,
            body=json.dumps(body),
            accept="application/json",
            contentType="application/json",
        )

        # 4. 解析文本
        data = json.loads(resp["body"].read())
        if "deepseek" in self.model_id:
            text = data["choices"][0]["message"]["content"]
        else:
            text = data["content"][0]["text"]

        # 5. 确保返回格式正确 - 修复关键部分
        # 检查返回的 content 格式，确保是字符串或正确的字典列表
        if isinstance(text, list):
            # 如果返回的是列表，需要转换为字符串
            text = " ".join(str(item) for item in text)

        # 确保返回的 ChatMessage 格式正确
        return ChatMessage(
            role=MessageRole.ASSISTANT,
            content=[{"type": "text", "text": str(text)}]  # 确保这里是字典列表
        )

# 使用
model = CompatibleBedrockModel(
    model_id=os.environ["AMAZON_BEDROCK_MODEL_ID"],
    client_kwargs={"region_name": os.environ.get("AWS_REGION", "us-east-2")}
)

agent = CodeAgent(tools=[WebSearchTool()], model=model)
output=agent.run("How many seconds would it take for a leopard at full speed to run through Pont des Arts?",stream=True)
for event in output:
    print(event)