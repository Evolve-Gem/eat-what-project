from flask import Flask, render_template, request, jsonify
from recommend2 import load_food_data, recommend_food
import os

app = Flask(__name__)

# 更稳的写法：无论在本地还是 Railway，都能正确找到 CSV
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "food_data.csv")
foods = load_food_data(csv_path)

# 首页路由（网页端）
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

# 网页端推荐路由
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

# 小程序 / 前后端联调用的 API 路由
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))