# from smolagents import CodeAgent, WebSearchTool, InferenceClientModel
#
# model = InferenceClientModel()
# agent = CodeAgent(tools=[WebSearchTool()], model=model, stream_outputs=True)
#
# agent.run("How many seconds would it take for a leopard at full speed to run through Pont des Arts?")

import os
from smolagents import CodeAgent, WebSearchTool, ChatMessageStreamDelta, ToolCall, ToolOutput, ActionOutput
from smolagents.models import AmazonBedrockModel  # 使用正确的模型类

# 使用 AmazonBedrockModel 而不是 AmazonBedrockServerModel
model = AmazonBedrockModel(
    model_id=os.environ.get("AMAZON_BEDROCK_MODEL_ID"),
    client_kwargs={"region_name": os.environ.get("AWS_REGION", "us-east-2")}
)

# 构建 agent
agent = CodeAgent(
    tools=[],
    model=model,
    use_structured_outputs_internally=False,  # 关键：禁用结构化输出
    code_block_tags=("```python", "```")  # 使用 markdown 代码块格式
)

# 跑任务
output = agent.run("编写代码，实现从1加到100，并输出结果的功能", stream=False)

# # 逐事件解析
# for event in output:
#     print(event)
print("Result:", output)
