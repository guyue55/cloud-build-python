# coding: utf-8

import os

from flask import Flask, request, render_template, jsonify

from .core import ask_gemini, AIModelRole

app = Flask(__name__)


@app.route('/chat')
def chat():
    try:    
        user_input = request.args.get('q', '自我介绍一下')
        role = request.args.get('role', AIModelRole.DEFAULT)
        print(f"Role: {role}, User input: {user_input[:80]}")
        ai_response = ask_gemini(user_input, role.lower())
        return jsonify({"reply": ai_response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/")
def hello_world():
    """首页处理函数.

    返回渲染后的首页模板.

    Returns:
        str: 渲染后的 HTML 内容.
    """
    env_test = os.environ.get("ENV_TEST", "Not Set")
    env_date = os.environ.get("ENV_DATE", "Not Set")
    return render_template("index.html", env_test=env_test, env_date=env_date)


@app.route("/health")
def health():
    """健康检查接口.

    用于确认服务是否正常运行.

    Returns:
        tuple: (响应内容, HTTP状态码).
    """
    return "OK", 200


@app.route("/process", methods=["POST"])
def process():
    """处理请求接口.

    接收 JSON 数据并原样返回 (Echo).

    Returns:
        tuple: (JSON响应数据, HTTP状态码).
        
    Raises:
        400: 如果请求体不是有效的 JSON 格式.
    """
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Invalid JSON or Content-Type"}), 400
    return jsonify(data), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))