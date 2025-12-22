# test_ai.py
import vertexai
from vertexai.generative_models import GenerativeModel
import google.auth

# 定义系统指令：这里我们把它设定为一个“毒舌”的资深云架构师
system_prompt = """
你是 WebEye 的资深云架构师助手。
1. 你的回答必须专业且简洁。
2. 你的语气要带有一点幽默感的“毒舌”，比如经常吐槽用户写的代码太烂。
3. 所有的回答最后必须带上一句：'别看了，快去改 Bug！'
注意：仅限回答 Google Cloud 相关的问题。
"""

try:
    credentials, project = google.auth.default()
    print(f"当前身份: {credentials.service_account_email if hasattr(credentials, 'service_account_email') else 'User Account'}")
    
    vertexai.init(project="guyue-001", location="us-central1")
    model = GenerativeModel(
        model_name="gemini-2.0-flash",
        system_instruction=[system_prompt] # 关键：在这里注入指令
    )
    q = "你是谁？"
    # q = "土豆炖牛肉怎么做"
    response = model.generate_content(q)
    print(f"AI 回复: {response.text}")
except Exception as e:
    print(f"捕获到错误: {e}")