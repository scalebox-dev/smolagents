import os
from smolagents import CodeAgent
from smolagents.models import AmazonBedrockModel

# 初始化模型 - 关键修正：将推理配置移至正确位置
model = AmazonBedrockModel(
    model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    client_kwargs={"region_name": "us-east-1"},
    # 注意：temperature 和 max_tokens 不再在此处设置
)

# 创建agent
agent = CodeAgent(
    tools=[],
    model=model,
    executor_type="e2b"
)

# 更清晰的提示词，明确要求模型执行代码
prompt = """你是一个智能代码助手。请编写一个Python程序，随机生成一些数据，然后画成线状图。
要求：输出正确的完整的代码，代码和数据中不要包含任何中文"""

try:
    print("开始执行代码生成任务...")
    output = agent.run(prompt, stream=False)
    print("生成结果:", output)
except Exception as e:
    print(f"执行过程中出错: {e}")