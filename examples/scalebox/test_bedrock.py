import boto3
from botocore.exceptions import ClientError


def list_bedrock_models():
    """
    列出 Amazon Bedrock 中的基础模型、自定义模型和导入的模型。
    """
    # 创建 Bedrock 客户端
    try:
        bedrock_client = boto3.client('bedrock')
    except Exception as e:
        print(f"创建 Bedrock 客户端时出错: {e}")
        return

    print("=" * 50)
    print("1. Amazon Bedrock 基础模型列表")
    print("=" * 50)

    try:
        # 获取基础模型列表
        response_fm = bedrock_client.list_foundation_models()
        models = response_fm['modelSummaries']

        for model in models:
            print(f"• 模型ID: {model['modelId']}")
            print(f"  模型名称: {model['modelName']}")
            print(f"  提供商: {model['providerName']}")
            # 判断是否为流式响应模型
            model_stream_support = model.get('modelStreamSupportSupported', False)
            print(f"  支持流式响应: {model_stream_support}")
            print(f"  模型ARN: {model['modelArn']}")
            print("  -" * 20)

    except ClientError as e:
        print(f"获取基础模型列表时发生错误: {e.response['Error']['Code']} - {e.response['Error']['Message']}")
    except KeyError as e:
        print(f"解析响应数据时出错，缺少键: {e}")

    print("\n" + "=" * 50)
    print("2. 您的自定义模型列表")
    print("=" * 50)

    try:
        # 获取自定义模型列表
        response_custom = bedrock_client.list_custom_models()
        custom_models = response_custom.get('modelSummaries', [])

        if not custom_models:
            print("暂无自定义模型。")
        else:
            for model in custom_models:
                print(f"• 模型ID: {model['modelId']}")
                print(f"  模型名称: {model['modelName']}")
                print(f"  基础模型: {model['baseModelArn']}")
                print(f"  创建时间: {model['creationTime']}")
                print("  -" * 20)

    except ClientError as e:
        print(f"获取自定义模型列表时发生错误: {e.response['Error']['Code']} - {e.response['Error']['Message']}")

    print("\n" + "=" * 50)
    print("3. 您导入的模型列表")
    print("=" * 50)

    try:
        # 获取导入的模型列表 (注意：此API可能需特定权限或仅在特定场景下有效)
        response_imported = bedrock_client.list_imported_models()
        imported_models = response_imported.get('modelSummaries', [])

        if not imported_models:
            print("暂无通过导入功能添加的模型。")
        else:
            for model in imported_models:
                print(f"• 模型ID: {model['modelId']}")
                print(f"  模型名称: {model['modelName']}")
                print(f"  状态: {model['modelStatus']}")
                print("  -" * 20)

    except ClientError as e:
        # 如果没有权限或该API不可用，可能会报错
        error_code = e.response['Error']['Code']
        if error_code == 'AccessDeniedException':
            print("权限不足，无法访问导入的模型列表。")
        elif error_code == 'ValidationException':
            print("list_imported_models API 在当前环境或条件下可能不可用。")
        else:
            print(f"获取导入模型列表时发生错误: {error_code} - {e.response['Error']['Message']}")


if __name__ == "__main__":
    list_bedrock_models()