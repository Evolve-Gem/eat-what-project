from flask import Flask, render_template, request, jsonify
from recommend2 import load_food_data, recommend_food
from openai import OpenAI
import os
import json

app = Flask(__name__)

# 加载菜品数据
foods = load_food_data("food_data.csv")

# DeepSeek 客户端
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")
client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com"
)

# =========================
# 原网页首页
# =========================
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


# =========================
# 原网页推荐
# =========================
@app.route("/recommend", methods=["POST"])
def recommend():
    mood = request.form.get("mood")
    tastes = request.form.getlist("taste")
    time_value = request.form.get("time")

    user_input = {
        "mood": mood,
        "taste": tastes,
        "time": time_value
    }

    recommendations = recommend_food(foods, user_input)
    return render_template("index.html", recommendations=recommendations)


# =========================
# 原小程序规则推荐接口
# =========================
@app.route("/api/recommend", methods=["POST"])
def api_recommend():
    data = request.get_json() or {}

    mood = data.get("mood", "")
    tastes = data.get("tastes", [])
    time_value = data.get("time", "")

    user_input = {
        "mood": mood,
        "taste": tastes,
        "time": time_value
    }

    recommendations = recommend_food(foods, user_input)

    return jsonify({
        "success": True,
        "data": recommendations
    })


# =========================
# DeepSeek 调用函数
# =========================
def call_deepseek_ai(user_text):
    if not DEEPSEEK_API_KEY:
        raise RuntimeError("未检测到 DEEPSEEK_API_KEY 环境变量")

    # 把当前菜品整理给模型看
    menu_lines = []
    for food in foods:
        name = food.get("name", "")
        price = str(food.get("price", ""))
        tags = "、".join(food.get("tags", []))
        mood = food.get("mood", "")
        time_value = food.get("time", "")

        menu_lines.append(
            f"- 菜名：{name}；价格：{price}；标签：{tags}；适合心情：{mood}；出餐时间：{time_value}"
        )

    menu_text = "\n".join(menu_lines)

    system_prompt = f"""
你是一个面向大学生校园场景的饮食决策助手。
用户会用自然语言描述自己想吃什么，请你理解需求，并且只能从下面给出的菜单中选择推荐菜品。

菜单如下：
{menu_text}

请严格输出 json，不要输出任何额外解释。
输出格式如下：
{{
  "parsedNeeds": ["需求1", "需求2", "需求3"],
  "result": {{
    "name": "菜名",
    "price": "价格",
    "score": 90,
    "reasons": ["理由1", "理由2", "理由3"]
  }},
  "aiSummary": "一段自然语言解释，说明为什么推荐这个菜"
}}
"""

    response = client.chat.completions.create(
        model="deepseek-chat",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text}
        ]
    )

    content = response.choices[0].message.content
    return json.loads(content)


# =========================
# 新增：AI 自然语言推荐接口
# =========================
@app.route("/api/ai-recommend", methods=["POST"])
def api_ai_recommend():
    data = request.get_json() or {}
    user_text = data.get("userInput", "").strip()

    if not user_text:
        return jsonify({
            "success": False,
            "message": "userInput 不能为空"
        }), 400

    try:
        ai_result = call_deepseek_ai(user_text)
        return jsonify({
            "success": True,
            "data": ai_result
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))