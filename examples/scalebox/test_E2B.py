import os
import json
from smolagents import CodeAgent, Tool
from smolagents.models import AmazonBedrockModel

# 确保使用 DeepSeek 模型 ID
DEEPSEEK_MODEL_ID = "us.deepseek.r1-v1:0"  # 或其他可用的 DeepSeek 模型 ID

# 初始化模型，专门针对 DeepSeek 优化
model = AmazonBedrockModel(
    model_id=os.environ.get("AMAZON_BEDROCK_MODEL_ID", DEEPSEEK_MODEL_ID),
    client_kwargs={"region_name": os.environ.get("AWS_REGION", "us-east-2")},
    temperature=0.1,  # 降低随机性，提高代码质量
    max_tokens=2048,  # 限制输出长度
)


# 创建一个简单的占位工具
class PlaceholderTool(Tool):
    name = "placeholder"
    description = "A placeholder tool"

    def use(self, *args, **kwargs):
        return "Tool executed"


# 构建 agent，针对代码生成优化
agent = CodeAgent(
    tools=[],  # 使用简单工具
    model=model,
    use_structured_outputs_internally=False,
    add_base_tools=False,  # 禁用可能干扰的基础工具
    max_steps=5,  # 减少最大步数
    # verbosity=2,  # 调试信息
    code_block_tags=("```python", "```"),
    executor_type="e2b"
)

# 更清晰的提示词
prompt = """请生成一个完整的Python程序，实现从1加到100的功能，输出完整代码"""

# 要求：
# 1. 使用标准的Python语法
# 2. 代码必须包含在 ```python 代码块中
# 3. 程序应该计算1到100的整数和
# 4. 最后打印结果
#
# 只需要输出代码，不需要解释。
# """

try:
    print("开始执行代码生成任务...")
    output = agent.run(prompt, stream=False)
    print("生成结果:", output)

    # 尝试提取代码并执行
#     if hasattr(output, 'reasoningContent'):
#         content = output.reasoningContent
#         if hasattr(content, 'reasoningText'):
#             text = content.reasoningText.text
#             # 尝试从文本中提取代码块
#             if '```python' in text:
#                 code_start = text.find('```python') + 9
#                 code_end = text.find('```', code_start)
#                 python_code = text[code_start:code_end].strip()
#                 print("提取的Python代码:")
#                 print(python_code)
#
#                 # 尝试执行生成的代码
#                 try:
#                     exec(python_code)
#                     print("代码执行成功!")
#                 except Exception as e:
#                     print(f"代码执行错误: {e}")
#
except Exception as e:
    print(f"执行过程中出错: {e}")