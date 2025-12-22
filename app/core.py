# coding: utf-8

import os

from vertexai.generative_models import GenerativeModel
import vertexai


# 定义系统指令：这里我们把它设定为一个“毒舌”的资深云架构师
g_system_prompt = """
你是 WebEye 的资深云架构师助手。
1. 你的回答必须专业且简洁。
2. 你的语气要带有一点幽默感的“毒舌”，比如经常吐槽用户写的代码太烂。
3. 所有的回答最后必须带上一句：'别看了，快去改 Bug！'
注意：仅限回答 Google Cloud 相关的问题。
"""

g_model: GenerativeModel = None

def ask_gemini(prompt):
    """
    Ask Gemini for a response.
    """
    global g_model

    # init model instance
    if not g_model:
        project_id = os.environ.get("PROJECT_ID", "Not Set")
        location = os.environ.get("LOCATION", "Not Set")
        model_name = os.environ.get("MODEL_NAME", "gemini-2.0-flash")
        vertexai.init(project=project_id, location=location)
        g_model = GenerativeModel(
            model_name=model_name,
            system_instruction=[g_system_prompt] # 关键：在这里注入指令
        )

    # ask
    response = g_model.generate_content(prompt)
    return response.text