# coding: utf-8

import os
from enum import Enum

from vertexai.generative_models import GenerativeModel
import vertexai


# 定义系统指令：这里我们把它设定为一个“毒舌”的资深云架构师
SYSTEM_PROMPT = """
你是 WebEye 的资深云架构师助手。
1. 你的回答必须专业且简洁。
2. 你的语气要带有一点幽默感的“毒舌”，比如经常吐槽用户写的代码太烂。
3. 所有的回答最后必须带上一句：'别看了，快去改 Bug！'
注意：仅限回答 Google Cloud 相关的问题。
"""
# 定义系统指令：设置为文本分析专家，判断情感（正/负）并提取关键词，强制 AI 返回 JSON 格式
CLASSIFIER_PROMPT = """
你是一个文本分析专家。请分析用户提供的反馈文本：
1. 判断情感：正面 (Positive) 或 负面 (Negative)。
2. 提取 3 个关键词。
3. 必须严格按以下 JSON 格式返回，不要有任何多余解释：
{
  "sentiment": "正/负",
  "keywords": ["词1", "词2", "词3"]
}
"""

# 全局模型实例
g_model: GenerativeModel = None
g_classify_model: GenerativeModel = None


class AIModelRole(Enum):
    # 定义角色
    DEFAULT = "default"
    CLASSIFIER = "classifier"


def init_model():
    """
    初始化模型实例
    """
    global g_model
    global g_classify_model
    
    project_id = os.environ.get("PROJECT_ID", "Not Set")
    location = os.environ.get("LOCATION", "Not Set")
    model_name = os.environ.get("MODEL_NAME", "gemini-2.0-flash")
    vertexai.init(project=project_id, location=location)
    print(f"Current project: {project_id}")
    print(f"Current location: {location}")
    print(f"Current model: {model_name}")

    g_model = GenerativeModel(
        model_name=model_name,
        system_instruction=[SYSTEM_PROMPT] # 关键：在这里注入指令
    )
    g_classify_model = GenerativeModel(
        model_name=model_name,
        system_instruction=[CLASSIFIER_PROMPT] # 关键：在这里注入指令
    )

# 根据传入的类型使用不同的目标，如 资深云架构师、文本分析专家
def ask_gemini(prompt, role=AIModelRole.DEFAULT):
    """
    Ask Gemini for a response.
    """
    # init model instance
    if not g_model or not g_classify_model:
        init_model()

    # ask
    if role == AIModelRole.DEFAULT.value:
        response = g_model.generate_content(prompt)
    elif role == AIModelRole.CLASSIFIER.value:
        response = g_classify_model.generate_content(prompt)
    else:
        raise ValueError(f"Invalid role: {role}")
    return response.text